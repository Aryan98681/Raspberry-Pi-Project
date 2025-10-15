#!/usr/bin/env python3
"""
ATTENDANCE SYSTEM - CORE MANAGER

This script handles all attendance system operations:
- Adding new users to the database
- Recording attendance check-ins
- Clearing LCD display (if connected)
- Generating attendance reports

Usage: python3 attendance_manager.py [command] [arguments]
"""

import mysql.connector
from datetime import datetime
import sys

class AttendanceManager:
    """Main class that handles all attendance system operations"""
    
    def __init__(self):
        """Initialize database connection"""
        try:
            self.db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='raspberry',  # Default RPi MySQL password
                database='attendance_db'
            )
            print("Database connected successfully")
        except Exception as e:
            print(f"Database connection failed: {e}")
    
    def add_user(self, name):
        """Add a new user to the system"""
        cursor = self.db.cursor()
        try:
            cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            self.db.commit()
            print(f"✓ User '{name}' added successfully!")
            return True
        except Exception as e:
            print(f"✗ Error adding user: {e}")
            return False
    
    def check_attendance(self, user_id):
        """Record attendance check-in for a user"""
        cursor = self.db.cursor()
        try:
            cursor.execute("INSERT INTO attendance (user_id, clock_in) VALUES (%s, NOW())", (user_id,))
            self.db.commit()
            print(f"✓ Attendance recorded for user ID {user_id} at {datetime.now()}")
            return True
        except Exception as e:
            print(f"✗ Error recording attendance: {e}")
            return False
    
    def clear_lcd(self):
        """Clear the LCD display (placeholder for hardware integration)"""
        # This would interface with actual LCD hardware
        # For now, just print a message
        print("✓ LCD display cleared")
        # Actual implementation might look like:
        # lcd.clear()
        # lcd.message("")
        return True
    
    def print_report(self, user_id=None):
        """Generate and display attendance reports"""
        cursor = self.db.cursor()
        
        try:
            if user_id:
                # Report for specific user
                query = """
                    SELECT u.name, DATE(a.clock_in), TIME(a.clock_in) 
                    FROM attendance a 
                    JOIN users u ON a.user_id = u.id 
                    WHERE u.id = %s 
                    ORDER BY a.clock_in DESC
                """
                cursor.execute(query, (user_id,))
                print(f"\n--- Attendance Report for User ID {user_id} ---")
            else:
                # Report for all users
                query = """
                    SELECT u.name, DATE(a.clock_in), TIME(a.clock_in) 
                    FROM attendance a 
                    JOIN users u ON a.user_id = u.id 
                    ORDER BY u.name, a.clock_in DESC
                """
                cursor.execute(query)
                print("\n--- Full Attendance Report ---")
            
            # Display results
            records = cursor.fetchall()
            for name, date, time in records:
                print(f"{name}: {date} at {time}")
                
            print(f"Total records: {len(records)}")
            return True
            
        except Exception as e:
            print(f"✗ Error generating report: {e}")
            return False

def main():
    """Main function - handle command line arguments"""
    manager = AttendanceManager()
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    
    if command == "add_user" and len(sys.argv) > 2:
        manager.add_user(sys.argv[2])
    elif command == "check_attendance" and len(sys.argv) > 2:
        manager.check_attendance(sys.argv[2])
    elif command == "clear_lcd":
        manager.clear_lcd()
    elif command == "report":
        user_id = sys.argv[2] if len(sys.argv) > 2 else None
        manager.print_report(user_id)
    else:
        show_help()

def show_help():
    """Display usage instructions"""
    print("""
Attendance System Manager - Usage:
    
python3 attendance_manager.py add_user "John Doe"      # Add new user
python3 attendance_manager.py check_attendance 5       # Record attendance for user ID 5
python3 attendance_manager.py clear_lcd               # Clear LCD display
python3 attendance_manager.py report                  # Show report for all users
python3 attendance_manager.py report 5                # Show report for user ID 5
    """)

if __name__ == "__main__":
    main()