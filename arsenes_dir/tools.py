# Ignoring warning messages from python
import warnings
warnings.filterwarnings('ignore')

# General use imports
import pandas as pd
import numpy as np

# Time Series imports
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

# Useful modules imports
import wrangle

# Visualization imports
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from pylab import rcParams

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from IPython.display import display_html
from itertools import chain,cycle

# Stats, cross validation splitting, and modeling tools
import statsmodels.api as sm
from math import sqrt
from statsmodels.tsa.stattools import acf
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import DecomposeResult, seasonal_decompose
from sktime.forecasting.model_selection import SlidingWindowSplitter
from sktime.utils.plotting import plot_series

# Displaying DataFrames side by side #

def display_side_by_side(*args,titles=cycle([''])):
    '''
    This function takes in DataFrame, Series,
    or arrays and plots them side by side
    '''
    html_str=''
    for df,title in zip(args, chain(titles,cycle(['</br>'])) ):
        html_str+='<th style="text-align:center"><td style="vertical-align:top">'
        html_str+=f'<h2 style="text-align: center;">{title}</h2>'
        html_str+=df.to_html().replace('table','table style="display:inline"')
        html_str+='</td></th>'
    display_html(html_str,raw=True)


# Get windows in a Sliding Windows Splitter split of a dataset #

def get_windows(df, sws):
    """Generate windows"""
    train_windows = []
    val_windows = []
    for i, (train_index, val_index) in enumerate(sws.split(df)):
        train_windows.append(train_index)
        val_windows.append(val_index)
    return train_windows, val_windows

# Plots the different spits #

def plot_windows(df, train_windows, val_windows, title=" "):
    '''
    This function takes in a DataFrame, the train and validate windows from a Sliding Windows Splitter, and a title
    then returns a graph of the splits
    '''
    def get_df(length, split):
        # Create a constant vector based on the split for y-axis."""
        return np.ones(length) * split
    # Gets the number of splits for train and vallidate plus the length of the df
    n_splits = len(train_windows)
    n_timepoints = len(df)
    len_val = len(val_windows[0])
    # Provide the setup for the colors of  train and validate and sets the size
    train_color, val_color = sns.color_palette("colorblind")[:2]
    fig, ax = plt.subplots(figsize=[20, 14])
    # Plots each fold of the split
    for i in range(n_splits):
        train = train_windows[i]
        val = val_windows[i]
        ax.plot(np.arange(n_timepoints), get_df(n_timepoints, i), marker="o", c="lightgray")
        ax.plot(train, get_df(len(train), i), marker="o", c=train_color, label="Window")
        ax.plot(val, get_df(len_val, i), marker="o", c=val_color, label="Forecasting horizon")
    # Inverts the yaxis (o-41 going from top to bottom)
    ax.invert_yaxis()
    # Uses MaxNLocator to select a specific number of location corresponding to splits
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    # Sets the ticks and labels for xaxis
    ax.set(
        title=title,
        ylabel="Window number",
        xlabel="Time in number of hours",
        xticklabels=range(0, len(df), 10000)
    )
    # remove duplicate labels/handles
    handles, labels = [(leg[:2]) for leg in ax.get_legend_handles_labels()]
    ax.legend(handles, labels)

# Getting Mean Absolute Percentage Error#

def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Getting 

# Plotting an autocorrelation function #

def create_corr_plot(series, plot_pacf=False):
    corr_array = acf(series.dropna(), alpha=0.05)
    lower_y = corr_array[1][:,0] - corr_array[0]
    upper_y = corr_array[1][:,1] - corr_array[0]

    fig = go.Figure()
    [fig.add_scatter(x=(x,x), y=(0,corr_array[0][x]), mode='lines',line_color='#3f3f3f') 
     for x in range(len(corr_array[0]))]
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=corr_array[0], mode='markers', marker_color='#1f77b4',
                   marker_size=12)
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=upper_y, mode='lines', line_color='rgba(255,255,255,0)')
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=lower_y, mode='lines',fillcolor='rgba(32, 146, 230,0.3)',
            fill='tonexty', line_color='rgba(255,255,255,0)')
    fig.update_traces(showlegend=False)
    fig.update_xaxes(range=[-1,42])
    fig.update_yaxes(zerolinecolor='#000000')
    
    title='Autocorrelation (ACF)'
    fig.update_layout(title=title)
    fig.show()


# Plotting seasonal decomposition #

'''
This function takes in a statistical model:
1.the seasonal decomposition using moving averages:
a pd Series of the value to plot (df.column_name, pd.Series, np.array),
the model or type of seasonal component ('additive' or 'multiplicative'),
and a period determining the amount of lag (integer),
2.the dates of the dataset as a Series (df.column_name, pd.Series) or
the length of the observed variable (np.arange(len(result.observed)))
'''

def plot_seasonal_decomposition(result:DecomposeResult, dates:pd.Series=None, title:str='Seasonal Decomposition'):
    x_values = dates if dates is not None else np.arange(len(result.observed))
    return (
        make_subplots(
            rows=4,
            cols=1,
            subplot_titles=['Observed or Steps', 'Trend', 'Seasonal', 'Residuals'],
        )
        .add_trace(
            go.Scatter(x=x_values, y=result.observed, mode='lines', name='Observed'),
            row=1,
            col=1,
        )
        .add_trace(
            go.Scatter(x=x_values, y=result.trend, mode='lines', name='Trend'),
            row=2,
            col=1,
        )
        .add_trace(
            go.Scatter(x=x_values, y=result.seasonal, mode='lines', name='Seasonal'),
            row=3,
            col=1,
        )
        .add_trace(
            go.Scatter(x=x_values, y=result.resid, mode='markers', name='Residual'),
            row=4,
            col=1,
        )
        .update_layout(
            height=900, title=f'<b>{title}</b>', margin={'t':100}, title_x=0.5, showlegend=False
        )
    )

# Producing a progress bar #

def progress_bar(progress, total):
    percent=100 * (progress / float(total))
    bar = '▌' * int(percent) + '»' * (100 - int(percent))
    print(f'\r|{bar}|) {percent:.2f}%', end='\r')