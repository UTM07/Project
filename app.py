from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Cambia 'root' si usas otro usuario
app.config['MYSQL_PASSWORD'] = ''  # Pon tu contraseña aquí si es necesario
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM mytable')
    data = cursor.fetchall()
    return render_template('index.html', mydata=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO mytable (name) VALUES (%s)', [name])
        mysql.connection.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        cursor.execute('UPDATE mytable SET name = %s WHERE id = %s', (name, id))
        mysql.connection.commit()
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM mytable WHERE id = %s', [id])
    data = cursor.fetchone()
    return render_template('update.html', mydata=data)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM mytable WHERE id = %s', [id])
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
