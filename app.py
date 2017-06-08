from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/Page1')

@app.route('/Page1', methods=['GET','POST'])
def Page1():
  return render_template('Page1.html')


@app.route('/Page2', methods=['GET', 'POST'])
def Page2():
  return render_template('Page2.html', 
  	ticker_symbol=request.form['ticker_symbol'],
  	closing = request.form['closing'],
  	adj_close = request.form['adj_close'],
  	opening = request.form['opening'],
  	adj_opening = request.form['adj_opening'])

if __name__ == '__main__':
  app.run(port=33507)
