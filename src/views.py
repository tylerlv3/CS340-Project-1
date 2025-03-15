from flask import Blueprint, render_template, flash, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool
import os
from dotenv import load_dotenv

# Create Blueprint
views = Blueprint('views', __name__)

load_dotenv()

# Global connection pool
dbconfig = {
    "host": os.getenv('DB_HOST', 'localhost'),
    "database": os.getenv('DB_NAME'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD')
}

# Initialize connection pool (create this once, not for each request)
try:
    connection_pool = MySQLConnectionPool(pool_name="mypool",
                                         pool_size=5,
                                         **dbconfig)
    print("Connection pool created successfully")
except Error as e:
    print(f"Error creating connection pool: {e}")
    connection_pool = None

def get_db_connection():
    try:
        if connection_pool:
            # Get connection from pool
            conn = connection_pool.get_connection()
            return conn
        else:
            # Fallback to direct connection if pool creation failed
            conn = mysql.connector.connect(**dbconfig)
            return conn
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

# Helper function to safely close connections from the pool
def close_connection(conn):
    if conn:
        try:
            conn.close()
        except Error as e:
            print(f"Error closing connection: {e}")

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
        # Optimized query with proper indexing - recommend adding indexes on tableID columns
        cur.execute("""
            SELECT t.*, 
                   s.name as recent_server_name,
                   st.employeeID as recent_server_id,
                   st.dateTime as assignment_time
            FROM tables t
            LEFT JOIN (
                SELECT st1.tableID, st1.employeeID, st1.dateTime
                FROM serversTables st1
                INNER JOIN (
                    SELECT tableID, MAX(dateTime) as max_time
                    FROM serversTables
                    GROUP BY tableID
                ) st2 ON st1.tableID = st2.tableID AND st1.dateTime = st2.max_time
            ) st ON t.tableID = st.tableID
            LEFT JOIN servers s ON st.employeeID = s.employeeID
            ORDER BY t.tableID;
        """)
        tables = cur.fetchall()
        
        # Get all servers in a single query for better performance
        cur.execute("SELECT * FROM servers;")
        all_servers = cur.fetchall()

        # Optimize this with a single JOIN query instead of multiple queries
        cur.execute("""
            SELECT st.tableID, s.employeeID, s.name
            FROM serversTables st
            JOIN servers s ON st.employeeID = s.employeeID
            ORDER BY st.tableID;
        """)
        
        # Build assignment dictionary
        assignments = cur.fetchall()
        table_assignments = {}
        for t in tables:
            table_assignments[t['tableID']] = []
            
        for row in assignments:
            if row['tableID'] in table_assignments:
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
        close_connection(conn)  # Use our safe closing function

@views.route('/reservations')
def reservations():
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return render_template('reservations.html', reservations=None, employees=None, tables=None, customers=None)
    try:
        cur = conn.cursor(dictionary=True)
        
        # Fetch reservations data
        cur.execute("""
            SELECT r.*, s.name as server_name, c.name as customer_name 
            FROM reservations r 
            JOIN servers s ON r.employeeID = s.employeeID 
            JOIN customers c ON r.customerID = c.customerID
            ORDER BY r.reservationDateTime;
        """)
        reservations = cur.fetchall()
        
        # Create separate cursors for additional queries to avoid "Commands out of sync" error
        cur.close()
        
        # Fetch employees
        cur2 = conn.cursor(dictionary=True)
        cur2.execute("SELECT employeeID, name FROM servers ORDER BY name;")
        employees = cur2.fetchall()
        cur2.close()
        
        # Fetch tables
        cur3 = conn.cursor(dictionary=True)
        cur3.execute("SELECT tableID FROM tables ORDER BY tableID;")
        tables = cur3.fetchall()
        cur3.close()
        
        # Fetch customers
        cur4 = conn.cursor(dictionary=True)
        cur4.execute("SELECT customerID, name FROM customers ORDER BY name;")
        customers = cur4.fetchall()
        cur4.close()
        
        return render_template(
            'reservations.html', 
            reservations=reservations, 
            employees=employees, 
            tables=tables, 
            customers=customers
        )
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('reservations.html', reservations=None, employees=None, tables=None, customers=None)
    finally:
        close_connection(conn)  # Use our safe closing function

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
        close_connection(conn)  # Use our safe closing function

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
        close_connection(conn)  # Use our safe closing function

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
        close_connection(conn)  # Use our safe closing function

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
            close_connection(conn)  # Use our safe closing function
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
        close_connection(conn)  # Use our safe closing function
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
        close_connection(conn)  # Use our safe closing function
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
            close_connection(conn)  # Use our safe closing function
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
        close_connection(conn)  # Use our safe closing function
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
            close_connection(conn)  # Use our safe closing function
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
        close_connection(conn)  # Use our safe closing function
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
        close_connection(conn)  # Use our safe closing function
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
        close_connection(conn)  # Use our safe closing function

@views.route('/newTab', methods=['GET', 'POST'])
def newTab():
    if request.method == 'POST':
        table_id = request.form.get('tableID')
        total = request.form.get('total')
        
        # Validate total before connecting to database
        try:
            totalValue = float(total)
            if totalValue < 0:
                flash('Total cannot be negative', 'error')
                return redirect(url_for('views.tabs'))
        except ValueError:
            flash('Invalid total value', 'error')
            return redirect(url_for('views.tabs'))
        
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed', 'error')
            return redirect(url_for('views.tabs'))
            
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
            close_connection(conn)  # Use our safe closing function
        return redirect(url_for('views.tabs'))

    return render_template('newTab.html')

@views.route('/updateTab/<int:tab_id>', methods=['POST'])
def updateTab(tab_id):
    total = request.form.get('total')
    
    # Validate total before connecting to database
    try:
        totalValue = float(total)
        if totalValue < 0:
            flash('Total cannot be negative', 'error')
            return redirect(url_for('views.tabs'))
    except ValueError:
        flash('Invalid total value', 'error')
        return redirect(url_for('views.tabs'))
    
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.tabs'))
        
    try:
        cur = conn.cursor()
        update_query = """
            UPDATE tabs 
            SET total = %s
            WHERE tabID = %s;
        """
        cur.execute(update_query, (total, tab_id))
        conn.commit()
        flash('Tab updated successfully!', 'success')
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        if 'cur' in locals():
            cur.close()
        close_connection(conn)  # Use our safe closing function
    return redirect(url_for('views.tabs'))

@views.route('/deleteTab/<int:tab_id>', methods=['POST'])
def deleteTab(tab_id):
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.tabs'))
        
    try:
        cur = conn.cursor()
        delete_query = """
            DELETE FROM tabs 
            WHERE tabID = %s;
        """
        cur.execute(delete_query, (tab_id,))
        conn.commit()
        flash('Tab deleted successfully!', 'success')
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        if 'cur' in locals():
            cur.close()
        close_connection(conn)  # Use our safe closing function
    return redirect(url_for('views.tabs'))

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
            close_connection(conn)  # Use our safe closing function
        return redirect(url_for('views.customers'))

    return render_template('newCustomer.html')

@views.route('/deleteCustomer/<int:customer_id>', methods=['POST'])
def deleteCustomer(customer_id):
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.customers'))
    try:
        cur = conn.cursor()
        delete_query = "DELETE FROM customers WHERE customerID = %s;"
        cur.execute(delete_query, (customer_id,))
        conn.commit()
        flash('Customer deleted successfully!', 'success')
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        if 'cur' in locals():
            cur.close()
        close_connection(conn)  # Use our safe closing function
    return redirect(url_for('views.customers'))

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
            cur = conn.cursor(dictionary=True)
            
            # Check for existing reservations at the same time and table
            check_query = """
                SELECT COUNT(*) as count FROM reservations 
                WHERE tableID = %s AND reservationDateTime = %s
            """
            cur.execute(check_query, (table_id, dateTime))
            result = cur.fetchone()
            
            if result['count'] > 0:
                flash('A reservation already exists for this table at the selected time', 'error')
                return redirect(url_for('views.newReservation'))
                
            # If no conflict, proceed with insertion
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
            close_connection(conn)  # Use our safe closing function
        return redirect(url_for('views.reservations'))

    return render_template('newReservation.html')

@views.route('/deleteReservation/<int:reservation_id>', methods=['POST'])
def deleteReservation(reservation_id):
    conn = get_db_connection()
    if conn is None:
        flash('Database connection failed', 'error')
        return redirect(url_for('views.reservations'))
    try:
        cur = conn.cursor()
        delete_query = "DELETE FROM reservations WHERE reservationID = %s;"
        cur.execute(delete_query, (reservation_id,))
        conn.commit()
        flash('Reservation deleted successfully!', 'success')
    except Error as e:
        flash(f'Database error: {str(e)}', 'error')
    finally:
        if 'cur' in locals():
            cur.close()
        close_connection(conn)  # Use our safe closing function
    return redirect(url_for('views.reservations'))

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
        close_connection(conn)  # Use our safe closing function
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
        close_connection(conn)  # Use our safe closing function
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
        close_connection(conn)  # Use our safe closing function
    return redirect(url_for('views.current'))