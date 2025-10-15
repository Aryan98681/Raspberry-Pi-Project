#!/bin/bash
#
# ATTENDANCE SYSTEM - MASTER CONTROL SCRIPT
#
# This script provides a simple command-line interface for the attendance system.
# It acts as a wrapper for the Python manager script with easy-to-remember commands.
#

# Display help if no arguments provided
if [ $# -eq 0 ]; then
    echo "Attendance System - Command Line Interface"
    echo "=========================================="
    echo ""
    echo "Usage: $0 [command] [arguments]"
    echo ""
    echo "Commands:"
    echo "  add_user \"Name\"    - Add a new user to the system"
    echo "  check USER_ID      - Record attendance for a user"
    echo "  clear_lcd          - Clear the LCD display"
    echo "  report [USER_ID]   - Generate attendance report"
    echo "  web               - Start the web interface"
    echo "  help               - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 add_user \"Alice Smith\""
    echo "  $0 check 5"
    echo "  $0 report"
    echo "  $0 web"
    echo ""
    exit 1
fi

# Handle different commands
case $1 in
    "add_user")
        if [ -z "$2" ]; then
            echo "Error: Please provide a user name in quotes"
            echo "Example: $0 add_user \"John Doe\""
            exit 1
        fi
        python3 attendance_manager.py add_user "$2"
        ;;
        
    "check")
        if [ -z "$2" ]; then
            echo "Error: Please provide a user ID"
            echo "Example: $0 check 5"
            exit 1
        fi
        python3 attendance_manager.py check_attendance "$2"
        ;;
        
    "clear_lcd")
        python3 attendance_manager.py clear_lcd
        ;;
        
    "report")
        python3 attendance_manager.py report "$2"
        ;;
        
    "web")
        echo "Starting web interface on http://localhost:5000"
        python3 app.py
        ;;
        
    "help")
        echo "See available commands above."
        ;;
        
    *)
        echo "Error: Unknown command '$1'"
        echo "Use '$0 help' for available commands."
        exit 1
        ;;
esac