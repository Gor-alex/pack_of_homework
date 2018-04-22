# coding=utf-8
# -*- coding: utf-8 -*-
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DataBase(object):
    '''

        Class for interaction with database

    '''

    DB_URL = 'postgresql://{user}:{password}@{postgre_server}:{bd_port}/{bd_name}'.format(
        user='postgres',
        postgre_server='localhost',
        bd_port='5432',
        password='11111111',
        bd_name='tweet'
    )

    def __init__(self, url=None):
        self.engine = create_engine(url if url is not None else self.DB_URL, echo=False)

    def new_session(self):
        return sessionmaker(bind=self.engine)()