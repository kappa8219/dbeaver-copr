#!/usr/bin/env python3
"""Prepare a packaging PR for the latest stable DBeaver release."""

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
API_URL = "https://api.github.com/repos/dbeaver/dbeaver/releases/latest"
ASSET_BASE = "https://github.com/dbeaver/dbeaver/releases/download/"


def get(url):
    headers = {"User-Agent": "dbeaver-copr-release-check"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    return urlopen(Request(url, headers=headers), timeout=180)


def sha256(url):
    if not url.startswith(ASSET_BASE):
        raise ValueError(f"Unexpected upstream asset URL: {url}")
    digest = hashlib.sha256()
    with get(url) as response:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def replace_once(text, pattern, replacement, label):
    result, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise ValueError(f"Expected one {label}; found {count}")
    return result


def main():
    with get(API_URL) as response:
        release = json.load(response)
    if release.get("draft") or release.get("prerelease"):
        raise ValueError("Latest release is not stable")
    version = release.get("tag_name", "")
    if not re.fullmatch(r"\d+(?:\.\d+)+", version):
        raise ValueError(f"Unexpected release tag: {version}")

    spec_path = ROOT / "dbeaver-ce.spec"
    makefile_path = ROOT / ".copr/Makefile"
    spec, makefile = spec_path.read_text(), makefile_path.read_text()
    current_match = re.search(r"^Version:\s+(\S+)$", spec, re.MULTILINE)
    if not current_match:
        raise ValueError("Could not read DBeaver package version")
    current = current_match.group(1)
    if tuple(map(int, version.split("."))) <= tuple(map(int, current.split("."))):
        print("updated=false")
        print(f"version={current}")
        print(f"release_url={release.get('html_url', '')}")
        return

    names = [f"dbeaver-ce-{version}-linux-x86_64.rpm", f"dbeaver-ce-{version}-linux-aarch64.rpm"]
    assets = {asset.get("name"): asset.get("browser_download_url") for asset in release.get("assets", [])}
    urls = [assets.get(name) for name in names]
    if any(not url for url in urls):
        raise ValueError("Release is missing one of the expected architecture RPMs")
    hashes = [sha256(url) for url in urls]

    spec = replace_once(spec, r"^(Version:\s+)\S+$", rf"\g<1>{version}", "Version")
    pattern = r"^(%global upstream_sha256 )[0-9a-f]{64}$"
    spec, count = re.subn(pattern, lambda m: m.group(1) + hashes.pop(0), spec, count=2, flags=re.MULTILINE)
    if count != 2 or hashes:
        raise ValueError("Expected the x86_64 and aarch64 source checksums")
    makefile = replace_once(makefile, r"^(version := )\S+$", rf"\g<1>{version}", "COPR version")

    date = datetime.now(timezone.utc).strftime("%a %b %d %Y")
    entry = f"* {date} OK <4374115+kappa8219@users.noreply.github.com> - {version}-1\n- Update to DBeaver CE {version}\n\n"
    spec = replace_once(spec, r"^%changelog[ \t]*\n", "%changelog\n" + entry, "changelog")
    spec = replace_once(spec, r"^(Release:\s+)\S+$", r"\g<1>1%{?dist}", "Release")

    spec_path.write_text(spec)
    makefile_path.write_text(makefile)
    print("updated=true")
    print(f"version={version}")
    print(f"release_url={release.get('html_url', '')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Release update failed: {error}", file=sys.stderr)
        sys.exit(1)
