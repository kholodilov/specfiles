# To build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
#
# wget https://raw.github.com/dartov/specfiles/master/flume-ext-patch/flume-ext-patch.spec -O ~/rpmbuild/SPECS/flume-ext-patch.spec
# wget http://10.66.48.10:8080/nexus/content/repositories/releases/ru/megafon/datalabs/flume/flume-ext-patch/1.0.0/flume-ext-patch-1.0.0.tar.gz -O ~/rpmbuild/SOURCES/flume-ext-patch-1.0.0.tar.gz
#
# rpmbuild -bb ~/rpmbuild/SPECS/flume-ext-patch.spec

%define __jar_repack %{nil}

%define flume_lib_directory /usr/lib/flume-ng/lib
%define flume_lib_backup_directory /usr/lib/flume-ng/lib.bk

Name: flume-ext-patch
Version: 1.0.0
Release: 1
Summary: Megafon Data Labs Flume-NG extensions
License: Proprietary
Group: Development/System
Source0: %{name}-%{version}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Requires: sh-utils, textutils, flume-ng
Provides: flume-ext-patch
Vendor: Megafon
Packager: Dmitry Kholodilov <dmitry.kholodilov@gmail.com>
BuildArch: noarch

%description
Flume-NG extensions: UDP source, Kestrel sink, Thrift interceptor

%prep
%setup -c %{name}-%{version}
rm -rf %{buildroot}

%build

%clean

%install
mkdir -p %{buildroot}/%{flume_lib_directory}
cp %{_builddir}/%{name}-%{version}/* %{buildroot}/%{flume_lib_directory}

%pre
mkdir %{flume_lib_backup_directory}
mv %{flume_lib_directory}/libthrift-* %{flume_lib_backup_directory}

%post

%preun

%postun
mv %{flume_lib_backup_directory}/* %{flume_lib_directory}
rmdir %{flume_lib_backup_directory}

%files
%{flume_lib_directory}/*

%changelog
* Tue Jan 21 2013 - Dmitry Kholodilov <dmitry.kholodilov@gmail.com>
- Initial version