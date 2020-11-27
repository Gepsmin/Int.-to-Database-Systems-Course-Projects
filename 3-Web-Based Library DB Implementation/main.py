from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
from datetime import date, timedelta
due = (date.today()+timedelta(days=14)).isoformat()


app = Flask(__name__)


db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/add_book', methods=['GET','POST'])
def add_book():
    if request.method == 'POST':
        book = request.form
        isbn = book['ISBN']
        title = book['title']
        author = book['author']
        year = book['year']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO book(isbn, title, author, year) VALUES(%s, %s, %s, %s)", (isbn, title, author, year))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('add_book.html')


@app.route('/delete_book', methods=['GET', 'POST'])
def delete_book():
    if request.method == 'POST':
        isbn = request.form['ISBN']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM book WHERE isbn = '{}'".format(isbn))
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM borrow WHERE isbn = '{}'".format(isbn))
        if result > 0:
            value = cur.fetchall()
            cur.close()
            tc = value[0][1]
            cur = mysql.connection.cursor()
            cur.execute("CALL delete_borrowed({})".format(isbn))
            mysql.connection.commit()
            cur.close()
            cur = mysql.connection.cursor()
            cur.execute("CALL decrement({})".format(tc))
            mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('delete_book.html')

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        tc = request.form['tc']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM user WHERE tc = '{}'".format(tc))
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("CALL delete_all_borrowed({})".format(tc))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('delete_user.html')

@app.route('/all_books', methods=['GET', 'POST'])
def all_books():
    cur = mysql.connection.cursor()
    resultValues = cur.execute("SELECT * FROM book")
    if resultValues > 0:
        books = cur.fetchall()
        return render_template('all_books.html', books=books)
    return "nothing to show"

@app.route('/all_users', methods=['GET', 'POST'])
def all_users():
    cur = mysql.connection.cursor()
    resultValues = cur.execute("SELECT * FROM user")
    if resultValues > 0:
        users = cur.fetchall()
        return render_template('all_users.html', users=users)
    return "nothing to show"


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user = request.form
        tc = user['tc']
        name = user['name']
        surname = user['surname']
        hold = 0
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(tc, name, surname, hold) VALUES(%s, %s,%s,%s)", (tc, name, surname, hold))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('add_user.html')

@app.route('/search_book')
def search_book():
    return render_template('search_book.html')

@app.route('/search_isbn', methods=['GET', 'POST'])
def search_isbn():
    if request.method == "POST":
        isbn = request.form['value']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM book WHERE isbn = '{}'".format(isbn))
        if result > 0:
            books = cur.fetchall()
            return render_template('searched_book.html', books=books)
        else:
            return "There is no book with wanted property"
    return render_template('search_isbn.html')

@app.route('/search_title', methods=['GET', 'POST'])
def search_title():
    if request.method == "POST":
        title = request.form['value']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM book WHERE title = '{}'".format(title))
        if result > 0:
            books = cur.fetchall()
            return render_template('searched_book.html', books=books)
        else:
            return "There is no book with wanted property"
    return render_template('search_title.html')

@app.route('/search_author', methods=['GET', 'POST'])
def search_author():
    if request.method == "POST":
        author = request.form['value']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM book WHERE author = '{}'".format(author))
        if result > 0:
            books = cur.fetchall()
            return render_template('searched_book.html', books=books)
        else:
            return "There is no book with wanted property"
    return render_template('search_author.html')

@app.route('/search_year', methods=['GET', 'POST'])
def search_year():
    if request.method == "POST":
        year = request.form['value']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM book WHERE year = '{}'".format(year))
        if result > 0:
            books = cur.fetchall()
            return render_template('searched_book.html', books=books)
        else:
            return "There is no book with wanted property"
    return render_template('search_year.html')

@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    if request.method == "POST":
        form = request.form
        tc = form['tc']
        isbn = form['isbn']
        cur = mysql.connection.cursor()
        result = cur.execute("INSERT INTO borrow(isbn, tc, due) VALUES(%s, %s,%s)", (isbn, tc, due))
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor()
        result = cur.execute("CALL increment({})".format(tc))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('borrow_book.html')

@app.route('/show_borrowed_books', methods=['GET', 'POST'])
def show_borrowed_books():
    if request.method == "POST":
        tc = request.form['tc']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT hold FROM user WHERE tc = '{}'".format(tc))
        hold = cur.fetchall()[0][0]
        result = cur.execute("SELECT * FROM borrow WHERE tc = '{}'".format(tc))
        if result > 0:
            borrowed = cur.fetchall()
            return render_template('show_borrowed_books.html', borrowed=borrowed, hold=hold , show=True)

    return render_template('show_borrowed_books.html', show=False)

if __name__=='__main__':
    app.run(debug=True)

