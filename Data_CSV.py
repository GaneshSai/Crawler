import csv
import mysql.connector
from config import DatabaseConfig
from config import FilesConfig
import configparser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import time


def data_to_csv():
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
    with open(
        "Urls.csv"
    ) as csv_file:
        csv_data = csv.DictReader(csv_file)
        for row in csv_data:
            print(row)
            cur.execute(
                "INSERT INTO Information_Security1(SNO, PID, URLs, IPAdd, Flag, H1) VALUES ('{sno}', '{pid}', '{urls}', '{ipadd}', '{flag}', '{hash}')".format(
                    sno=col[0],
                    pid=col[1],
                    urls=col[2],
                    ipadd=col[4],
                    flag=col[5],
                    hash=col[6],
                )
            )
            cur.execute("update Information_Security1 set H1 = NULL where H1 = ''")
            # close the connection to the database.
        cur.close()
        print("Done")


while True:
    data_to_csv()
    f = open("Urls.csv", "w")
    f.truncate()
    f.close()
    time.sleep(10)
