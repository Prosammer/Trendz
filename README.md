# Trendz

Trendz uses Deep Learning to find up-and-coming search terms. It does so by scraping Google Trends data (thanks to Pytrends), adding them to a PostgreSQL database, and finally running this time series data through a variety of models (ARMA, Prophet, and an Azure Deep learning model).

* Trendz is my current work-in-progress - I plan on creating docker images so the entire process can be demonstrated *
