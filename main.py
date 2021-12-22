from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'user'
)

@app.route('/add_user', methods=['GET', 'POST']) 
def add_user():
    if request.method == 'GET':
        return render_template(
            'add_user.html'
        )


    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']

        cursor = mydb.cursor(prepared = True)
        sql = "INSERT INTO User VALUES (null, ?, ?, ?, ?, ?)"
        values = (firstname, lastname, age, phone, email)

        cursor.execute(sql, values)
        mydb.commit()

        return 'User successfully added!'


@app.route('/all_users')
def all_users():
    cursor = mydb.cursor(prepared = True)
    sql = "SELECT * FROM User"
    
    cursor.execute(sql)

    result = cursor.fetchall()
    n = len(result)

    for i in range(n):
        result[i] = list(result[i])
        for j in range(len(result[0])):
            if isinstance(result[i][j], bytearray):
                result[i][j] = result[i][j].decode()

    return render_template(
        'all_users.html',
        users = result
    )


@app.route('/all_users/<user_id>')
def one_user(user_id):
    cursor = mydb.cursor(prepared = True)

    sql = "SELECT * FROM User WHERE UserID = ?"
    value = (user_id, ) #Mora da ima zreaz ako postoji samo jedna vr.
    cursor.execute(sql, value) 
    
    result = cursor.fetchone()

    if result == None:
        return '<h3>There is no user with that ID<h3>'


    result = list(result)
    for i in range(len(result)):
        if isinstance(result[i], bytearray):
            result[i] = result[i].decode()


    return render_template(
        'one_user.html',
        user = result
    )


@app.route('/delete/<user_id>', methods=['POST'])
def delete(user_id):
    cursor = mydb.cursor(prepared = True)
    sql = "DELETE FROM User WHERE UserID = ?"
    value = (user_id, )

    cursor.execute(sql, value)
    mydb.commit()

    return redirect(
        url_for('all_users')
    )


@app.route('/update/<user_id>', methods=['GET', 'POST'])
def update(user_id):
    if request.method == 'GET':
        cursor = mydb.cursor(prepared = True)
        sql = "SELECT * FROM User WHERE UserID = ?"
        value = (user_id, )

        cursor.execute(sql, value)
        result = cursor.fetchone()

        if result == None:
            return redirect(
                url_for('all_users')
            )

        else:
            result = list(result)
            n = len(result)

            for i in range(n):
                if isinstance(result[i], bytearray):
                    result[i] = result[i].decode()

            return render_template(
                'update.html',
                user = result
            )

    else:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']

        cursor = mydb.cursor(prepared = True)
        sql = "UPDATE User SET Firstname=?, Lastname=?, Age=?, Phone=?, Email=?"
        values = (firstname, lastname, age, phone, email)
        cursor.execute(sql, values)

        mydb.commit()

        return redirect(
            url_for('all_users')
        )


app.run(debug = True)
#Kada vrsimo neku promenu nad bazom data treba da uradimo mydb.commit() tj.
# Da sacuvamo sve promene!