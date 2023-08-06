#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: settings.py
# @time: 2018/9/8 0:53
# @Software: PyCharm

import os
from apihelper.handlers import HelloWorldHandler
from sqlalchemy.ext.declarative import declarative_base  # db 基类
from sqlalchemy import Column, Integer, String, DateTime  # 相应的列
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session  # 执行的相关方法
from sqlalchemy.dialects.mysql import LONGTEXT

# DEFAULT_DATABASES_MYSQL = {
#     'ENGINE': 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
#         DB_USERNAME,
#         DB_PASSWORD,
#         DB_HOST,
#         DB_PORT,
#         DB_DATABASE
#     )
# }


class Config(object):
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 80
    NUM_PROCESSES = 1

    _APP_NAME = ''
    _DB_URI = ''

    @classmethod
    def get_APP_NAME(cls):
        cls.set_APP_NAME()
        return cls._APP_NAME


    @classmethod
    def set_APP_NAME(cls, app_name='snowland'):
        cls._APP_NAME = app_name
        cls.DB_PREFIX = app_name + '_'
    NAME = 'APIHELPER'
    PREFIX = 'http'
    DB_DRIVER = 'mysql+pymysql'
    DB_USERNAME = 'root'
    DB_PASSWORD = 'root'
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_DATABASE = ''
    DB_PREFIX = _APP_NAME + '_'
    DB_MIGRATE_REPO = _APP_NAME + '/'
    __basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_MIGRATE_REPO = os.path.join(__basedir, _APP_NAME)  # 设置数据库迁移保存的文件夹，用来sqlalchemymigrate

    @classmethod
    def set_DB_URI(cls):
        cls._DB_URI = '%s://%s:%s@%s:%d/%s' \
            % (cls.DB_DRIVER, cls.DB_USERNAME, cls.DB_PASSWORD, cls.DB_HOST, cls.DB_PORT, cls.DB_DATABASE)

    @classmethod
    def get_DB_URI(cls):
        cls.set_DB_URI()
        return cls._DB_URI


class Urls(object):
    urls = [
        (r"/", HelloWorldHandler.HelloWorldHandler),
    ]
