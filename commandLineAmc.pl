use Getopt::ArgParse;
use 5.010;

$ap = Getopt::ArgParse->new_parser(
  prog => 'command line access amc', 
  description => 'use some of the options below', 
  epilog => 'This appears at the bottom of usage');

#Quantidade de provas para serem geradas
$ap->add_arg('--tests', '-t', required => 1, default => 0, help => 'Quantidade de provas');
  
# $ns is also accessible via $ap->namespace
$ns = $ap->parse_args();


say $ns->tests;
