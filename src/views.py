from flask import Blueprint, render_template, flash
import mysql.connector
from mysql.connector import Error
import os

# Create Blueprint
views = Blueprint('views', __name__)

host=os.getenv('DB_HOST', 'localhost'),
port=os.getenv('DB_PORT', 3306),
database=os.getenv('DB_NAME'),
user=os.getenv('DB_USER'),
password=os.getenv('DB_PASSWORD')
print(host, port, database, user, password)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

        return conn
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/current')
def current():
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return render_template('current.html', parties=None)
    try:
        cur = conn.cursor(dictionary=True)
        query = """
            SELECT st.*, s.name AS server_name
            FROM serversTables st
            JOIN servers s ON st.serverID = s.employeeID;
        """
        cur.execute(query)
        parties = cur.fetchall()
        return render_template('current.html', parties=parties)
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('current.html', parties=None)
    finally:
        if 'cur' in locals():
            cur.close()
        if conn.is_connected():
            conn.close()

@views.route('/reservations')
def reservations():
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return render_template('reservations.html', parties=None)
    try:
        cur = conn.cursor(dictionary=True)
        query = """
            SELECT r.*, s.name as server_name, c.name as customer_name FROM reservations r JOIN servers s ON r.employeeID = s.employeeID JOIN customers c ON r.customerID = c.customerID;
        """
        cur.execute(query)
        reservations = cur.fetchall()
        return render_template('reservations.html', reservations=reservations)
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('reservations.html', parties=None)
    finally:
        if 'cur' in locals():
            cur.close()
        if conn.is_connected():
            conn.close()