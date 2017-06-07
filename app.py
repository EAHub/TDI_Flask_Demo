from flask import Flask, render_template, request, redirect

app = Flask(__EliTickerApp__)

@app.route('/')
def main():
  return redirect('/Page1')

@app.route('/Page1')
def Page1():
  return render_template('Page1.html')

if __name__ == '__main__':
  app.run(port=33507)
