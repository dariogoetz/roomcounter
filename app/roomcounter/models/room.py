# -*- coding: utf-8 -*-
"""
    Copyright (c) 2020 Dario Götz.
    All rights reserved.
"""

from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from roomcounter.db.base_class import Base


class Room(Base):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer)
    utilization = Column(Integer)


class Door(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)

    left_room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    left_room = relationship("Room", foreign_keys=left_room_id)

    right_room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    right_room = relationship("Room", foreign_keys=right_room_id)
