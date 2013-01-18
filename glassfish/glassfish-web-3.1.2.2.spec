# To build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
#
# wget https://raw.github.com/dartov/specfiles/master/glassfish/glassfish-web-3.1.2.2.spec -O ~/rpmbuild/SPECS/glassfish-web-3.1.2.2.spec
# wget https://raw.github.com/dartov/specfiles/master/glassfish/glassfish-web.init -O ~/rpmbuild/SOURCES/glassfish-web.init
# wget https://raw.github.com/dartov/specfiles/master/glassfish/asadmin -O ~/rpmbuild/SOURCES/asadmin
# wget http://download.java.net/glassfish/3.1.2.2/release/glassfish-3.1.2.2-web.zip -O ~/rpmbuild/SOURCES/glassfish-web-3.1.2.2.zip
#
# rpmbuild -bb ~/rpmbuild/SPECS/glassfish-web-3.1.2.2.spec

%define __jar_repack %{nil}

%define glassfish_name glassfish-web
%define glassfish_version 3.1.2.2
%define release_version 4
%define glassfish_parent /opt
%define glassfish_home %{glassfish_parent}/%{glassfish_name}
%define glassfish_user glassfish
%define glassfish_group glassfish

%define sourceroot %{_builddir}/glassfish3

Name: %{glassfish_name}
Version: %{glassfish_version}
Release: %{release_version}
Summary: GlassFish is a Java EE open source application server.
License: COMMON DEVELOPMENT AND DISTRIBUTION LICENSE (CDDL)Version 1.1
URL: http://glassfish.java.net/
Group: Development/System
Source0: %{glassfish_name}-%{glassfish_version}.zip
Source1: %{glassfish_name}.init
Source2: asadmin
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Requires: sh-utils, textutils, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/service
Provides: glassfish-web
Vendor: Oracle
Packager: Dmitry Kholodilov <dmitry.kholodilov@gmail.com>
BuildArch: noarch

%description
GlassFish is an open source, production-ready, Java EE-compatible application server.
GlassFish version 3 provides a small footprint, fully-featured implementation of Java EE 6.

%prep
%setup -n glassfish3 
rm -rf %{buildroot}

%build

%clean

%install
mkdir -p %{buildroot}/%{glassfish_parent} 
cp -r %{_builddir}/glassfish3 %{buildroot}/%{glassfish_home}
rm -rf %{buildroot}/%{glassfish_home}/glassfish/domains/*

install -m 755 %{_sourcedir}/asadmin %{buildroot}/%{glassfish_home}/bin/asadmin
mkdir -p %{buildroot}/%{_bindir}
ln -s %{glassfish_home}/bin/asadmin %{buildroot}/%{_bindir}

mkdir -p %{buildroot}/%{_initrddir}
cp %{_sourcedir}/%{glassfish_name}.init %{buildroot}/%{_initrddir}/%{glassfish_name}

%pre
getent group %{glassfish_group} >/dev/null || groupadd -r %{glassfish_group}
getent passwd %{glassfish_user} >/dev/null || /usr/sbin/useradd --comment "Glassfish Daemon User" --shell /bin/bash --system -g %{glassfish_group} --create-home %{glassfish_user}

%post

%preun
if [ "$1" = "0" ] ; then
service %{name} stop > /dev/null 2>&1
fi

%files
%defattr(-,%{glassfish_user},%{glassfish_group})
%{glassfish_home}
%config(noreplace) %{glassfish_home}/glassfish/config/asenv.conf
%config(noreplace) %{glassfish_home}/glassfish/config/glassfish.container
%config(noreplace) %{glassfish_home}/glassfish/config/osgi.properties
%attr(755,root,root) %{_initrddir}/%{glassfish_name}
%{_bindir}/asadmin

%changelog
* Tue Jan 18 2013 - Dmitry Kholodilov <dmitry.kholodilov@gmail.com>
- Enable status reporting and chkconfig for daemon
* Tue Jan 18 2013 - Dmitry Kholodilov <dmitry.kholodilov@gmail.com>
- Correctly create home directory for glassfish user
* Tue Jan 17 2013 - Dmitry Kholodilov <dmitry.kholodilov@gmail.com>
- Added asadmin symlink in /usr/bin
* Tue Jan 16 2013 - Dmitry Kholodilov <dmitry.kholodilov@gmail.com>
- Initial release
