#!/bin/bash
make distclean
./configure --with-apr=/usr/bin/apr-1-config --with-java-home=/usr/local/jdk1.7.0_80
make && make install
if [ -z "`grep "TOMCAT1_HOME" /etc/profile`" ];then
echo -e '
####tomcat1
TOMCAT1_HOME=/data/tomcat1
CATALINA1_HOME=/data/tomcat1
CATALINA1_BASE=/data/tomcat1
export  TOMCAT1_HOME  CATALINA1_HOME CATALINA1_BASE
####apr
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/apr/lib' >> /etc/profile
fi
