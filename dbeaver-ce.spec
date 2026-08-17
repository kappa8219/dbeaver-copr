%global debug_package %{nil}
%global __strip /bin/true
%global __requires_exclude_from ^%{_datadir}/dbeaver-ce/.*$

Name:           dbeaver-ce
Version:        26.1.4
Release:        1%{?dist}
Summary:        Universal Database Manager and SQL Client
License:        Apache-2.0
URL:            https://dbeaver.io/
Source0:        https://github.com/dbeaver/dbeaver/releases/download/%{version}/dbeaver-ce-%{version}-linux-x86_64.rpm
Source1:        https://github.com/dbeaver/dbeaver/releases/download/%{version}/dbeaver-ce-%{version}-linux-aarch64.rpm
ExclusiveArch:  x86_64 aarch64

BuildRequires:  cpio
BuildRequires:  desktop-file-utils
BuildRequires:  rpm

%description
DBeaver Community Edition is a free and open source universal database manager
and SQL client.

%prep
%ifarch x86_64
%global upstream_rpm %{SOURCE0}
%global upstream_sha256 d49eec1f0b27df6ddf1a7221c1c93a12e515ad6d3f36e420ea02c3489c000332
%else
%global upstream_rpm %{SOURCE1}
%global upstream_sha256 90d26751f4501b38dbe29c53343a1bc014b0c99e52f77bbcec105d82f8d5200a
%endif
echo "%{upstream_sha256}  %{upstream_rpm}" | sha256sum --check

%install
rpm2cpio %{upstream_rpm} | cpio --extract --make-directories --quiet --directory %{buildroot}
ln -snf ../share/dbeaver-ce/dbeaver %{buildroot}%{_bindir}/dbeaver-ce
find %{buildroot}%{_datadir}/dbeaver-ce -mindepth 1 -maxdepth 1 ! -name licenses \
    -printf '%{_datadir}/dbeaver-ce/%%f\n' > %{name}.files

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/dbeaver-ce.desktop

%files -f %{name}.files
%license %{_datadir}/dbeaver-ce/licenses
%{_bindir}/dbeaver-ce
%{_datadir}/applications/dbeaver-ce.desktop

%changelog
* Mon Aug 17 2026 kappa8219 <4374115+kappa8219@users.noreply.github.com> - 26.1.4-1
- Package DBeaver Community Edition 26.1.4

* Mon Aug 17 2026 OK <o.kraievyi@quadient.com> - 26.1.5-1
- Package the upstream DBeaver Community Edition RPMs for COPR
