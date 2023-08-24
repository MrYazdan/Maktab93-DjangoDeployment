#!/bin/bash

set -e

mkdir -p /var/log/nginx/api

echo "Checking for dhparams.pem"
if [ ! -f "/vol/proxy/ssl-dhparams.pem" ]; then
  echo "dhparams.pem does not exist ! - Creating ..."
  openssl dhparam -out /vol/proxy/ssl-dhparams.pem 1024
fi

echo "Checking for fullchain.pem"
if [ ! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]; then
  echo "No SSL cert, enabling HTTP only..."
  envsubst '\$DOMAIN' < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
else
  echo "SSL cert exists, enabling HTTPS..."
  envsubst '\$DOMAIN' < /etc/nginx/default-ssl.conf.tpl > /etc/nginx/conf.d/default.conf
fi
nginx-debug -g 'daemon off;'