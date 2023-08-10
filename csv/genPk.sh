openssl ecparam -name secp256k1 -genkey -noout -out $1 && \
cat $1 | base64 | xargs | tr -d ' '