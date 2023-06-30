Generate secret_key
$ openssl rand -hex 32


$ python
>>> import secrets
>>> secrets.token_hex(32)