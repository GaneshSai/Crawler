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
    with open("Urls.csv") as csv_file:
        csv_data = csv.reader(csv_file)
        for row in csv_data:
            cur.execute(
                "INSERT INTO "
                + DatabaseConfig.Table_Name
                + "(SNO, PID, URLs, IPAdd, Flag, H1) VALUES (%s, %s, %s, %s, %s, %s)",
                row)
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
