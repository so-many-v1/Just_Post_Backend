import bcrypt
from jwt import encode, decode

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session
from database.models import Users

from config import pub_key, private_key

class AuthError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


def encode_jwt(payload):
    encoded = encode(payload=payload, key=private_key, algorithm="RS256")
    return encoded

def decode_jwt(payload):
    decoded = decode(jwt=payload, key=pub_key, algorithms=["RS256"])
    return decoded

def password_to_hashed(password) -> bytes:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=password.encode('utf-8'), salt=salt)
    return hashed_password.decode("utf-8")

def validate_password(hashed_password:str, password:str) -> bool:
    is_valid = bcrypt.checkpw(password=password.encode("utf-8"), hashed_password=hashed_password.encode("utf-8"))
    return is_valid


async def get_current_user(
        cred: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        session:AsyncSession = Depends(get_async_session)
):
    try:
        jwt_data = decode_jwt(payload=cred.credentials)
        sub = jwt_data["sub"]

        if not sub:
            raise AuthError("Missing SUB in JWT.")

        user = await session.get(Users, int(sub))

        if not user:
            raise AuthError("User not found.")

        return user
    except AuthError as e:
        print(e)
        HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Auth Error"
        )


