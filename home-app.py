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
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        user_id = session['login_id']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts (user_id, title, description, tags, created_at) VALUES (%s, %s, %s, %s, %s)",(user_id, title, description, tags, created_at))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('my_posts'))
    
    
    return render_template('create-post.html')
        
        
    # return render_template('create-post.html')

@app.route('/userhome')
def user_home():
    if 'loggedin' in session:
        user_data = session['username'] 
        return render_template('user-home.html', user_data=user_data)
    else:
        return redirect(url_for('login'))


@app.route('/myposts')
def my_posts():
    if 'loggedin' not in session:
        return redirect('/home')
    
    user_id = session['login_id']

    # cur = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM posts WHERE user_id = %s", (user_id,))
    posts = cur.fetchall()
    cur.close()
    # print(posts)

    return render_template('my-post.html', posts=posts)



@app.route('/deletepost/<int:post_id>')
def delete_post(post_id):
    
    if 'loggedin' not in session:
        return redirect('/home')

    user_id = session['login_id']

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM posts WHERE post_id = %s AND user_id = %s", (post_id, user_id))
    mysql.connection.commit()
    cur.close()

    return redirect('/myposts')


@app.route('/publishpost/<int:post_id>')
def publish_post(post_id):
    
    if 'loggedin' not in session:
        return redirect('/home')

    user_id = session['login_id']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE posts SET is_published = True WHERE post_id = %s AND user_id = %s", (post_id, user_id))
    mysql.connection.commit()
    cur.close()

    return redirect('/myposts')


@app.route('/unpublish/<int:post_id>')
def unpublish_post(post_id):
    
    if 'loggedin' not in session:
        return redirect('/home')

    user_id = session['login_id']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE posts SET is_published = False WHERE post_id = %s AND user_id = %s", (post_id, user_id))
    mysql.connection.commit()
    cur.close()

    return redirect('/myposts')



@app.route('/editpost/<int:post_id>')
def edit_post(post_id):
    if 'loggedin' not in session:
        return redirect('/home')
    
    user_id = session['login_id']
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM posts WHERE post_id = %s AND user_id = %s", (post_id, user_id))
    post = cur.fetchone()
    cur.close()

    return render_template('edit-post.html', post = post)

@app.route('/updatepost/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    
    if 'loggedin' not in session:
        return redirect('/home')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        tags = request.form['tags']
        
        user_id = session['login_id']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE posts SET title = %s, description = %s, tags = %s WHERE post_id = %s AND user_id = %s", (title, description, tags, post_id, user_id))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('my_posts'))
    
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM posts WHERE post_id = %s AND user_id = %s", (post_id, user_id))
    post = cur.fetchall()
    cur.close()

    return render_template('edit-post.html', post = post)


# @app.route('/viewposts')
# def view_posts():
#     return render_template('view-posts.html')


@app.route('/viewposts')
def list_posts():
    if 'loggedin' not in session:
        return redirect('/home')
    
    user_id = session['login_id']
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM likes")
    like = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT p.user_id, p.post_id, p.title, p.description,p.tags, p.created_at, p.is_published,
        (SELECT COUNT(*) FROM likes WHERE post_id = p.post_id) as likes_count,
        (SELECT name FROM users WHERE user_id = p.user_id) as user,
        (SELECT COUNT(*) FROM likes WHERE post_id = p.post_id AND user_id = %s) as user_liked
        FROM posts p
        WHERE p.is_published = True
        ORDER BY p.created_at DESC
    """, (user_id,))
    
    posts = cur.fetchall()
    cur.close()

    return render_template('view-posts.html', posts=posts , like = like)


@app.route('/like/<int:post_id>')
def like_post(post_id):
    if 'loggedin' not in session:
        return redirect('/home')

    user_id = session['login_id']

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM likes WHERE post_id = %s AND user_id = %s", (post_id, user_id))
    like = cur.fetchone()

    if like:
        cur.execute("DELETE FROM likes WHERE post_id = %s AND user_id = %s", (post_id, user_id))
    else:
        cur.execute("INSERT INTO likes (post_id, user_id) VALUES (%s, %s)", (post_id, user_id))

    mysql.connection.commit()
    cur.close()

    return redirect('/viewposts')


if __name__ == "__main__":
    app.run(debug=True)