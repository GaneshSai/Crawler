import pymongo
from pymongo import MongoClient
import csv
import json
import pandas as pd
import sys
from config import FilesConfig

client = MongoClient("localhost", 27017, username="Ganesh", password="Siren@123",)
db = client["Siren"]
# collection_name = "Information_Security"
db_cm = db["Information_Security"]
urls = []


def insertion():
    csvfile = open(FilesConfig.csv_file_name + "Urls.csv", "r")
    data = pd.read_csv(csvfile)
    data_json = json.loads(data.to_json(orient="records"))
    db_cm.insert_many(data_json)


def update_hash():
    with open("Urls.csv") as csv_file:
        csv_data = csv.reader(csv_file)
        for row in csv_data:
            url = row[2]
            url = str(url)
            hash_x = row[5]
            myquery = {"URLs": url}
            newvalues = {"$set": {"Flag": 1, "Hash Value": hash_x}}
            db_cm.update_one(myquery, newvalues)


def sno():
    sno = db_cm.find().sort("Sno", -1).limit(1)
    for x in sno:
        first, second, *_ = x.values()
        return second


def sorting_ip():
    flag = {"Flag": 0}
    mydoc = db_cm.find(flag, sort=[("IP Address", -1)])
    for x in mydoc:
        id_val, sno, pid, url, *_ = x.values()
        urls.append(url)
    return urls


def seed_url_fetch():
    flag = {"Flag": 0}
    mydoc = db_cm.find_one(flag, sort=[("IP Address", -1)])
    if mydoc is None:
        return None
    else:
        id_val, sno, pid, url, *_ = mydoc.values()
        return url
