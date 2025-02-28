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
        return render_template('current.html', tables=[], all_servers=[])
    try:
        cur = conn.cursor(dictionary=True)
        # Get all tables with their most recent server assignment
        cur.execute("""
            SELECT t.*, 
                   s.name as recent_server_name,
                   st.employeeID as recent_server_id,
                   st.dateTime as assignment_time
            FROM tables t
            LEFT JOIN (
                SELECT tableID, employeeID, dateTime
                FROM serversTables
                WHERE (tableID, dateTime) IN (
                    SELECT tableID, MAX(dateTime) as max_time
                    FROM serversTables
                    GROUP BY tableID
                )
            ) st ON t.tableID = st.tableID
            LEFT JOIN servers s ON st.employeeID = s.employeeID
            ORDER BY t.tableID;
        """)
        tables = cur.fetchall()
        
        # Continue with rest of your existing code to get assigned_servers and all_servers
        # Get all servers
        cur.execute("SELECT * FROM servers;")
        all_servers = cur.fetchall()

        # Build a dictionary mapping tableID -> list of servers assigned
        # serversTables: tableID, employeeID
        # employees: employeeID, name
        table_assignments = {}
        for t in tables:
            table_assignments[t['tableID']] = []

        cur.execute("""
            SELECT st.tableID, s.employeeID, s.name
            FROM serversTables st
            JOIN servers s ON st.employeeID = s.employeeID;
        """)
        assignments = cur.fetchall()
        for row in assignments:
            table_assignments[row['tableID']].append({
                'employeeID': row['employeeID'],
                'name': row['name']
            })

        # Attach the assigned_servers list to each table dict
        for t in tables:
            t['assigned_servers'] = table_assignments[t['tableID']]

        return render_template('current.html', tables=tables, all_servers=all_servers)
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('current.html', tables=[], all_servers=[])
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
        # Query pre-existing data for the form
        cur.execute("SELECT employeeID, name FROM servers;")
        employees = cur.fetchall()
        cur.execute("SELECT tableID FROM tables WHERE status = 'avail';")
        tables = cur.fetchall()
        cur.execute("SELECT customerID, name FROM customers;")
        customers = cur.fetchall()
        return render_template(
            'reservations.html', 
            reservations=reservations, 
            employees=employees, 
            tables=tables, 
            customers=customers
        )
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('reservations.html', parties=None)
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
        if conn and conn.is_connected():
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
        if conn and conn.is_connected():
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

@views.route('/update_status/<int:row_id>', methods=['POST'])
def update_status(row_id):
    new_status = request.form.get('new_status')
    if new_status not in ['open', 'closed']:
        flash('Invalid status value.', 'error')
        return redirect(url_for('views.current'))
    
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.current'))
    
    try:
        cur = conn.cursor(dictionary=True)
        # Get the current party row to know its tableID
        cur.execute("SELECT tableID FROM serversTables WHERE currentID = %s;", (row_id,))
        party = cur.fetchone()
        if party is None:
            flash('Party not found.', 'error')
            return redirect(url_for('views.current'))
        
        table_id = party['tableID']

        # Update the party's status
        update_query = "UPDATE serversTables SET status = %s WHERE currentID = %s;"
        cur.execute(update_query, (new_status, row_id))
        
        # Determine new table status based on party status
        # If the party is opened => table becomes 'taken'
        # If the party is closed => table becomes 'avail'
        table_status = 'taken' if new_status == 'open' else 'avail'
        cur.execute("UPDATE tables SET status = %s WHERE tableID = %s;", (table_status, table_id))
        
        conn.commit()
        flash('Status updated successfully!', 'success')
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        if 'cur' in locals():
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('views.current'))

@views.route('/delete_party/<int:row_id>', methods=['POST'])
def delete_party(row_id):
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.current'))
    try:
        cur = conn.cursor(dictionary=True)
        # Get the party to retrieve the tableID
        cur.execute("SELECT tableID FROM serversTables WHERE currentID = %s;", (row_id,))
        party = cur.fetchone()
        if party is None:
            flash('Party not found.', 'error')
            return redirect(url_for('views.current'))
        table_id = party['tableID']
        
        # Delete the party
        cur.execute("DELETE FROM serversTables WHERE currentID = %s;", (row_id,))
        # Set the table status back to available
        cur.execute("UPDATE tables SET status = 'avail' WHERE tableID = %s;", (table_id,))
        
        conn.commit()
        flash('Party deleted and table status set to available!', 'success')
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        if 'cur' in locals():
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('views.current'))

