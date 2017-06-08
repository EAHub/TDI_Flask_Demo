from flask import Flask, render_template, request, redirect
from bokeh.charts import TimeSeries, show, output_file
from bokeh.layouts import column
from bokeh import embed
from bokeh.resources import CDN
import numpy as np
import pandas as pd


app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/Page1')

@app.route('/Page1', methods=['GET','POST'])
def Page1():
  return render_template('Page1.html')

def plotter():
	ticker_symbol=request.form['ticker_symbol']
	# closing = request.form['closing'],
	# adj_close = request.form['adj_close'],
	# opening = request.form['opening'],
	# adj_opening = request.form['adj_opening']

	ts_plot = figure(title = "Time Series")
	ts_plot.line([1,2,3,4],[2,4,6,8])

	return ts_plot


@app.route('/Page2', methods=['GET', 'POST'])
def Page2():
	bokeh_plot = plotter()
	script, div = embed.components(bokeh_plot)
	return render_template('Page2.html', ticker_symbol = request.form['ticker_symbol'], div = div, script = script)

if __name__ == '__main__':
  app.run(port=33507)
