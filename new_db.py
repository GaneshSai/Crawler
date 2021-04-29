import csv
import mysql.connector
from config import DatabaseConfig
from config import FilesConfig
import configparser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# from newcrawler import *

# print("newdb")
engine = create_engine(
    "mysql+pymysql://{user}:{pw}@localhost/{db}".format(
        user=DatabaseConfig.user,
        pw=DatabaseConfig.passwd,
        db=DatabaseConfig.database,
        pool_recycle=3600,
    )
)

Session = sessionmaker(bind=engine)
session = Session()
cur = engine.connect()

queue = []


def sorting_ip():  # Sorting IP in form of ascending order
    sql = (
        "select distinct substring_index(IPADD,'.',1) as a,"
        "substring_index(substring_index(IPADD,'.',2),'.',-1) as b,"
        "substring_index(substring_index(substring_index\
          (IPADD,'.',3),'.',-1),'.',-1) as c,"
        "substring_index(IPADD,'.',-1) as d, IPADD  from "
        + DatabaseConfig.Table_Name
        + " where Flag = 0 order by a+0,b+0,c+0,d+0;"
    )
    try:
        sql_results = cur.execute(sql)
        session.commit()
        sql_results = sql_results.fetchall()
        for element in sql_results:
            ip = element[4]
            result = getUrlsIPBased(ip)
            for url in result:
                P_url = url[0]
                queue.append(P_url)
        return queue

    except Exception as e:
        print(e)
        print("############")
    # thread_initializer(queue)


def getUrlsIPBased(ip):  # fetching all the IP address already in DB
    sql = (
        "select distinct URLs,IPADD  from "
        + DatabaseConfig.Table_Name
        + " \
    where IPADD='"
        + ip
        + "' and Flag !=1;"
    )
    try:
        sql_results = cur.execute(sql)
        session.commit()
        sql_results = sql_results.fetchall()
        return sql_results
    except Exception as e:
        print(e)
        print("***********")