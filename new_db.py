import csv
import mysql.connector
from config import DatabaseConfig
from config import FilesConfig
import configparser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine(
    "mysql+pymysql://{user}:{pw}@localhost/{db}?charset=utf8mb4".format(
        user=DatabaseConfig.user,
        pw=DatabaseConfig.passwd,
        db=DatabaseConfig.database,
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
        "substring_index(substring_index(substring_index"
        "(IPADD,'.',3),'.',-1),'.',-1) as c,"
        "substring_index(IPADD,'.',-1) as d, IPADD  from "
        + DatabaseConfig.Table_Name
        + " where Flag = 0 order by a+0,b+0,c+0,d+0;"
    )
    try:
        sql_results = cur.execute(sql)
        session.commit()
        sql_results = sql_results.fetchall()
        for element in sql_results:
            ip = element[4]  # getting only the IP address

            result = getUrlsIPBased(ip)
            for url in result:
                P_url = url[0]
                queue.append(P_url)
        return queue

    except Exception as e:
        pass
        # print(e)
        # print("############")
    # thread_initializer(queue)


# def sorting_score():
#     sql = ("select Score from " + DatabaseConfig.Table_Name + " order by Score DESC;")
#     try:
#         sql_results = cur.execute(sql)
#         session.commit()
#         sql_results = sql_results.fetchall()
#         for element in sql_results:
#             score = element[0]
#             result = getUrlsIPBased(score)
#             print(result)
#             for url in result:
#                 P_url = url[0]
#                 queue.append(P_url)
#                 print(queue)
#         return queue

#     except Exception as e:
#         pass


def update_hash(
    hash_x, url
):  # updating the hash value and its flag after it getting crawled.
    hash_x = hash_x
    url = url
    sql = (
        "update "
        + DatabaseConfig.Table_Name
        + " set H1 = %s, Flag = 1 where URLs = %s;"
    )
    cur.execute(sql, (hash_x, url))
    session.commit()


def update_score(scoreIS, sno):  # updating score of IS getting from bert
    score = scoreIS
    sno = sno
    cur.execute("update " + DatabaseConfig.Table_Name + " set Score = %s where SNO = %s;", (score, sno))
    session.commit()


def getUrlsIPBased(ip):  # fetching all the IP address already in DB
    sql = (
        "select distinct URLs from "
        + DatabaseConfig.Table_Name
        + " where IPADD = '"
        + ip
        + "' and Flag<>1;"
    )
    try:
        sql_results = cur.execute(sql)
        session.commit()
        sql_results = sql_results.fetchall()
        return sql_results
    except Exception as e:
        pass
        # print(e)
        # print("***********")


def seed_url_fetch():
    # Checking if there is already some URL's in DB.
    sql = (
        "select distinct substring_index(IPADD,'.',1) as a,\
          substring_index(substring_index(IPADD,'.',2),'.',-1) as b,"
        "substring_index(substring_index\
          (substring_index(IPADD,'.',3),'.',-1),'.',-1) as c,"
        "substring_index(IPADD,'.',-1) as d, IPADD,pid,urls from "
        + DatabaseConfig.Table_Name
        + " \
          where  Flag<>1 order by a+0,b+0,c+0,d+0 limit 1;"
    )
    result = cur.execute(sql)
    session.commit()
    result = result.fetchone()
    return result


def sno():
    sql = "select sno from " + DatabaseConfig.Table_Name + " ORDER BY SNO DESC LIMIT 1;"
    result = cur.execute(sql)
    session.commit()
    result = result.fetchone()
    return result