import pandas as pd
import os, requests, time
import plotly.express as px

df = pd.read_pickle("Juul.pkl")
print(df.head(10))

fig = px.line(df, x="Juul", y="date", title=f"Popularity of the keyword: {kw_list[0]} ")

fig.write_html("test.html")