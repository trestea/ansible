#!/bin/bash
make distclean
./configure --with-apr=/usr/bin/apr-1-config --with-java-home=/usr/local/jdk1.7.0_76
make && make install
if [ -z "`grep "TOMCAT1_HOME" /etc/profile`" ];then
echo -e '
####tomcat1
TOMCAT1_HOME=/data/tomcat1
CATALINA1_HOME=/data/tomcat1
CATALINA1_BASE=/data/tomcat1
export  TOMCAT1_HOME  CATALINA1_HOME CATALINA1_BASE
####tomcat2
TOMCAT2_HOME=/data/tomcat2
CATALINA2_HOME=/data/tomcat2
CATALINA2_BASE=/data/tomcat2
export  TOMCAT2_HOME  CATALINA2_HOME CATALINA2_BASE
####tomcat3
TOMCAT3_HOME=/data/tomcat3
CATALINA3_HOME=/data/tomcat3
CATALINA3_BASE=/data/tomcat3
export  TOMCAT3_HOME  CATALINA3_HOME CATALINA3_BASE
####tomcat4
TOMCAT4_HOME=/data/tomcat4
CATALINA4_HOME=/data/tomcat4
CATALINA4_BASE=/data/tomcat4
export  TOMCAT4_HOME  CATALINA4_HOME CATALINA4_BASE
####apr
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/apr/lib' >> /etc/profile
fi