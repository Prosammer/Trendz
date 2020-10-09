import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px
import pymysql.cursors
from sqlalchemy import create_engine, exc


# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=-240,retries=2,backoff_factor=0.2,)



# Connect to the database

connection = pymysql.connect(host='localhost',
user='root',
password='***REMOVED***',
db='trends',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)


# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
.format(user="root",
pw="***REMOVED***",
db="trends"))

def retrieve_keyword(keyword):
    with connection.cursor() as cursor: 
            # Read a single record
            sqlselect = "SELECT topic_title FROM keywords WHERE interest IS NULL ORDER BY 'id' DESC LIMIT 1;"
            cursor.execute(sqlselect)
            # Returns a list of key:value dicts with 'topic_title':keyword
            listofdicts = cursor.fetchall()
            # Turns list of dict into a single-item list
            resultlist = [f['topic_title'] for f in listofdicts]
            cursor.execute()
            connection.commit()
            return resultlist


def find_interest(keyword):
    keyword_list = retrieve_keyword(keyword)
    pytrends.build_payload(kw_list=keyword_list, timeframe='today 3-m', geo='CA')
    print("Commencing interest_over_time search...")
    interest_over_time_df = pytrends.interest_over_time()
    print(interest_over_time_df.head())


if __name__ =='__main__':
    
    print("Number of Cycles to run: ", str(numofcycles))