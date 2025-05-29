import os
import jwt
from jwt import InvalidTokenError

SECRET_KEY = os.environ.get("JWT_SECRET", "secret")
ALGORITHM = "HS256"


def verify_token(token: str) -> bool:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except InvalidTokenError:
        return False
