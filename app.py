from flask import Flask, render_template, request, redirect, url_for
from pandas import DataFrame, to_datetime
import pandas as pd
import numpy as np
import json
import requests
import time
import datetime
from bokeh.plotting import figure, output_file, show
from bokeh import embed
from bokeh.charts import TimeSeries, show, output_file
from bokeh.layouts import column
from bokeh.resources import CDN
from bokeh.embed import components
import os
import cgi



app = Flask(__name__)

# vars for API call composition from quandl
API_Key = os.environ['QUANDL']

@app.route('/')
def main():
  return redirect('/Page1')

@app.route('/Page1', methods=['GET','POST'])
def Page1():
  return render_template('Page1.html')

def plotter():
	# find out what data the user wants plotted
	selected = request.form.getlist('check')

	# pull in the ticker info from page 1
	ticker = request.form['ticker_symbol']

	# calculate custom start and end dates as strings, based on where you are today
	start = (datetime.datetime.now() + datetime.timedelta(-30)).strftime("%Y%m%d")
	end = time.strftime("%Y%m%d")

	# form custom url to fetch data from quandl using requests library (as json)
	url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte='+start+'&date.lt='+end+'&ticker='+ticker+'&api_key='+API_Key
	req = requests.get(url)
	data = req.json()

	# get a plottable dataframe (from json object to pandas)
	data_section = data['datatable']['data']
	column_labels = ['ticker','date','open','high','low','close','volume','ex-dividend','split_ratio','adj_open','adj_high','adj_low','adj_close','adj_volume']
	data_pd = pd.DataFrame(data = data_section, columns = column_labels)
	
	# setup date format for plot
	data_pd = data_pd.set_index(['date'])
	data_pd.index = pd.to_datetime(data_pd.index)

	# plot lines conditionally using Bokeh
	ts_plot = figure(x_axis_type = "datetime")

	if "closing" in selected:
	 	ts_plot.line(data_pd.index, data_pd['close'], color = 'blue', legend = 'Closing')

	if "adj_close" in selected:
		ts_plot.line(data_pd.index, data_pd['adj_close'], color = 'green', legend = 'Adjusted Closing')

	if "opening" in selected:
		ts_plot.line(data_pd.index, data_pd['open'], color = 'yellow', legend = 'Opening')

	if "adj_opening" in selected:
		ts_plot.line(data_pd.index, data_pd['adj_open'], color = 'red', legend = 'Adjusted Opening')

	return ts_plot


@app.route('/Page2', methods=['GET', 'POST'])
def Page2():
	plot = plotter()
	script, div = embed.components(plot)
	return render_template('Page2.html', ticker_symbol = request.form['ticker_symbol'], div = div, script = script)

if __name__ == '__main__':
  app.run(port=33507)
