import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px
import pymysql.cursors


# Set desired number of cycles (for easy testing)
numofcycles = 2


# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=-240,retries=2,backoff_factor=0.2,)



# Connect to the database

connection = pymysql.connect(host='db-mysql-tor1-72034-do-user-8152651-0.b.db.ondigitalocean.com',
user='doadmin',
password='sjmfco80xbdp0rjl',
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
    singlekeywordlist = retrieve_keyword(cursor)
    keyword = str(singlekeywordlist[0])
    print("Keyword is: ", keyword)

    time.sleep(2)
    print("Commencing get_historical_interest search...")
    historical_df = pytrends.get_historical_interest(singlekeywordlist, frequency='daily', year_start=2010, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=8, day_end=1, hour_end=0, geo='CA', gprop='', sleep=0)

    sql_query = None

    if historical_df.empty:
        print("Not enough data for this keyword, deleting from table...")
        sql_query = "DELETE from keywords WHERE topic_title = \"%s\"" % (keyword)
    else:
        #Don't care about the isPartial column - dropping it
        df = historical_df.drop(columns=['isPartial'])
        # Dropping HH:MM:SS from the index's datetime format
        df.reset_index(inplace=True)
        print(df.head())
        print(df.dtypes)
        csv = df.to_csv()
        #df.index = pd.to_datetime(df.index, format = '%Y-%m-%d').strftime('%Y-%m-%d')
        sql_query = "UPDATE keywords SET interest=\"%s\" WHERE topic_title = \"%s\"" % (csv,keyword)

    cursor.execute(sql_query)
    print("Execute finished!")
    
        



if __name__ =='__main__':
    print("Number of Cycles to run: ", str(numofcycles))
    with connection.cursor() as cursor: 
        try:
            for i in range(numofcycles):
                find_interest(cursor)
                connection.commit()
                connection.close()
        except Exception as e:
                print(str(e))
                connection.close()