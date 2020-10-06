import pandas as pd
import os, requests, time, operator
from pytrends.request import TrendReq
import plotly.express as px


def df_cleaner(df):
    preclean_len = len(df.index)
    df.drop_duplicates(subset='topic_title', keep='first', inplace=False).reset_index(drop=True)
    cleaned_len = len(df.index)
    if preclean_len != cleaned_len:
        print(abs(preclean_len-cleaned_len)," duplicate records were dropped.")
    return df



masterkeywordDF = pd.read_pickle("masterkeywordDF.pkl")
cleanedKeywords = df_cleaner(masterkeywordDF)
cleanedKeywords.to_pickle("masterkeywordDF.pkl")
cleanedKeywords.to_html('masterkeywordDF.html')




#cursor.execute("CREATE TABLE keywords (formattedValue TEXT, topic_mid TEXT,topic_title TEXT, topic_type TEXT, parent TEXT, checked INTEGER)")


# Already moved pandas to sql: cleanedKeywords.to_sql(name='keywords', con=connection)
