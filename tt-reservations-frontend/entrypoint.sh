#! /bin/sh

if [ -n "$SSL_CERT" ] && [ -n "$SSL_KEY" ]; then
    echo "Using SSL"
    ng serve --host 0.0.0.0 --ssl --ssl-cert "$SSL_CERT" --ssl-key "$SSL_KEY"
else
    echo "Please use SSL in future"
    ng serve --host 0.0.0.0
fi