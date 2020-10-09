import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px
import pymysql.cursors
from sqlalchemy import create_engine

# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=-240,retries=2,backoff_factor=0.2,)

pytrends.build_payload(kw_list=['Yeti Cooler'], timeframe='all', geo='CA')


print("Commencing interest_over_time search...")
interest_over_time_df = pytrends.interest_over_time()

#print(interest_over_time_df.tail())
print(interest_over_time_df.groupby('isPartial').count())