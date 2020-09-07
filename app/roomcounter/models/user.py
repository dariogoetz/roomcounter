# -*- coding: utf-8 -*-
"""
    Copyright (c) 2020 Dario Götz.
    All rights reserved.
"""
import enum

from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from roomcounter.db.base_class import Base


class PermissionType(str, enum.Enum):
    admin = 'admin'


class User(Base):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    permissions = relationship('Permission',
                               backref='user',
                               cascade='all, delete-orphan')


class Permission(Base):

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    permission = Column(Enum(PermissionType), nullable=False)
