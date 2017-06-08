from flask import Flask, render_template, request, redirect
from bokeh.charts import TimeSeries, show, output_file
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from bokeh.resources import CDN
from bokeh import embed
from bokeh.embed import components
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

	selected = request.form.getlist('check')

	if "closing" in selected:
		ts_plot = figure(title="CLOSING SELECTED", plot_width=300, plot_height=300)

	if "adj_close" in selected:
		ts_plot = figure(title="ADJ CLOSE SELECTED", plot_width=300, plot_height=300)

	if "opening" in selected:
		ts_plot = figure(title="OPENING SELECTED", plot_width=300, plot_height=300)

	if "adj_opening" in selected:
		ts_plot = figure(title="ADJ OPEN SELECTED", plot_width=300, plot_height=300)

	ts_plot.line(x=[1, 2, 3, 4, 5], y=[6, 7, 2, 4, 5])

	return ts_plot


@app.route('/Page2', methods=['GET', 'POST'])
def Page2():
	plot = plotter()
	script, div = embed.components(plot)
	return render_template('Page2.html', ticker_symbol = request.form['ticker_symbol'], div = div, script = script)

if __name__ == '__main__':
  app.run(port=33507)
