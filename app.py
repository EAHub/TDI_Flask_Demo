from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def main():
  return redirect('/Page1')

@app.route('/Page1', methods=['GET','POST'])
def Page1():
  return render_template('Page1.html')

@app.route('/Page2')
def Page2():
  return render_template('Page2.html', methods=['GET', 'POST'])

if __name__ == '__main__':
  app.run(port=33507)
