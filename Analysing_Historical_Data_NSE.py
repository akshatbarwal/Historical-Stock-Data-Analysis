#!/usr/bin/env python
# coding: utf-8

# # Reliance Industries Ltd. Stock Analysis (2020-2022)

# ## 1. Installing Yahoon Finance Python Library

# In[1]:


# Intsalling Yahoo Finance to extract the data for Reliance Industries Ltd

get_ipython().system('pip install yfinance')


# ## 2. Installing Python libraries

# In[31]:


# Importing the python libraries that we need to perform our analysis

import pandas as pd
import numpy as np
import yfinance as yf
from tabulate import tabulate

import plotly.graph_objects as go
import cufflinks as cf
from plotly.offline import iplot, init_notebook_mode
import matplotlib.pyplot as plt


# ## 3. Defining functions used in to analyze the yahoo finance data

# ### 3.1 Extracting the relevant data using get_stock_data function

# In[5]:


# Function for extracting the data using Yahoo finance

def get_stock_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker + ".NS", start = start_date, end = end_date)
        
        # Reset the index to make Date a column
        data = data.reset_index()
        
        return data
    
    except Exception as ex:
        
        print("Error occured:", str(ex))
        
        return None


# ### 3.2 Adding a Date column to our data

# In[12]:


# Function for adding the date column in the final extracted table

def add_date_column(data):
    
    if data is not None:
        # Extract the dates as strings from the "Date" column
        dates = data["Date"].dt.strftime("%Y-%m-%d").tolist()
        
        # Add the date column to the data
        data["Trading Date"] = dates
        
        return data


# ### 3.3 Printing the data in a tabulated manner using Tabulate library

# In[8]:


# Function to print the extracted data in a tabulated manner

def print_stock_data(data):
    
    if data is not None:
        
        # Since we do not require adjusted close price in our data, we will drop the respective column
        data = data.drop(["Adj Close"], axis = 1)
        
        data_list = data.values.tolist()
        
        headers = data.columns.tolist()
        
        print(tabulate(data_list, headers = headers, floatfmt = ".2f", tablefmt = "fancy_grid"))


# ### 3.4 Inputting the values for the Reliance stock

# In[15]:


# We will be using Reliance Industries Ltd as the company for our analysis

ticker = "RELIANCE"
start_date = "2020-01-01"
end_date = "2022-12-31"

stock_data = get_stock_data(ticker, start_date, end_date)
stock_data = add_date_column(stock_data)
print_stock_data(stock_data.head())


# ## 4. Basic Data Processing and Cleaning

# In[16]:


# How many rows and columns are there in our data
stock_data.shape


# In[17]:


stock_data.info()


# In[18]:


stock_data["Trading Date"] = pd.to_datetime(stock_data["Trading Date"])


# In[24]:


# Removing unwanted columns from stock_data
stock_data = stock_data.drop(["Adj Close", "Trading Date"], axis = 1)


# In[25]:


stock_data


# ## 5. Calculating the Avg. Daily Trading Volume using Pandas

# In[26]:


# Finding the Average Daily Trading Volume

adtv = stock_data["Volume"].mean()
print("The Average Daily Trading Volume is - ", adtv)


# ## 6. Generating an interactive Candlestick chart using Plotly

# In[36]:


# Candlestick chart for stock_data using plotly

fig = go.Figure(data = [go.Candlestick(x = stock_data['Date'],
                                      open = stock_data['Open'], 
                                      high = stock_data['High'],
                                      low = stock_data['Low'], 
                                      close = stock_data['Close'],
                                      increasing_line_color = "green",
                                      decreasing_line_color = "red")
                       ])

fig.update_layout(
    title = "Reliance Stock over a period of 3 years",
    yaxis_title = "RELIANCE Stock",
    xaxis_title = "Date"
)

fig.show()

