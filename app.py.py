#!/usr/bin/env python3
"""
ATTENDANCE SYSTEM - FLASK WEB INTERFACE

This file displays attendance records in a web browser.
Shows a monthly calendar view with user attendance data.
Users can view different months/years via URL parameters.
"""

from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime, date
import calendar
from collections import defaultdict

app = Flask(__name__)

def get_db_connection():
    """Create and return database connection"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='raspberry',  # Default RPi MySQL password
            database='attendance_db'
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def get_all_users():
    """Get all users from the database"""
    conn = get_db_connection()
    users = []
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name FROM users ORDER BY name")
            users = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching users: {e}")
        finally:
            conn.close()
    return users

@app.route('/')
def attendance_view():
    """Display attendance records in calendar view"""
    # Get month/year from URL or use current date
    year = request.args.get('year', type=int, default=datetime.now().year)
    month = request.args.get('month', type=int, default=datetime.now().month)
    
    # Validate month and year
    if not (1 <= month <= 12):
        month = datetime.now().month
    if year < 2000 or year > 2100:
        year = datetime.now().year
    
    # Calculate days in the selected month
    num_days = calendar.monthrange(year, month)[1]
    
    # Get all users first
    users = get_all_users()
    
    # Get attendance data
    attendance_data = defaultdict(lambda: defaultdict(list))
    conn = get_db_connection()
    
    if conn and users:
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Query to get attendance for the selected month
            query = """
                SELECT u.id, u.name, DATE(a.clock_in) as date, a.clock_in 
                FROM users u 
                LEFT JOIN attendance a ON u.id = a.user_id 
                AND MONTH(a.clock_in) = %s AND YEAR(a.clock_in) = %s 
                ORDER BY u.name, a.clock_in
            """
            cursor.execute(query, (month, year))
            results = cursor.fetchall()
            
            # Initialize attendance data for all users
            for user in users:
                attendance_data[user['name']] = defaultdict(list)
            
            # Populate attendance data
            for row in results:
                if row['date']:  # Only process if there's attendance data
                    date_str = row['date'].strftime('%Y-%m-%d')
                    attendance_data[row['name']][date_str].append(row['clock_in'])
            
        except Exception as e:
            print(f"Database query error: {e}")
        finally:
            conn.close()
    
    # Generate month name for display
    month_name = datetime(year, month, 1).strftime('%B %Y')
    
    return render_template('attendance.html',
                         year=year,
                         month=month,
                         month_name=month_name,
                         num_days=num_days,
                         attendance=attendance_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)