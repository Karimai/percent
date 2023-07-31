import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import jwt

load_dotenv()


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(
        minutes=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(
        to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )

    return encoded_jwt