@views.route('/newEmployee', methods=['GET', 'POST'])
def newEmployee():
    if request.method == 'POST':
        name = request.form.get('employee')
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed', 'error')
            return redirect(url_for('views.newEmployee'))
        try:
            cur = conn.cursor()
            insert_query = """
                INSERT INTO servers (name)
                VALUES (%s);
            """
            cur.execute(insert_query, (name,))
            conn.commit()
            flash('New employee added successfully!', 'success')
        except Error as e:
            flash(f'Database error: {str(e)}', 'error')
        finally:
            if 'cur' in locals():
                cur.close()
            if conn and conn.is_connected():
                conn.close()
        return redirect(url_for('views.employees'))

    return render_template('newEmployee.html')

@views.route('/fireEmployee/<int:row_id>', methods=['POST'])
def fireEmployee(row_id):
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.employees'))
    try:
        cur = conn.cursor()
        delete_query = "DELETE FROM servers WHERE employeeID = %s;"
        cur.execute(delete_query, (row_id,))
        conn.commit()
        flash('Employee deleted successfully!', 'success')
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        if 'cur' in locals():
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('views.employees'))

@views.route('/newTable', methods=['GET', 'POST'])
def newTable():
    if request.method == 'POST':
        capacity = request.form.get('table')
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed', 'error')
            return redirect(url_for('views.newTable'))
        try:
            cur = conn.cursor()
            insert_query = """
                INSERT INTO tables (seatsAvail)
                VALUES (%s);
            """
            cur.execute(insert_query, (capacity,))
            conn.commit()
            flash('New table added successfully!', 'success')
        except Error as e:
            flash(f'Database error: {str(e)}', 'error')
        finally:
            if 'cur' in locals():
                cur.close()
            if conn and conn.is_connected():
                conn.close()
        return redirect(url_for('views.tables'))

    return render_template('newTable.html')

@views.route('/updateTable/<int:table_id>', methods=['POST'])
def updateTable(table_id):
    # Retrieve any updated info from request.form, e.g.
    # new_capacity = request.form.get('new_capacity')
    status = request.form.get('new_status')
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.tables'))
    try:
        cur = conn.cursor()
        update_query = "UPDATE tables SET status = %s WHERE tableID = %s;"
        # Use new_capacity or any other updated field
        cur.execute(update_query, (status, table_id))
        conn.commit()
        flash('Table updated successfully!', 'success')
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        if 'cur' in locals():
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('views.tables'))

@views.route('/deleteTable/<int:table_id>', methods=['POST'])
def deleteTable(table_id):
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.tables'))
    try:
        cur = conn.cursor()
        delete_query = "DELETE FROM tables WHERE tableID = %s;"
        cur.execute(delete_query, (table_id,))
        conn.commit()
        flash('Table deleted successfully!', 'success')
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        if 'cur' in locals():
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('views.tables'))

@views.route('/tabs', methods=['GET', 'POST'])
def tabs():
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return render_template('tabs.html', tabs=None, tables=[])
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM tabs;")
        tabs = cur.fetchall()
        # Get tables for the dropdown; you'll need to get all tables (or filter in SQL)
        cur.execute("SELECT tableID, status FROM tables;")
        tables = cur.fetchall()
        return render_template('tabs.html', tabs=tabs, tables=tables)
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('tabs.html', tabs=None, tables=[])
    finally:
        if 'cur' in locals():
            cur.close()
        if conn and conn.is_connected():
            conn.close()

@views.route('/newTab', methods=['GET', 'POST'])
def newTab():
    if request.method == 'POST':
        table_id = request.form.get('tableID')
        total = request.form.get('total')
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed', 'error')
            return redirect(url_for('views.newTab'))
        try:
            cur = conn.cursor()
            insert_query = """
                INSERT INTO tabs (tableID, total)
                VALUES (%s, %s);
            """
            cur.execute(insert_query, (table_id, total))
            conn.commit()
            flash('New tab created successfully!', 'success')
        except Error as e:
            flash(f'Database error: {str(e)}', 'error')
        finally:
            if 'cur' in locals():
                cur.close()
            if conn and conn.is_connected():
                conn.close()
        return redirect(url_for('views.tabs'))

    return render_template('newTab.html')

