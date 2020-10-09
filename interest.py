import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px
import pymysql.cursors
from sqlalchemy import create_engine, exc


# Set desired number of cycles (for easy testing)
numofcycles = 10


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

def retrieve_keyword():
    with connection.cursor() as cursor: 
            # Read a single record
            sqlselect = "SELECT topic_title FROM pandas_temp WHERE interest IS NULL ORDER BY 'id' DESC LIMIT 1;"
            cursor.execute(sqlselect)
            # Returns a list of key:value dicts with 'topic_title':keyword
            listofdicts = cursor.fetchall()
            # Turns list of dict into a single-item list
            resultlist = [f['topic_title'] for f in listofdicts]
            connection.commit()
            return resultlist


def find_interest():
    singlekeywordlist = retrieve_keyword()
    keyword = str(singlekeywordlist[0])
    print("Keyword type is: ",type(keyword), "Keyword is: ", keyword)

    time.sleep(3)
    pytrends.build_payload(kw_list=singlekeywordlist, timeframe='all', geo='CA')
    print("Commencing interest_over_time search...")
    interest_over_time_df = pytrends.interest_over_time()
    #Don't care about the isPartial column - dropping it
    df = interest_over_time_df.drop(columns=['isPartial'])
    print(df.tail())
    keywordattr = getattr(df, keyword)

    interest_dict = dict(zip(df.index, keywordattr))

    interest_data_insert = "UPDATE pandas_temp SET interest=\"%s\" WHERE topic_title = \"%s\"" % (interest_dict,keyword)
    with connection.cursor() as cursor: 
        cursor.execute(interest_data_insert)
        print("Execute finished!")
        connection.commit()
        connection.close()

if __name__ =='__main__':
    print("Number of Cycles to run: ", str(numofcycles))
    find_interest()