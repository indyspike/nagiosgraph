#!/usr/bin/perl

# License: OSI Artistic License
#          http://www.opensource.org/licenses/artistic-license-2.0.php
# Author:  (c) 2005 Soren Dossing
# Author:  (c) 2008 Alan Brenner, Ithaka Harbors
# Author:  (c) 2010 Matthew Wall

# The configuration file and ngshared.pm must be in this directory.
# So take note upgraders, there is no $configfile = '....' line anymore.
use lib '/opt/nagiosgraph/etc';

# Main program - change nothing below

use ngshared;
use CGI;
use File::Find;
use English qw(-no_match_vars);
use RRDs;
use strict;
use warnings;

readconfig('read');
if (defined $Config{ngshared}) {
    debug(DBCRT, $Config{ngshared});
    htmlerror($Config{ngshared});
    exit;
}

my $cgi = new CGI;  ## no critic (ProhibitIndirectSyntax)
$cgi->autoEscape(0);

my $params = getparams($cgi);
getdebug('show', $params->{host}, $params->{service});

dumper(DBDEB, 'config', \%Config);
dumper(DBDEB, 'params', $params);

my $host = q();
if ($params->{host}) { $host = $params->{host}; }
my $service = q();
if ($params->{service}) { $service = $params->{service}; }

my $periods = getperiods('timeall', $params->{period});

my @style;
if ($Config{stylesheet}) {
    @style = (-style => {-src => "$Config{stylesheet}"});
}
my $hurl = $Config{nagiosgraphcgiurl} . '/showhost.cgi?host=' .
    $cgi->escape($host);
my $surl = $Config{nagiosgraphcgiurl} . '/showservice.cgi?service=' .
    $cgi->escape($service);
my $refresh = (defined $Config{refresh})
    ? $cgi->meta({ -http_equiv => 'Refresh', -content => "$Config{refresh}" })
    : q();
my $ngtitle = (defined $Config{hidengtitle} and $Config{hidengtitle} eq 'true')
    ? q() : $cgi->h1('Nagiosgraph');

cfgparams($params, $params, $service);

# Draw the full page
print $cgi->header,
    $cgi->start_html(-id => 'nagiosgraph',
                     -title => "nagiosgraph: $host - $service",
                     -head => $refresh,
                     @style) . "\n" .
    printnavmenu($cgi, $host, $service, $cgi->remote_user(), $params) .
    $cgi->br({-clear=>'all'}) . "\n" .
    $ngtitle .
    $cgi->p(trans('perfforhost') . q( ) .
            $cgi->span({-class=>'item_label'},
                       $cgi->a({href => $hurl}, $host)) . ', ' .
            trans('service') . q( ) .
            $cgi->span({-class=>'item_label'},
                       $cgi->a({href => $surl}, $service)) . q( ) .
            trans('asof') . q( ) .
            $cgi->span({-class=>'timestamp'},scalar localtime)
            ) . "\n" or
    debug(DBCRT, "error sending HTML to web server: $OS_ERROR");

my $now = time;
for my $period (graphsizes($periods)) {
    my $str = printgraphlinks($cgi, $params, $period);
    print printperiodlinks($cgi, $params, $period, $now, $str);
}

print printscript('both', $host, $service);

print printfooter($cgi) or
    debug(DBCRT, "error sending HTML to web server: $OS_ERROR");

__END__

=head1 NAME

show.cgi - Graph Nagios data

=head1 DESCRIPTION

Run this via a web server to generate a page of graph data.

=head1 USAGE

B<show.cgi>

=head1 CONFIGURATION

The B<nagiosgraph.conf> file controls the behavior of this script.

=head1 OPTIONS

host=host_name

service=service_name

period=(day week month quarter year)

=head1 DIAGNOSTICS

Use the debug_show setting from B<nagiosgraph.conf> to control the amount
of debug information that will be emitted by this script.  Debug output will
go to the web server error log.

=head1 DEPENDENCIES

=over 4

=item B<showgraph.cgi>

This generates the graphs shown in the HTML generated here.

=item B<Nagios>

While this could probably run without Nagios, as long as RRD databases exist,
it is intended to work along side Nagios.

=item B<rrdtool>

This provides the data storage and graphing system.

=item B<RRDs>

This provides the perl interface to rrdtool.

=back

=head1 INSTALLATION

Copy this file into Nagios' cgi directory (for the Apache web server, see where
the ScriptAlias for /nagios/cgi-bin points), and make sure it is executable by
the web server.

Install the B<ngshared.pm> file and edit this file to change the B<use lib>
line to point to the directory containing B<ngshared.pm>.

Create or edit the example B<nagiosgraph.conf>, which must reside in the same
directory as B<ngshared.pm>.

To link a web page generated by this script from Nagios, add definitions like:

=over 4

define serviceextinfo {
 service_description Current Load
 host_name           host1, host2
 action_url          show.cgi?host=$HOSTNAME$&service=$SERVICEDESC$
}

=back

to the Nagios configuration file(s). The service_description must match an
existing service. Only the hosts listed in host_name will have an action icon
next to the service name on a detail page.

Copy the images/action.gif file to the nagios/images directory, if desired.

=head1 SEE ALSO

B<nagiosgraph.conf> B<showhost.cgi> B<showservice.cgi> B<showgraph.cgi> B<ngshared.pm>

=head1 AUTHOR

Soren Dossing, the original author in 2005.

Alan Brenner - alan.brenner@ithaka.org; I've updated this from the version
at http://nagiosgraph.wiki.sourceforge.net/ by moving some subroutines into a
shared file (ngshared.pm), adding color number nine, and adding support for
showhost.cgi and showservice.cgi.

Craig Dunn: support for service based graph options via rrdopts.conf file

Matthew Wall, added features, bug fixes and refactoring in 2010.

=head1 LICENSE AND COPYRIGHT

Copyright (C) 2005 Soren Dossing, 2008 Ithaka Harbors, Inc.

This program is free software; you can redistribute it and/or modify it
under the terms of the OSI Artistic License:
http://www.opensource.org/licenses/artistic-license-2.0.php

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.
