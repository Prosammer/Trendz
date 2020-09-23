import pandas as pd    
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

kw_list=["BlockChain"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='CA', gprop='')


df = pytrends.interest_by_region()
df.head(10)
print(df)

print("Fuck me it's been a while")