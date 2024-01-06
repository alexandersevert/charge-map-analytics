"""
This script generates a 'credentials.json' file for storing database connection details.
The generated file includes the following keys:
- dbname: Name of the database
- user: Username for the database
- password: Password for the database
- host: Host address of the database
- port: Port number for the database connection

Usage:
    Run the script and follow the prompts to enter your database credentials.
    python create_credentials_json.py

Security Note:
    The 'credentials.json' file will contain sensitive information. Ensure it is properly
    secured and not checked into version control.
"""

import json

def create_credentials_file():
    """
    Prompts the user for database credentials and writes them to 'credentials.json'.
    The file is created with human-readable formatting.
    """
    print("Please enter your database credentials.")
    credentials = {
        "dbname": input("Enter the database name: "),
        "user": input("Enter the username: "),
        "password": input("Enter the password: "),
        "host": input("Enter the host address: "),
        "port": input("Enter the port number: "),
    }

    try:
        with open("credentials.json", "w", encoding="utf-8") as file:
            json.dump(credentials, file, indent=4)
        print("credentials.json has been created successfully.")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    create_credentials_file()
