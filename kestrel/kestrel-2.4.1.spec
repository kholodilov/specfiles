# To build:
# 
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# wget http://robey.github.com/kestrel/download/kestrel-2.4.1.zip -O ~/rpmbuild/SOURCES/kestrel-2.4.1.zip

%define kestrel_name kestrel
%define kestrel_branch 2.4
%define kestrel_version 2.4.1
%define scala_version 2.9.2
%define release_version 2
%define kestrel_home /usr/local/%{kestrel_name}/%{kestrel_name}_%{scala_version}-%{kestrel_version}
%define kestrel_user kestrel
%define kestrel_group kestrel

Name: %{kestrel_name}
Version: %{kestrel_version}
Release: %{release_version}
Summary: Kestrel is a simple, distributed message queue written on the JVM.
License: Apache License 2.0 
URL: http://robey.github.com/kestrel/
Group: Development/Libraries
Source0: %{kestrel_name}-%{kestrel_version}.zip
Source1: %{kestrel_name}.sh
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Requires: sh-utils, textutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service
Provides: kestrel
Vendor: Robey Pointer <robeypointer@gmail.com>
Packager: Anton Zadorozhniy <anton.zadorozhniy@gmail.com>
BuildArch: noarch

%description
Kestrel is a simple, distributed message queue written on the JVM, based on Blaine Cook's "starling".

Each server handles a set of reliable, ordered message queues, with no cross communication, resulting in a cluster of k-ordered ("loosely ordered") queues. Kestrel is fast, small, and reliable.

%prep
%setup -n %{kestrel_name}-%{kestrel_version}

%build

%clean
rm -rf %{buildroot}

%install
install -d -m 755 %{buildroot}/%{kestrel_home}/
install    -m 644 %{_builddir}/%{kestrel_name}-%{kestrel_version}/*.jar           %{buildroot}/%{kestrel_home}/

install -d -m 755 %{buildroot}/%{kestrel_home}/config/
install    -m 644 %{_builddir}/%{kestrel_name}-%{kestrel_version}/config/*.scala           %{buildroot}/%{kestrel_home}/config

install -d -m 755 %{buildroot}/%{kestrel_home}/libs/
install    -m 644 %{_builddir}/%{kestrel_name}-%{kestrel_version}/libs/*.jar           %{buildroot}/%{kestrel_home}/libs

install -d -m 755 %{buildroot}/%{kestrel_home}/scripts/
install    -m 755 %{_builddir}/%{kestrel_name}-%{kestrel_version}/scripts/*.sh           %{buildroot}/%{kestrel_home}/scripts

install -d -m 755 %{buildroot}/%{kestrel_home}/scripts/load/
install    -m 755 %{_builddir}/%{kestrel_name}-%{kestrel_version}/scripts/load/*           %{buildroot}/%{kestrel_home}/scripts/load

cd %{buildroot}/usr/local/%{kestrel_name}/
ln -s %{kestrel_name}_%{scala_version}-%{kestrel_version} current
cd -

install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %{_sourcedir}/kestrel.sh           	%{buildroot}/%{_initrddir}/kestrel

install -d -m 755 %{buildroot}/var/run/%{kestrel_name}
install -d -m 755 %{buildroot}/var/log/%{kestrel_name}

%pre
getent group %{kestrel_group} >/dev/null || groupadd -r %{kestrel_group}
getent passwd %{kestrel_user} >/dev/null || /usr/sbin/useradd --comment "Kestrel Daemon User" --shell /bin/bash -M -r -g %{kestrel_group} --home %{kestrel_home} %{kestrel_user}

%post

%preun
if [ "$1" = "0" ] ; then
service %{name} stop > /dev/null 2>&1
fi

%files
%defattr(-,%{kestrel_user},%{kestrel_group})
%{kestrel_home}/*
/usr/local/%{kestrel_name}/current
%attr(755,%{kestrel_user},%{kestrel_group}) %{_initrddir}/kestrel
/var/log/%{kestrel_name}
/var/run/%{kestrel_name}

%changelog
* Sun Jan 27 2013 - Dmitry Kholodilov <dmitry.kholodilov@gmail.com>
- Fix exit code for kestrel service status request
* Tue Jan 15 2013 - Anton Zadorozhniy <anton.zadorozhniy@gmail.com>
- Initial release.