from flask import Flask, render_template, request, redirect, flash, url_for
from bokeh.charts import TimeSeries, show, output_file
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
import config as con
import datetime
import quandl
from bokeh.resources import CDN
from bokeh import embed
from bokeh.embed import components
import numpy as np
import requests
import json
import pandas as pd
from pandas import DataFrame, to_datetime
import os
import cgi
import time


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
	# find out what the user wants
	selected = request.form.getlist('check')

	# get the json format data from quandl with requests.get
	ticker_symbol = request.form['ticker_symbol']
	now = datetime.now()
	start = (now - timedelta(days=30)).strftime('%Y-%m-%d')
	end = now.strftime('%Y-%m-%d')
	
	data_source = 'https://www.quandl.com/api/v3/datasets/WIKI/'+ticker_symbol+'.json?start_date='+start+'&end_date='+end+'&order=asc&api_key='+API_Key
	quandl_data = requests.get(data_source)

	# using pandas to get a plottable df
	data_req_pd = DataFrame(quandl_data.json())
	data_pd = DataFrame(data_req_pd.ix['data','dataset'], columns = data_req_pd.ix['column_names','dataset'])
	data_pd.columns = [x.lower() for x in data_pd.columns]
	
	data_pd = data_pd.set_index(['date'])
	data_pd.index = to_datetime(data_pd.index)

	# plot conditional lines in Bokeh
	ts_plot = figure(x_axis_type = "datetime")

	if "closing" in selected:
		ts_plot.line(data_pd.index, data_pd["CLOSE"], color = "blue", legend = "Closing")

	if "adj_close" in selected:
		ts_plot.line(data_pd.index, data_pd["ADJ_CLOSE"], color = "green", legend = "Adjusted Closing")

	if "opening" in selected:
		ts_plot.line(data_pd.index, data_pd["OPEN"], color = "yellow", legend = "Opening")

	if "adj_opening" in selected:
		ts_plot.line(data_pd.index, data_pd["ADJ_OPEN"], color = "red", legend = "Adjusted Opening")

	return ts_plot


@app.route('/Page2', methods=['GET', 'POST'])
def Page2():
	plot = plotter()
	script, div = embed.components(plot)
	return render_template('Page2.html', ticker_symbol = request.form['ticker_symbol'], div = div, script = script)

if __name__ == '__main__':
  app.run(port=33507)
