from main import kw_list
import pandas as pd
import os, requests, time
import plotly.express as px


df = pd.read_pickle(F"{kw_list[0]}_vs_{kw_list[1]}.pkl")
del df['isPartial']

#print(df.head(10))

#print(df.index)
fig = px.line(df, x=df.index, y=["Tiktok","Juul"], title=f"Popularity of the keyword: {kw_list[0]} vs {kw_list[1]} ")

fig.write_html("test.html")