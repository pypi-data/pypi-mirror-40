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
from migrate.versioning import api
import os.path
import datetime


Base = None

def make_app(config=Config, urls=Urls):
    return tornado.web.Application(urls.urls, debug=config.DEBUG)

def isenit_db(Base, db):
    Base.metadata.create_all(bind=db)

def runserver(config=Config, urls=Urls, webservice=None):
    """
    运行
    :param config:
    :param urls:
    :param webservice:
    :return:
    """
    if webservice is None:
        assert urls
        app = make_app(config, urls)
    else:
        app = webservices.WebService(webservice)
    server = tornado.httpserver.HTTPServer(app)
    server.bind(port=config.PORT, address=config.HOST)
    server.start(num_processes=config.NUM_PROCESSES)  # forks one process per cpu
    print('''
    {}
    snowland-apihelper version {}, using settings {}
    Starting development server at {}://{}:{}
    '''.format(datetime.datetime.now(), apihelper.__VERSION__, config.NAME, config.PREFIX, config.HOST, config.PORT))
    tornado.ioloop.IOLoop.instance().start()


def run(config=Config, urls=Urls):
    warnings.warn("run is deprecated. Use replace_one, runserver instead.", DeprecationWarning, stacklevel=2)
    runserver(config, urls)


def makemigrations(config=Config):

    db = create_engine(config.get_DB_URI(), echo=True)

    Base = declarative_base()
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=db))

    Base.query = db_session.query_property()

    Base.metadata.create_all(bind=db)

    if not os.path.exists(config.SQLALCHEMY_MIGRATE_REPO):
        api.create(config.SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(config.set_DB_URI(), config.SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(config.get_DB_URI(), config.SQLALCHEMY_MIGRATE_REPO, api.version(config.SQLALCHEMY_MIGRATE_REPO))


def migrate(config=Config):

    migration = config.SQLALCHEMY_MIGRATE_REPO + '/versions/d_migration.py' % (
                api.db_version(config.get_DB_URI(), config.SQLALCHEMY_MIGRATE_REPO) + 1)
    tmp_module = __import__('old_model')
    old_model = api.create_model(config.get_DB_URI(), config.SQLALCHEMY_MIGRATE_REPO)
    exec(old_model in tmp_module.__dict__)
    script = api.make_update_script_for_model(config.get_DB_URI(), config.SQLALCHEMY_MIGRATE_REPO, tmp_module.meta,
                                              Base.metadata)
    with open(migration, 'wt') as f:
        f.write(script)
    api.upgrade(config.get_DB_URI(), config.SQLALCHEMY_MIGRATE_REPO)
    print('New migration saved as ' + migration)
    print('Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)))




def createsuperuser(config=Config, urls=Urls):
    raise NotImplementedError


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
