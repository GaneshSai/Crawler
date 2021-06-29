import csv
from config import FilesConfig
import configparser
import time
import sys
from mongo_db import *

def data_to_csv():
    try:
        insertion()
    except:
        pass

def main_csv():
    while True:  # Running the code after every 10 sec so that it doesn't stop.
        data_to_csv()
        f = open("Urls.csv", "w")
        f.truncate()
        f.close()
        time.sleep(10)