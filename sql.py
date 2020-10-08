import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px
import pymysql.cursors
from sqlalchemy import create_engine

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

def df_cleaner(df):
    preclean_len = len(df.index)
    df.drop_duplicates(subset='topic_title', keep='first', inplace=False).reset_index(drop=True)
    cleaned_len = len(df.index)
    if preclean_len != cleaned_len:
        print(abs(preclean_len-cleaned_len)," duplicate records were dropped.")
    return df


masterkeywordDF = pd.read_pickle("masterkeywordDF.pkl")
# Insert whole DataFrame into MySQL
cleaneddf = df_cleaner(masterkeywordDF)
cleaneddf.to_sql('keywords', con = engine, if_exists = 'append', chunksize = 1000)

#masterkeywordDF.to_sql('DFkeywords', con, flavor='mysql', schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None)


#cleanedKeywords = df_cleaner(masterkeywordDF)
#cleanedKeywords.to_pickle("masterkeywordDF.pkl")
#cleanedKeywords.to_html('masterkeywordDF.html')

#connection.close()

