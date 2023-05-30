openssl req -new -sha256 -key $1 -extensions v3_req -config $2 -out $3 && \
cat $3 | base64 | xargs | tr -d ' '