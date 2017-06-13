from flask import Flask, render_template, request, redirect, url_for
from pandas import DataFrame, to_datetime
import pandas
import numpy as np
import json
import requests
import time
import datetime
from bokeh.plotting import figure, output_file, show
from bokeh import embed
import cgi
from bokeh.charts import TimeSeries, show, output_file
from bokeh.layouts import column
from bokeh.resources import CDN
from bokeh.embed import components
import os



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
	ticker = request.form['ticker_symbol']

	start = (datetime.datetime.now() + datetime.timedelta(-30)).strftime("%Y%m%d")
	end = time.strftime("%Y%m%d")

	url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte='+start+'&date.lt='+end+'&ticker='+ticker+'&api_key='+API_Key
	req = requests.get(url)
	data = req.json()

	# # using pandas to get a plottable df
	# data_req = DataFrame(quandl_data.json())
	# data_plot = DataFrame(data_req.ix['data','dataset'], columns = data_req.ix['column_names','dataset'])
	# data_plot.columns = [x.lower() for x in data_plot.columns]
	
	# data_plot = data_plot.set_index(['date'])
	# data_plot.index = to_datetime(data_plot.index)

	# # plot conditional lines in Bokeh
	ts_plot = figure(x_axis_type = "datetime")

	# if "closing" in selected:
	# 	ts_plot.line(data_plot.index, data_plot['CLOSE'], color = 'blue', legend = 'Closing')

	# if "adj_close" in selected:
	# 	ts_plot.line(data_plot.index, data_plot['ADJ_CLOSE'], color = 'green', legend = 'Adjusted Closing')

	# if "opening" in selected:
	# 	ts_plot.line(data_plot.index, data_plot['OPEN'], color = 'yellow', legend = 'Opening')

	# if "adj_opening" in selected:
	# 	ts_plot.line(data_plot.index, data_plot['ADJ_OPEN'], color = 'red', legend = 'Adjusted Opening')

	return ts_plot


@app.route('/Page2', methods=['GET', 'POST'])
def Page2():
	plot = plotter()
	script, div = embed.components(plot)
	return render_template('Page2.html', ticker_symbol = request.form['ticker_symbol'], div = div, script = script)

if __name__ == '__main__':
  app.run(port=33507)
