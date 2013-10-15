Summary: Apache ActiveMQ
Name: activemq
Version: 5.5.0
Release: 1%{?dist}
License: Apache
Group: Network/Daemons
Source0: apache-activemq-%{version}-bin.tar.gz
Source1: wlcg-patch.tgz
Source2: activemq.xml
Source3: jetty-realm.properties
Source4: jetty.xml
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Requires: tanukiwrapper >= 3.2.0

#%define buildver 5.1.0

%define homedir /usr/share/%{name}
%define libdir /var/lib/%{name}
%define libexecdir /usr/libexec/%{name}
%define cachedir /var/cache/%{name}
%define docsdir /usr/share/doc/%{name}-%{version}

%description
ApacheMQ is a JMS Compliant Messaging System

%package info-provider
Summary: An LDAP information provider for activemq
Group:grid/lcg
%description info-provider
An LDAP infomation provider for activemq

%package meta
Summary: A metapackage
Group:grid/lcg
Requires: activemq = %{version}-%{release}, activemq-info-provider = %{version}-%{release}
%description meta
A metapackage

%prep
%setup -q -a1 -n apache-activemq-%{version}

%build
install --directory ${RPM_BUILD_ROOT}

%install
rm -rf $RPM_BUILD_ROOT
install --directory ${RPM_BUILD_ROOT}%{homedir}
install --directory ${RPM_BUILD_ROOT}%{homedir}/bin
install --directory ${RPM_BUILD_ROOT}%{docsdir}
install --directory ${RPM_BUILD_ROOT}%{libdir}/lib
install --directory ${RPM_BUILD_ROOT}%{libexecdir}
install --directory ${RPM_BUILD_ROOT}%{libdir}/webapps
install --directory ${RPM_BUILD_ROOT}%{cachedir}
install --directory ${RPM_BUILD_ROOT}%{cachedir}/data
install --directory ${RPM_BUILD_ROOT}/var/log/%{name}
install --directory ${RPM_BUILD_ROOT}/var/run/%{name}
install --directory ${RPM_BUILD_ROOT}/etc/%{name}
install --directory ${RPM_BUILD_ROOT}/etc/init.d
install --directory ${RPM_BUILD_ROOT}/etc/httpd/conf.d

# Config files
install %{SOURCE2} ${RPM_BUILD_ROOT}/etc/%{name}
install conf/credentials.properties ${RPM_BUILD_ROOT}/etc/%{name}
install conf/jetty.xml  ${RPM_BUILD_ROOT}/etc/%{name}
install %{SOURCE3} ${RPM_BUILD_ROOT}/etc/%{name}
install %{SOURCE4} ${RPM_BUILD_ROOT}/etc/%{name}
install conf/log4j.properties ${RPM_BUILD_ROOT}/etc/%{name}
install conf/activemq-wrapper.conf ${RPM_BUILD_ROOT}/etc/%{name}
install conf/activemq-httpd.conf ${RPM_BUILD_ROOT}/etc/httpd/conf.d

# startup script
install bin/activemq ${RPM_BUILD_ROOT}/etc/init.d

# Bin and doc dirs
install *.txt *.html ${RPM_BUILD_ROOT}%{docsdir}
cp -r docs ${RPM_BUILD_ROOT}%{docsdir}

install bin/run.jar bin/activemq-admin ${RPM_BUILD_ROOT}%{homedir}/bin
install --directory ${RPM_BUILD_ROOT}/usr/bin
%{__ln_s} -f %{homedir}/bin/activemq-admin ${RPM_BUILD_ROOT}/usr/bin

# Runtime directory
cp -r lib ${RPM_BUILD_ROOT}%{libdir}
cp -r webapps/admin ${RPM_BUILD_ROOT}%{libdir}/webapps

# Info provider
install info-provider-activemq ${RPM_BUILD_ROOT}/%{libexecdir}

pushd ${RPM_BUILD_ROOT}%{homedir}
    [ -d conf ] || %{__ln_s} -f /etc/%{name} conf
    [ -d data ] || %{__ln_s} -f %{cachedir}/data data
    [ -d docs ] || %{__ln_s} -f %{docsdir} docs
    [ -d lib ] || %{__ln_s} -f %{libdir}/lib lib
    [ -d lib ] || %{__ln_s} -f %{libdir}/libexec libexec
    [ -d log ] || %{__ln_s} -f /var/log/%{name} log
    [ -d webapps ] || %{__ln_s} -f %{libdir}/webapps webapps
popd

#pushd $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}
#  for file in $(ls -1)
#  do
#    sed -i 's,${activemq.base},/usr/share/activemq/,g' $file
#  done
#popd


%pre
# Add the "activemq" user and group
# we need a shell to be able to use su - later
/usr/sbin/groupadd -g 92 -r activemq 2> /dev/null || :
/usr/sbin/useradd -c "Apache Activemq" -u 92 -g activemq \
    -s /bin/bash -r -d /usr/share/activemq activemq 2> /dev/null || :

%post
# install activemq (but don't activate)
/sbin/chkconfig --add activemq

%preun
if [ $1 = 0 ]; then
    [ -f /var/lock/subsys/activemq ] && /etc/init.d/activemq stop
    [ -f /etc/init.d/activemq ] && /sbin/chkconfig --del activemq
fi

%postun

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%attr(755,root,root) /usr/bin/activemq-admin
%{homedir}
%docdir %{docsdir}
%{docsdir}
%{libdir}
%attr(775,activemq,activemq) %dir /var/log/%{name}
%attr(775,activemq,activemq) %dir /var/run/%{name}
%attr(775,root,activemq) %dir %{cachedir}/data
%attr(755,root,root) /etc/init.d/activemq
%config(noreplace) /etc/httpd/conf.d/activemq-httpd.conf
%config(noreplace) /etc/%{name}/*

%files info-provider
%defattr(-,root,root)
%attr(755,root,root) %{libexecdir}/info-provider-activemq

%changelog
* Fri Sep 02 2011 Michael Stahnke <stahnma@fedoraproject.org> - 5.5.0-1
- Update for 5.5.0

* Sat Jan 16 2010 R.I.Pienaar <rip@devco.net> 5.3.0
- Adjusted for ActiveMQ 5.3.0

* Wed Oct 29 2008 James Casey <james.casey@cern.ch> 5.2.0-2
- fixed defattr on subpackages

* Tue Sep 02 2008 James Casey <james.casey@cern.ch> 5.2.0-1
- Upgraded to activemq 5.2.0

* Tue Sep 02 2008 James Casey <james.casey@cern.ch> 5.1.0-7
- Added separate logging of messages whenever the logging interceptor is enabled in the config file
- removed BrokerRegistry messages casued by REST API
- now we don't log messages to stdout (so no duplicates in wrapper log).
- upped the number and size of the rolling logs

* Fri Aug 29 2008 James Casey <james.casey@cern.ch> 5.1.0-6
- make ServiceData be correct LDIF

* Wed Aug 27 2008 James Casey <james.casey@cern.ch> 5.1.0-5
- changed glue path from mds-vo-name=local to =resource
