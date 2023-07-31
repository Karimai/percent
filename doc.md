Generate secret_key
$ openssl rand -hex 32


$ python
>>> import secrets
>>> secrets.token_hex(32)
> 
> 

docker build --tag karimmoradi/percent:1.0.0 .
docker push karimmoradi/percent:1.0.0
