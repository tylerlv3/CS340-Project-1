from flask import Blueprint, render_template, flash, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Create Blueprint
views = Blueprint('views', __name__)

load_dotenv()

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

@views.route('/current', methods=['GET', 'POST'])
def current():
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return render_template('current.html', parties=None)
    try:
        cur = conn.cursor(dictionary=True)
        if request.method == 'POST':
            # Retrieve form values from drop-down menus
            employee_id = request.form.get('employeeID')
            table_id = request.form.get('tableID')
            # Customer is optional. If not chosen an empty string is sent.
            customer_id = request.form.get('customerID') or None
            insert_query = """
                INSERT INTO serversTables (employeeID, tableID, status)
                VALUES (%s, %s, %s);
            """
            cur.execute(insert_query, (employee_id, table_id, 'open')) #add customer back here if we decide to have serverTables accept that
            conn.commit()
            flash('New guest has been seated.', 'success')
            return redirect(url_for('views.current'))
        
        # GET - Fetch existing seating data
        query = """
            SELECT st.*, s.name AS server_name
            FROM serversTables st
            JOIN servers s ON st.employeeID = s.employeeID;
        """
        cur.execute(query)
        parties = cur.fetchall()
        # Query pre-existing data for the form
        cur.execute("SELECT employeeID, name FROM servers;")
        employees = cur.fetchall()
        cur.execute("SELECT tableID FROM tables;")
        tables = cur.fetchall()
        cur.execute("SELECT customerID, name FROM customers;")
        customers = cur.fetchall()

        return render_template(
            'current.html', 
            parties=parties, 
            employees=employees, 
            tables=tables, 
            customers=customers
        )
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('current.html', parties=None)
    finally:
        if 'cur' in locals():
            cur.close()
        if conn and conn.is_connected():
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

@views.route('/tabs')
def tabs():
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return render_template('tabs.html', tabs=None)
    try:
        cur = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM tabs;
        """
        cur.execute(query)
        tabs = cur.fetchall()
        return render_template('tabs.html', tabs=tabs)
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('tabs.html', tabs=None)
    finally:
        if 'cur' in locals():
            cur.close()
        if conn.is_connected():
            conn.close()

@views.route('/tables')
def tables():
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return render_template('tables.html', tables=None)
    try:
        cur = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM tables;
        """
        cur.execute(query)
        tables = cur.fetchall()
        return render_template('tables.html', tables=tables)
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('tables.html', tables=None)
    finally:
        if 'cur' in locals():
            cur.close()
        if conn.is_connected():
            conn.close()

@views.route('/employees')
def employees():
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return render_template('employees.html', employees=None)
    try:
        cur = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM servers;
        """
        cur.execute(query)
        servers = cur.fetchall()
        return render_template('employees.html', employees=servers)
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('employees.html', employees=None)
    finally:
        if 'cur' in locals():
            cur.close()
        if conn.is_connected():
            conn.close()


@views.route('/customers')
def customers():
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return render_template('customers.html', customers=None)
    try:
        cur = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM customers;
        """
        cur.execute(query)
        customers = cur.fetchall()
        return render_template('customers.html', customers=customers)
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('customers.html', customers=None)
    finally:
        if 'cur' in locals():
            cur.close()
        if conn.is_connected():
            conn.close()

@views.route('/add_guest', methods=['GET', 'POST'])
def add_guest():
    if request.method == 'POST':
        # Retrieve form data (adjust field names as needed)
        guest_name = request.form.get('guest_name')
        table_number = request.form.get('table_number')
        employee_id = request.form.get('employeeID')
        
        if not guest_name or not table_number or not employee_id:
            flash('All fields are required', 'error')
            return redirect(url_for('views.add_guest'))
        
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed', 'error')
            return redirect(url_for('views.home'))
        try:
            cur = conn.cursor()
            insert_query = """
                INSERT INTO serversTables (guest_name, table_number, employeeID)
                VALUES (%s, %s, %s);
            """
            cur.execute(insert_query, (guest_name, table_number, employee_id))
            conn.commit()
            flash('New guest has been seated.', 'success')
        except Error as e:
            flash(f'Database error: {str(e)}', 'error')
        finally:
            if 'cur' in locals():
                cur.close()
            if conn.is_connected():
                conn.close()
        return redirect(url_for('views.home'))
    
    return render_template('add_guest.html')