#!/bin/sh
# install soft for MacOSX Sierra

#install pcre
tar -zxvf pcre-8.41.tar.gz
cd pcre-8.5
sudo ./configure --prefix=/usr/local
sudo make
sudo make install

#install openSSL
tar -zxvf tar -zxvf openssl-1.0.2l.tar.gz
cd openssl-1.0.2l
sudo ./config --prefix=/usr/local
sudo make
sudo make install

#安装nignx
#brew search nginx
#brew install nginx
#或者还有其他的方法安装Nginx
wget http://nginx.org/download/nginx-1.12.1.tar.gz
tar -zxvf nginx-1.12.1.tar.gz
cd nginx
sudo ./configure --prefix=/usr/local/nginx --with-http_ssl_module --with-cc-opt="-Wno-deprecated-declarations" --with-openssl=/usr/l
ocal/openssl-1.0.2l
sudo ln -s /usr/local/nginx/sbin/nginx /usr/sbin/nginx
