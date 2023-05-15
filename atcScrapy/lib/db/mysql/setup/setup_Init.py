import json
import os

import mysql.connector
from aws_lambda_powertools.utilities import parameters
from mysql.connector import errorcode

def initDBConnection():

    DB_SECRET = json.loads(parameters.get_secret("ATC_DB_Credentials"))
    DB_USER = DB_SECRET["username"]
    DB_PASSWORD = DB_SECRET["password"]
    DB_ENDPOINT = os.getenv("DB_ENDPOINT")
    DB_NAME = os.getenv("DB_NAME")

    try:
        dbConnection = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_ENDPOINT,
            database=DB_NAME
        )
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        raise Exception("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        raise Exception("Database does not exist")
      else:
        raise Exception(err)
    else:
        return dbConnection

def getCursor(dbConnection, dictionary=True, buffered=True):
    return dbConnection.cursor(dictionary=dictionary, buffered=buffered)