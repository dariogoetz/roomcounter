from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import jwt

from roomcounter.db.session import SessionLocal
from roomcounter.core.cookie_token import OAuth2PasswordBearerCookie
from roomcounter.core import security
from roomcounter.core.config import settings
from roomcounter.schemas.token import TokenData
from roomcounter.schemas.user import AuthenticatedUser
from roomcounter.models.user import PermissionType

oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="auth/login",
                                           auto_error=False)


def db():
    db = SessionLocal()

    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


def optional_user(token: Optional[str] = Depends(oauth2_scheme)):
    if token is None:
        return None

    try:
        payload = jwt.decode(token,
                             settings.SECRET_KEY,
                             algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        permissions: str = payload.get("permissions", [])
        id: int = payload.get("id")
        if username is None:
            return None

        token_data = TokenData(username=username,
                               permissions=permissions,
                               id=id)
    except jwt.JWTError:
        return None

    # do not hit db again for user details, take directly from token
    # user = crud_users.get_user(username)
    user = AuthenticatedUser(**token_data.dict())
    return user


def authenticated_user(
        user: Optional[AuthenticatedUser] = Depends(optional_user)):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def admin(user: AuthenticatedUser = Depends(authenticated_user)):
    if PermissionType.admin in user.permissions:
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Only admin allowed")
