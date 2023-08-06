#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: manage.py
# @time: 2018/6/19 9:51
# @Software: PyCharm

from apihelper.settings import Config, Urls
from sqlalchemy.ext.declarative import declarative_base  # db 基类
from sqlalchemy import Column, Integer, String, DateTime  # 相应的列
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session  # 执行的相关方法
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import create_engine
import tornado.ioloop
import tornado.web
import tornado.httpserver
import os
from apihelper.thirdparty.tornadows import webservices
import warnings
from apihelper.handlers import HelloWorldHandler

def make_app(urls=Urls):
    return tornado.web.Application(urls.urls, debug=Config.DEBUG)


def runserver(config=Config, urls=Urls, webservice=None):
    if webservice is None:
        assert urls
        app = make_app(urls)
    else:
        app = webservices.WebService(webservice)
    server = tornado.httpserver.HTTPServer(app)
    server.bind(port=config.PORT, address=config.HOST)
    server.start(num_processes=config.NUM_PROCESSES)  # forks one process per cpu
    tornado.ioloop.IOLoop.instance().start()


def run(config=Config, urls=Urls):
    warnings.warn("run is deprecated. Use replace_one, runserver instead.", DeprecationWarning, stacklevel=2)
    runserver(config, urls)


def migrate(config=Config, urls=Urls):

    # basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = config.get_DB_URI()
    # SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, config.DB_DATABASE)  # 设置数据库迁移保存的文件夹，用来sqlalchemymigrate

    db = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    Base = declarative_base()
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=db))

    Base.query = db_session.query_property()

    def isenit_db():
        Base.metadata.create_all(bind=db)

        # config.

def createsuperuser(config=Config, urls=Urls):
    pass


if __name__ == "__main__":
    class MConfig(Config):
        DB_DATABASE = 'test'
        PORT = 10020
        DB_PASSWORD = 'snowland.ltd'
    class MUrls(object):
        urls = [
            (r"/helloworld", HelloWorldHandler.HelloWorldHandler),
        ]
    runserver(config=MConfig, urls=MUrls)
    # migrate()
