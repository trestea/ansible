#!/bin/bash
set -e
yum install -y gcc gcc-c++ make cmake automake autoconf gd file bison patch mlocate flex \
diffutils zlib zlib-devel pcre pcre-devel \
libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel libxml2 libxml2-devel \
glibc glibc-devel glib2 glib2-devel bzip2 bzip2-devel \
ncurses ncurses-devel curl curl-devel libcurl libcurl-devel e2fsprogs e2fsprogs-devel \
krb5 krb5-devel openssl openssl-devel \
openldap openldap-devel nss_ldap openldap-clients openldap-servers \
openldap-devellibxslt-devel kernel-devel libtool-libs \
readline-devel gettext-devel libcap-devel php-mcrypt libmcrypt libmcrypt-devel recode-devel mcrypt httpd httpd-devel

cp -frp /usr/lib64/libldap* /usr/lib/
if [ -f ./php-7.0.9.tar.gz ];then
tar xf php-7.0.9.tar.gz && cd php-7.0.9
fi
./configure \
--prefix=/data/php \
--with-config-file-path=/data/php/etc \
--with-mcrypt \
--with-mhash \
--with-mysqli=mysqlnd \
--with-pdo-mysql=mysqlnd \
--with-gd \
--with-iconv \
--with-zlib \
--with-curl \
--with-jpeg-dir \
--with-freetype-dir \
--with-apxs2=/usr/sbin/apxs \
--with-openssl \
--with-xmlrpc \
--with-bz2 \
--with-gettext \
--with-readline \
--with-recode \
--with-ldap \
--with-fpm-user=apache \
--with-fpm-group=apache \
--enable-fpm \
--enable-cgi \
--enable-xml \
--enable-bcmath \
--enable-inline-optimization \
--enable-mbregex \
--enable-mbstring \
--enable-ftp \
--enable-gd-native-ttf \
--enable-pcntl \
--enable-sockets \
--enable-sysvmsg \
--enable-sysvshm \
--enable-shmop \
--enable-zip \
--enable-soap \
--enable-session \
--enable-opcache \
--enable-cli
if [ $? == 0 ];then
  make && make install
else
  rm -rf php-7.0.9
fi