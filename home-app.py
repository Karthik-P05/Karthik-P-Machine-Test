from flask import  *
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'machine_test'

mysql = MySQL(app)

app.secret_key='ab'

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/login')
# def home1():
#     return render_template('home.html')


@app.route('/registration')
def register():
    return render_template('register.html')

@app.route('/save', methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['mobile']
        username = request.form['user']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT username from users where username = '{username}'")
        user = cur.fetchone()
        cur.close()
        
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT username from users where email = '{email}'")
        em = cur.fetchone()
        cur.close()
        
        
        if em:
            return render_template('register.html', error1 = "Email already exists!", name=name, mobile=phone, user=username)
        
        if user:
            return render_template('register.html', error = "Username already exists!", name=name, email=email, mobile=phone)
        
        
            
        
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (name, mobile, email, username, password) VALUES (%s, %s, %s, %s, %s)",(name, phone, email, username, password))
            mysql.connection.commit()
            cur.close()

            # return redirect('/login')
            return render_template('register.html', success = True)
        
    return render_template('register.html')


@app.route('/home', methods=['GET','POST'])
def login():   
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cur.execute(f"select * from users where username = '{username}' and password = '{password}'")
        cur.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        user = cur.fetchone()
        cur.close()
        
        if user:           
            session['loggedin'] = True
            session['login_id'] = user['user_id']
            session['username'] = user['username']
            return render_template('user-home.html', user_data = user)
        
        elif username == 'admin' and password == 'admin':
            return render_template('admi-home.html')
        else:
            return render_template('home.html', error = "Invalid Username or Password!")
        
    return render_template('home.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('login_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/createpost', methods=['GET', 'POST'])
def create_post():
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        tags = request.form['tags']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        
        user_id = session['login_id']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts (user_id, title, description, tags, created_at) VALUES (%s, %s, %s, %s, %s)",(user_id, title, description, tags, created_at))
        mysql.connection.commit()
        cur.close()
        
        return redirect('home')
        
        
    return render_template('create-post.html')












if __name__ == "__main__":
    app.run(debug=True)