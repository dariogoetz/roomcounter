from typing import List, Optional
from pydantic import BaseModel

from roomcounter.schemas.permission import Permission as SchemaPermission
from roomcounter.models.user import PermissionType


class UserBase(BaseModel):
    username: str
    permissions: List[SchemaPermission]

    class Config:
        orm_mode = True


class User(UserBase):
    """
    User as it is retrieved from db (no password, permissions in db format)
    """
    id: int


class UserCreate(UserBase):
    """
    User to add to database (with password, permissions in convenient format)
    """
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    permissions: Optional[List[SchemaPermission]]


class AuthenticatedUser(BaseModel):
    id: int
    username: str
    permissions: List[PermissionType]
