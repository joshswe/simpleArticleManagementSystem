from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
#from data import Articles
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
from formclass import RegisterForm, ArticleForm


#Create an instance of the flask class
app = Flask(__name__) 

# Config MySQL
# Newer versions of Ubuntu (≥16.04): Removing the line bind-address 127.0.0.1 in /etc/mysql/mysql.conf.d/mysqld.cnf.
app.config['MYSQL_HOST']='' 
app.config['MYSQL_USER']=''
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']=''
app.config['MYSQL_CURSORCLASS']='DictCursor'
app.config['MYSQL_PORT'] = 3306

# Initialize MySQL
mysql = MySQL(app)

# Index
@app.route('/')
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Articles
@app.route('/articles')
def articles():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall() # This will be fetched in dictionary form
    if result > 0:
        return render_template('articles.html',articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)

    #Close connection
    cur.close()

    return render_template('articles.html', articles = Articles)

#Single Article
@app.route('/article/<string:id>/')
def article(id):
        # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s",[id])
    article = cur.fetchone() 
    return render_template('article.html', article=article)



# User Register
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute Query
        cur.execute("INSERT INTO users(name,email,username,password) VALUES (%s,%s,%s,%s)",(name,email,username,password))
        # Commit to DB 
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        # Create Cursor
        cur = mysql.connection.cursor()
        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
        app.logger.info(result)
        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            app.logger.info(data)
            password = data['password']
            # Compare passwords
            if sha256_crypt.verify(password_candidate,password):
                # Valid Login Credentials
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in','success')
                return redirect(url_for('dashboard'))
            else:
                msgInvalidLogin = 'Invalid Login'
                return render_template('login.html',error=msgInvalidLogin) # Error message can be found in inludes/_messages.html
            # Close connection
            cur.close()
        else:
            msgInvalidUser = 'Username Not Found'
            return render_template('login.html',error=msgInvalidUser)


    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please login','danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall() # This will be fetched in dictionary form
    if result > 0:
        return render_template('dashboard.html',articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    #Close connection
    cur.close()


# Add Article
@app.route('/add_article', methods=['GET','POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        #Create cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s,%s,%s)",(title,body,session['username']))
        # Commit to database
        mysql.connection.commit()
        # Close connection
        cur.close()

        flash('Your article was created!','success')

        return redirect(url_for('dashboard'))
    return render_template('add_article.html',form=form)

# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_article(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get article by ID
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()
    # Get form
    form = ArticleForm(request.form)
    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        #Create cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title,body,id))
        # Commit to database
        mysql.connection.commit()
        # Close connection
        cur.close()

        flash('Article Updated','success')

        return redirect(url_for('dashboard'))
    return render_template('edit_article.html',form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    #Create cursor
    cur = mysql.connection.cursor()
    # Execute
    cur.execute("DELETE FROM articles WHERE id=%s",[id])
    # Commit to database
    mysql.connection.commit()
    # Close connection
    cur.close()

    flash('Article Deleted','success')

    return redirect(url_for('dashboard'))


if __name__ == '__main__': #That means the script is going to be executed
    app.secret_key='secret123'
    app.run(debug=True)