@views.route('/newCustomer', methods=['GET', 'POST'])
def newCustomer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('customerEmail')
        phone = request.form.get('customerPhone')
        if not name or not phone:
            flash('All fields are required', 'error')
            return redirect(url_for('views.newCustomer'))
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed', 'error')
            return redirect(url_for('views.newCustomer'))
        try:
            cur = conn.cursor()
            insert_query = """
                INSERT INTO customers (name, customerEmail, customerPhone)
                VALUES (%s, %s, %s);
            """
            cur.execute(insert_query, (name, email, phone))
            conn.commit()
            flash('New customer added successfully!', 'success')
        except Error as e:
            flash(f'Database error: {str(e)}', 'error')
        finally:
            if 'cur' in locals():
                cur.close()
            if conn and conn.is_connected():
                conn.close()
        return redirect(url_for('views.customers'))

    return render_template('newCustomer.html')

@views.route('/newReservation', methods=['GET', 'POST'])
def newReservation():
    if request.method == 'POST':
        customer_id = request.form.get('customerID')
        employee_id = request.form.get('employeeID')
        table_id = request.form.get('tableID')
        dateTime = request.form.get('resDateTime')
        status = request.form.get('status')
        if not customer_id or not employee_id or not table_id or not dateTime or not status:
            flash('All fields are required', 'error')
            return redirect(url_for('views.newReservation'))
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed', 'error')
            return redirect(url_for('views.newReservation'))
        try:
            cur = conn.cursor()
            insert_query = """
                INSERT INTO reservations (customerID, employeeID, tableID, reservationDateTime, status)
                VALUES (%s, %s, %s, %s, %s);
            """
            cur.execute(insert_query, (customer_id, employee_id, table_id, dateTime, status))
            conn.commit()
            flash('New reservation added successfully!', 'success')
        except Error as e:
            flash(f'Database error: {str(e)}', 'error')
        finally:
            if 'cur' in locals():
                cur.close()
            if conn and conn.is_connected():
                conn.close()
        return redirect(url_for('views.reservations'))

    return render_template('newReservation.html')

@views.route('/addServerToTable/<int:table_id>', methods=['POST'])
def addServerToTable(table_id):
    server_id = request.form.get('serverID')
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.current'))
    try:
        cur = conn.cursor()
        # Attempt to insert a new row
        cur.execute("""
            INSERT INTO serversTables (employeeID, tableID, status)
            VALUES (%s, %s, 'open');
        """, (server_id, table_id))
        conn.commit()
        flash('Server added to table successfully!', 'success')
    except Error as e:
        # 1062 is the MySQL error code for duplicate entry
        if e.errno == 1062:
            flash('That server is already assigned to this table!', 'error')
        else:
            flash(f'Database error: {str(e)}', 'error')
    finally:
        if 'cur' in locals():
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('views.current'))

@views.route('/removeServerFromTable/<int:table_id>', methods=['POST'])
def removeServerFromTable(table_id):
    server_id = request.form.get('serverID')
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.current'))
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM serversTables WHERE employeeID = %s AND tableID = %s;", (server_id, table_id))
        conn.commit()
        flash('Server removed from table.', 'success')
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        if 'cur' in locals():
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('views.current'))

@views.route('/toggleTableStatus/<int:table_id>', methods=['POST'])
def toggleTableStatus(table_id):
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.current'))
    try:
        # Create cursor with dictionary=True
        cur = conn.cursor(dictionary=True)
        
        # First get current status
        cur.execute("SELECT status FROM tables WHERE tableID = %s", (table_id,))
        current_status = cur.fetchone()['status']
        
        # Toggle the status
        new_status = 'taken' if current_status == 'avail' else 'avail'
        
        # Update the status
        cur.execute("UPDATE tables SET status = %s WHERE tableID = %s", (new_status, table_id))
        conn.commit()
        flash(f'Table {table_id} status updated to {new_status}!', 'success')
    except Error as e:
        flash(f'Database error: {str(e)}', 'danger')
    finally:
        if 'cur' in locals():
            cur.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for('views.current'))