%global release 1

%global ng_bin_dir %{_libexecdir}/%{name}
%global ng_cgi_dir /usr/lib/%{name}/cgi-bin
%global ng_doc_dir %{_defaultdocdir}/%{name}
%global ng_etc_dir %{_sysconfdir}/%{name}
%global ng_examples_dir %{_datadir}/%{name}/examples
%global ng_www_dir %{_datadir}/%{name}/htdocs
%global ng_util_dir %{_datadir}/%{name}/util
%global ng_rrd_dir %{_localstatedir}/spool/%{name}/rrd
%global ng_log_file %{_localstatedir}/log/%{name}/nagiosgraph.log
%global ng_cgilog_file %{_localstatedir}/log/%{name}/nagiosgraph-cgi.log

Summary: A Nagios add-on which archives and graphs data
Name: nagiosgraph
Version: VERSION
Release: %{release}
Group: Applications/System
Source: http://sourceforge.net/projects/nagiosgraph/files/nagiosgraph/%{version}/%{name}-%{version}.tar.gz
URL: http://nagiosgraph.sourceforge.net/
License: Artistic 2.0
Requires: nagios, httpd, perl, perl(CGI), perl(RRDs), perl(GD)
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: perl

%description
Nagiosgraph is an add-on to Nagios. It collects performance data
into RRD files and displays graphs in web pages.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} NG_LAYOUT=redhat perl install.pl --no-check-prereq --no-chown

%post
cp %{_sysconfdir}/%{name}/nagiosgraph-apache.conf %{_sysconfdir}/httpd/conf.d/nagiosgraph.conf
cp -p %{_sysconfdir}/nagios/nagios.cfg %{_sysconfdir}/nagios/nagios.cfg-saved
cat %{_sysconfdir}/%{name}/nagiosgraph-nagios.cfg >> %{_sysconfdir}/nagios/nagios.cfg
cp -p %{_sysconfdir}/nagios/objects/commands.cfg %{_sysconfdir}/nagios/objects/commands.cfg-saved
cat %{_sysconfdir}/%{name}/nagiosgraph-commands.cfg >> %{_sysconfdir}/nagios/objects/commands.cfg
%{_initrddir}/httpd restart
%{_initrddir}/nagios restart

%postun
rm %{_sysconfdir}/httpd/conf.d/nagiosgraph.conf
%{_initrddir}/httpd restart
%{_initrddir}/nagios restart

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%attr(755,root,root) %{ng_bin_dir}/insert.pl
%attr(755,root,root) %{ng_cgi_dir}/show.cgi
%attr(755,root,root) %{ng_cgi_dir}/showconfig.cgi
%attr(755,root,root) %{ng_cgi_dir}/showgraph.cgi
%attr(755,root,root) %{ng_cgi_dir}/showgroup.cgi
%attr(755,root,root) %{ng_cgi_dir}/showhost.cgi
%attr(755,root,root) %{ng_cgi_dir}/showservice.cgi
%attr(755,root,root) %{ng_cgi_dir}/testcolor.cgi
%doc %{ng_doc_dir}/AUTHORS
%doc %{ng_doc_dir}/CHANGELOG
%doc %{ng_doc_dir}/INSTALL
%doc %{ng_doc_dir}/README
%doc %{ng_doc_dir}/TODO
%config(noreplace) %{ng_etc_dir}/access.conf
%config(noreplace) %{ng_etc_dir}/datasetdb.conf
%config(noreplace) %{ng_etc_dir}/groupdb.conf
%config(noreplace) %{ng_etc_dir}/hostdb.conf
%config(noreplace) %{ng_etc_dir}/labels.conf
%config(noreplace) %{ng_etc_dir}/map
%config(noreplace) %{ng_etc_dir}/nagiosgraph.conf
%config(noreplace) %{ng_etc_dir}/nagiosgraph_fr.conf
%config(noreplace) %{ng_etc_dir}/nagiosgraph_de.conf
%config(noreplace) %{ng_etc_dir}/nagiosgraph_es.conf
%config(noreplace) %{ng_etc_dir}/nagiosgraph-apache.conf
%config(noreplace) %{ng_etc_dir}/nagiosgraph-nagios.cfg
%config(noreplace) %{ng_etc_dir}/nagiosgraph-commands.cfg
%config(noreplace) %{ng_etc_dir}/ngshared.pm
%config(noreplace) %{ng_etc_dir}/rrdopts.conf
%config(noreplace) %{ng_etc_dir}/servdb.conf
%{ng_examples_dir}/nagiosgraph.1.css
%{ng_examples_dir}/nagiosgraph.2.css
%{ng_examples_dir}/map_minimal
%{ng_examples_dir}/map_examples
%{ng_examples_dir}/map_mwall
%{ng_examples_dir}/nagiosgraph-apache.conf
%{ng_examples_dir}/nagiosgraph-nagios.cfg
%{ng_examples_dir}/nagiosgraph-commands.cfg
%{ng_examples_dir}/map_1_4_4
%{ng_examples_dir}/map_1_3
%{ng_examples_dir}/map_1_4_3
%{ng_examples_dir}/action.gif
%{ng_examples_dir}/nagiosgraph.ssi
%{ng_www_dir}/nagiosgraph.css
%{ng_www_dir}/nagiosgraph.js
%attr(755,root,root) %{ng_util_dir}/testentry.pl
%attr(755,root,root) %{ng_util_dir}/upgrade.pl
%attr(775,nagios,apache) %{ng_rrd_dir}
%attr(644,nagios,nagios) %{ng_log_file}
%attr(644,apache,apache) %{ng_cgilog_file}

%changelog
* Fri Nov 5 2010 Matthew Wall <nagiosgraph@sourceforge.net> 1.4.4-1
- refactor for use with new install script and latest fedora/redhat

* Wed Nov 11 2009 Craig Dunn <craig@craigdunn.org>
- action.gif renamed to nagiosgraph_action.gif to avoid package conflict with nagios

* Fri Nov 6 2009 Craig Dunn <craig@craigdunn.org>
- Fixed build root, paths and install command

* Tue Sep 23 2008 Alan Brenner <alan.brenner@ithaka.org>
- Initial spec.
