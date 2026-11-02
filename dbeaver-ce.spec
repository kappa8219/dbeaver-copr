%global debug_package %{nil}
%global __strip /bin/true
%global __requires_exclude_from ^%{_datadir}/dbeaver-ce/.*$

Name:           dbeaver-ce
Version:        26.2.4
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
%global upstream_sha256 d8ea7d5388dbaae63fd5630682a0effbcada327605a85dd7b3cfd6f717d078b4
%else
%global upstream_rpm %{SOURCE1}
%global upstream_sha256 1966c19f369d7f71dd325cd86c79b491354d621579a19d575689d29eaa2c23fc
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
* Tue Oct 27 2026 OK <4374115+kappa8219@users.noreply.github.com> - 26.2.4-1
- Update to DBeaver CE 26.2.4

* Mon Oct 19 2026 OK <4374115+kappa8219@users.noreply.github.com> - 26.2.3-1
- Update to DBeaver Community Edition 26.2.3
