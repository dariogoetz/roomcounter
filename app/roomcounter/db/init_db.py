from sqlalchemy.orm import Session

from roomcounter.db.session import engine, SessionLocal
from roomcounter.db.base_class import Base
from roomcounter.core.config import settings
from roomcounter.crud import crud_user, crud_room
from roomcounter.schemas import user as schema_user, room as schema_room
from roomcounter.schemas.permission import Permission as SchemaPermission
from roomcounter.models.user import PermissionType

import logging
log = logging.getLogger(__name__)


# database initialization functions
def initialize_sql():
    """
    Initializes database corresponding to models in sqlalchemy_orm_objects.
    A one-time session is created for this.
    """
    # make a session only for table creation
    while True:
        try:
            Base.metadata.bind = engine
            Base.metadata.create_all(engine)
            break
        except Exception as e:
            log.warning(
                'No database connection possible (error: %s). Sleeping for 5 sec.',
                e)
            import time
            time.sleep(5)


def initialize_default_user(session: Session):
    users = crud_user.get_users(session)
    if not users:
        user = schema_user.UserCreate(
            username=settings.INITIAL_USER,
            password=settings.INITIAL_PASSWORD,
            permissions=[SchemaPermission(permission=PermissionType.admin)]
        )
        crud_user.register_user(db=session, user=user)
        log.info('Initializing default user "%s"', settings.INITIAL_USER)


def initialize_default_room(session: Session):
    rooms = crud_room.get_rooms(session)
    if not rooms:
        room = schema_room.RoomCreate(
            name=settings.INITIAL_ROOM_NAME,
            capacity=0,
        )
        crud_room.add_room(db=session, room=room)
        log.info('Initializing default room "%s"', settings.INITIAL_ROOM_NAME)


def init_database():
    session = SessionLocal()
    initialize_sql()
    initialize_default_user(session)
    initialize_default_room(session)
