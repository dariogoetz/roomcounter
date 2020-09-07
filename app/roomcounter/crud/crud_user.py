from sqlalchemy.orm import Session
from typing import List, Optional

from roomcounter.schemas.permission import Permission as SchemaPermission
from roomcounter.schemas.user import UserCreate as SchemaUserCreate
from roomcounter.models.user import User, Permission, PermissionType
from roomcounter.core import security

import logging
log = logging.getLogger(__name__)


def get_users(db: Session):
    '''
    Get a list of all users.
    '''
    users = db.query(User).all()
    return users


def get_user_by_id(db: Session, uid: int):
    '''
    Get all info for a user.
    If the user is not logged in, "None" is returned.
    '''
    if uid is None:
        return None
    return db.query(
        User).filter(User.id == uid).first()


def get_user(db: Session, username: str):
    '''
    Get all info for a user.
    If the user is not logged in, "None" is returned.
    '''
    if username is None:
        return None
    return db.query(
        User).filter(User.username == username).first()


def rename_user(db: Session, uid: int, username: str):
    user = db.query(
        User).filter(User.id == uid).first()
    if user is None:
        return None
    new_user = db.query(
        User).filter(User.username == username).first()
    if username is None or new_user is not None:
        return None

    user.username = username
    db.add(user)
    return True


def get_groups(db: Session, uid: int):
    '''
    Get the roles for a userself.
    If the user does not exist, returns None.
    '''
    user = db.query(
        User).filter(User.id == uid).first()
    if user is None:
        return None
    return [str(p.permission.name) for p in user.permissions]


def set_groups(db: Session, uid: int, groups: List[SchemaPermission]):
    user = db.query(
        User).filter(User.id == uid).first()
    if user is None:
        return None
    user.permissions = groups
    return True


def set_password(db: Session, uid: int, password: str):
    user = db.query(
        User).filter(User.id == uid).first()
    if user is None:
        return None
    user.password_hash = security.generate_hashed_pw(password)
    db.commit()
    return True


def verify_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not security.verify_password(password, user.password_hash):
        return False
    return user


def register_user(db: Session,
                  user: SchemaUserCreate,
                  uid: Optional[int] = None,
                  put: bool = False):

    target_permissions = sorted([p.permission for p in user.permissions or []])
    if not db.query(User.id).count():
        # first registered user is admin
        target_permissions = sorted(set(target_permissions)
                                    | set([PermissionType.admin]))

    password_hash = None
    if user.password is not None:
        password_hash = security.generate_hashed_pw(user.password)
    if uid is not None:
        # update existing user
        db_user = get_user_by_id(db, uid)
        if put:
            db_user.username = None
            db_user.first_name = None
            db_user.last_name = None
            db_user.additional_info = None
            db_user.permissions = []
    else:
        # new user
        db_user = User()
    existing_permissions = {p.permission for p in db_user.permissions}

    for key, val in user.dict().items():
        if key in ["permissions", "password"]:
            continue
        if val is None:
            continue
        setattr(db_user, key, val)

    if password_hash is not None:
        db_user.password_hash = password_hash

    db.add(db_user)
    db.flush()

    for permission in target_permissions:
        if permission in existing_permissions:
            continue
        p = Permission(user_id=db_user.id, permission=permission)
        db.add(p)

    db.commit()
    db.flush()
    return db_user


def set_name(db: Session, uid: int, first_name: str, last_name: str):
    user = db.query(
        User).filter(User.id == uid).first()
    if user is None:
        return True
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    db.add(user)
    return True


def delete_user(db: Session, uid: int):
    user = db.query(
        User).filter(User.id == uid).first()
    if user is None:
        return True
    db.delete(user)
    return True
