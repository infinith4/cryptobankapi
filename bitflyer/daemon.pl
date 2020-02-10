#!/usr/bin/perl
use strict;
use warnings;

#Remind Bookmark
#This script is send mail from DB.

my @command = ('python', 'checkinfo.py');
my $sleeptime = 10;
print sprintf("%d秒間隔で実行\r\n", $sleeptime);

while(1){
  print "start\r\n";
  my $ret = system @command;
  if ($ret != 0) {
    print "code[$ret]\n";
  }
  print sprintf("end. Wait %d seconds\r\n",$sleeptime);
  sleep($sleeptime);
}
