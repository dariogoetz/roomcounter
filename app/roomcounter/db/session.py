# -*- coding: utf-8 -*-
"""
    Copyright (c) 2018 Dario Götz and Jörg Christian Reiher.
    All rights reserved.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, configure_mappers
import sqlalchemy.event as sqlevent

from roomcounter.core.config import settings


import logging
log = logging.getLogger(__name__)

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()


def get_engine(uri):
    """Get the sqlalchemy engine"""
    connect_args = {}
    if uri.startswith('sqlite'):
        connect_args["check_same_thread"] = False

    engine = create_engine(uri, connect_args=connect_args, pool_pre_ping=True)

    if uri.startswith('sqlite'):
        # ensure that cascaded deletion for foreign key constr. works in sqlite
        sqlevent.listen(
            engine, 'connect',
            lambda conn, rec: conn.execute('PRAGMA foreign_keys=ON;'))
    return engine


# initialize
engine = get_engine(settings.DB_URI)

# session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
