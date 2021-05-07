import csv
import mysql.connector
from config import DatabaseConfig
from config import FilesConfig
import configparser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import time
from new_db import update


def data_to_csv():
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
    with open("Urls.csv") as csv_file:
        csv_data = csv.reader(csv_file)
        for row in csv_data:
            url = row[2]
            url = str(url)
            hash_x = row[5]
            update(hash_x, url)
            result = cur.execute("SELECT * FROM " + DatabaseConfig.Table_Name + " WHERE URLs=%s", (url,))
            if result.fetchone() is None:
                print(row)
                sql = (
                    "INSERT INTO "
                    + DatabaseConfig.Table_Name
                    + "(SNO, PID, URLs, IPAdd, Flag, H1) VALUES (%s, %s, %s, %s, %s, %s)")
                cur.execute(sql, row)
                cur.execute("update Information_Security1 set H1 = NULL where H1 = '';")
                session.commit()
                # close the connection to the database.
            else :
                pass
        cur.close()
        print("Done")



while True:
    data_to_csv()
    f = open("Urls.csv", "w")
    f.truncate()
    f.close()
    time.sleep(10)
