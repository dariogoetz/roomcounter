from pydantic import BaseModel
from roomcounter.models.user import PermissionType


class Permission(BaseModel):
    permission: PermissionType

    class Config:
        orm_mode = True


class PermissionInternal(Permission):
    id: int
    user_id: int
