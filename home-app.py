from flask import  *

app = Flask(__name__)

app.secret_key='ab'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def home1():
    return render_template('home.html')


@app.route('/registration')
def register():
    return render_template('register.html')















if __name__ == "__main__":
    app.run(debug=True)