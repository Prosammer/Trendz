import pandas as pd
from pytrends.request import TrendReq

# Only needs to run once - all requests use this session
pytrends = TrendReq(hl='en-US', tz=360)

# Keyword List Below
kw_list=["Juul","LED Strips", "TikTok"]

# Payload only needed for interest_over_time(), interest_by_region() & related_queries()
#pytrends.build_payload(kw_list, cat='362', timeframe='today 3-m', geo='CA', gprop='')




df = pytrends.get_historical_interest(kw_list, year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=8, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)

print(df)
df.to_pickle(JuulLEDTikTok.pkl) 