spec := dbeaver-ce.spec
version := 26.2.0
release_url := https://github.com/dbeaver/dbeaver/releases/download/$(version)
sources := dbeaver-ce-$(version)-linux-x86_64.rpm dbeaver-ce-$(version)-linux-aarch64.rpm

.PHONY: srpm
srpm:
	for source in $(sources); do curl --fail --location --output $$source $(release_url)/$$source; done
	rpmbuild -bs --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
