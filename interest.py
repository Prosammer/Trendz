import pandas as pd
import os,sys,requests,time,operator,logging
from pytrends.request import TrendReq
import plotly.express as px
import pymysql.cursors


# Set desired number of cycles (for easy testing)
numofcycles = 800


# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=-240,retries=2,backoff_factor=0.2)



# Connect to the database

connection = pymysql.connect(host='private-db-mysql-tor1-7***REMOVED***-0.b.db.ondigitalocean.com',
user='***REMOVED***',
password='***REMOVED***',
port=25060,
db='trends',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)



def retrieve_keyword(cursor):
    # Read a single record
    sqlselect = "SELECT topic_title FROM keywords WHERE interest IS NULL ORDER BY 'id' DESC LIMIT 1;"
    cursor.execute(sqlselect)
    # Returns a list of key:value dicts with 'topic_title':keyword
    listofdicts = cursor.fetchall()
    # Turns list of dict into a single-item list
    resultlist = [f['topic_title'] for f in listofdicts]
    return resultlist


def find_interest(cursor):
    #singlekeywordlist = retrieve_keyword(cursor)
    singlekeywordlist = ["Macbook"]
    keyword = str(singlekeywordlist[0])
    logging.info(f"Keyword is: {keyword}")

    logging.info("Commencing get_historical_interest search...")
    historical_df = pytrends.get_historical_interest(singlekeywordlist, frequency='daily', year_start=2010, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=8, day_end=1, hour_end=0, geo='CA', gprop='', sleep=60)


    if historical_df.empty:
        logging.info(f"Keyword type: {type(keyword)}")
        logging.info(f"Not enough data for keyword: {keyword} deleting from table...")
        sql_query = "DELETE from keywords WHERE topic_title = '{}'".format(keyword)
        #cursor.execute(sql_query)
    else:
        #Don't care about the isPartial column - dropping it
        df = historical_df.drop(columns=['isPartial'])
        #Removing the extra 0's from datetime
        df.index = pd.to_datetime(df.index, format = '%Y-%m-%d').strftime('%Y-%m-%d')
        logging.info(f"df.head is: {df.head()}")
        logging.info(f"Df.dtypes is: {df.dtypes()}")
        csv = df.to_csv()
        
        sql_query = "UPDATE keywords SET interest='{}' WHERE topic_title = '{}'".format(csv, keyword)
       # cursor.execute(sql_query)
        #connection.commit()

    logging.info("Execute finished!")
    

if __name__ =='__main__':
    logging.root.handlers = []
    logging.basicConfig(level=logging.DEBUG,handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)])

    logging.info("Greetings, Pleb!")
    time.sleep(2)
    logging.info(f"Number of Cycles to run: {numofcycles}")
    with connection.cursor() as cursor: 
        for i in range(numofcycles):
                find_interest(cursor)
                
        connection.close()