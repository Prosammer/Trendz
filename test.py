import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px





# Only needs to run once - all requests use this session
# Timezone is 240 (could be -240 as well?)
pytrends = TrendReq(hl='en-US', tz=240,retries=2)




def find_interest():
    
    kw_list = ["Juul"]
    pytrends.build_payload(kw_list=kw_list, timeframe='today 3-m', geo='CA')
    #   Main data-retrieval function:
    print("Commencing historical interest search...")
    #interest_over_time_df = pytrends.interest_over_time()
    #print(interest_over_time_df.head())

    kw_interest = pytrends.get_historical_interest(kw_list, year_start=2020, month_start=7, day_start=7, hour_start=0, year_end=2020, month_end=10, day_end=2, hour_end=0, cat=0, sleep=2,frequency='daily')
    print(kw_interest)



if __name__ =='__main__':
    find_interest()