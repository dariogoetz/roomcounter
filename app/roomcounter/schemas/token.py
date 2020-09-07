from typing import Optional, List
from pydantic import BaseModel

from roomcounter.models.user import PermissionType


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    permissions: Optional[List[PermissionType]] = None
