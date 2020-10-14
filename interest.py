import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px
import pymysql.cursors


# Set desired number of cycles (for easy testing)
numofcycles = 100

# Trying BlazingSEO shared proxies
proxylist = ['https://104.168.51.141:4444','https://192.186.134.157:4444','https://192.3.214.40:4444','https://104.144.220.10:4444','https://104.144.28.167:4444','https://172.245.181.226:4444','https://192.210.185.193:4444','https://23.236.232.162:4444','https://23.254.68.49:4444','https://23.94.176.161:4444','https://69.4.90.17:4444','https://107.172.94.128:4444','https://138.128.84.159:4444','https://192.186.161.228:4444','https://192.241.64.90:4444','https://192.241.80.170:4444','https://198.12.80.148:4444','https://198.23.217.80:4444','https://23.250.94.234:4444','https://45.72.0.245:4444']


# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=-240,retries=2,backoff_factor=0.2, proxies=proxylist)



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
    time.sleep(.5)
    print("Commencing get_historical_interest search...")
    historical_df = pytrends.get_historical_interest(singlekeywordlist, frequency='daily', year_start=2010, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=8, day_end=1, hour_end=0, geo='CA', gprop='', sleep=3)


    if historical_df.empty:
        print("Not enough data for keyword: ",keyword," deleting from table...")
        print("historical_df type: ",type(historical_df))
        print(historical_df.head())
        sql_query = "DELETE from keywords WHERE topic_title = '{}'".format(keyword)
        cursor.execute(sql_query)
    else:
        #Don't care about the isPartial column - dropping it
        df = historical_df.drop(columns=['isPartial'])
        df.index = pd.to_datetime(df.index, format = '%Y-%m-%d').strftime('%Y-%m-%d')
        # Dropping HH:MM:SS from the index's datetime format
        #df.reset_index(inplace=True)
        print(df.head())
        print(df.dtypes)
        csv = df.to_csv()
        
        sql_query = "UPDATE keywords SET interest='{}' WHERE topic_title = '{}'".format(csv, keyword)
        cursor.execute(sql_query)
        connection.commit()

    print("Execute finished!")
    

if __name__ =='__main__':
    print("Number of Cycles to run: ", str(numofcycles))
    with connection.cursor() as cursor: 
        for i in range(numofcycles):
                find_interest(cursor)
                
        connection.close()