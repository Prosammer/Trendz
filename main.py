import pandas as pd
from pytrends.request import TrendReq

# Only needs to run once - all requests use this session
pytrends = TrendReq(hl='en-US', tz=360)

# Keyword List Below
masterkeywordlist=["Juul","LED Strips", "TikTok"]

dicti = {}
i = 1
for keyword in masterkeywordlist:
    try:
        # Payload only needed for interest_over_time(), interest_by_region() & related_queries()
        pytrends.build_payload(kw_list=keyword, cat='362', timeframe='today 3-m', geo='CA', gprop='')
        dicti = pytrends.interest_over_time()
        i+= 1
        print("I am on round:" + i)
        time.sleep(6)
    except requests.exceptions.Timeout:
        print('Dis a timeout bruv')

#df = pytrends.get_historical_interest(kw_list, year_start=2020, month_start=6, day_start=1, hour_start=0, year_end=2020, month_end=7, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=60)


print(df.head())
# df.to_pickle(JuulLEDTikTok.pkl) 