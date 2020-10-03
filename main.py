import pandas as pd
import os, requests, time
from pytrends.request import TrendReq
#pd.options.plotting.backend = "plotly"
import plotly.express as px



# Only needs to run once - all requests use this session
pytrends = TrendReq(hl='en-US', tz=-240)

# Keyword List Below

kw_list = ["Juul"]

# Note: Payload only needed for interest_over_time(), interest_by_region() & related_queries()
# pytrends.build_payload(kw_list =["Juul"], cat='', timeframe='today 3-m', geo='', gprop='')
try:
    time.sleep(.3)
    #df = pytrends.top_charts(2019, hl='en-US', tz=300, geo='GLOBAL')

    # Simple test dataframe:
        #df = pd.DataFrame(dict(a=[1,3,2], b=[3,2,1]))
    #   Main data-retrieval function:
    #df = pytrends.get_historical_interest(kw_list, year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2019, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=15, frequency='daily')
    #df.to_pickle("Juul.pkl") 
except requests.exceptions.Timeout:
    print("Timeout bruv")




