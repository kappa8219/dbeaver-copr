%global debug_package %{nil}
%global __strip /bin/true
%global __requires_exclude_from ^%{_datadir}/dbeaver-ce/.*$

Name:           dbeaver-ce
Version:        26.2.0
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
%global upstream_sha256 acb3bc2fc2c3547df154f2bec20b5dc6b7941bd420ccb778de94e43e7170947e
%else
%global upstream_rpm %{SOURCE1}
%global upstream_sha256 a10c532c0ebce880643937083ccc3b77ca1a0a3869efab2b557d55a6b14a1972
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
* Mon Aug 31 2026 OK <o.kraievyi@gmail.com> - 26.2.0-1
- Update to DBeaver Community Edition 26.2.0

* Mon Aug 17 2026 OK <o.kraievyi@gmail.com> - 26.1.5-1
- Package the upstream DBeaver Community Edition RPMs for COPR
