"""
This script reads database connection details from 'credentials.json' and
creates a new PostgreSQL database. The user must have the necessary permissions
to create a database. The name of the new database should be provided when
prompted.

Usage:
    Run the script and follow the prompts. Ensure 'credentials.json' is present.
    python create_postgres_db.py

Security Note:
    Handle 'credentials.json' securely as it contains sensitive information.
"""

import json
import sys
import psycopg2
from psycopg2 import sql

def load_credentials(file_path):
    """
    Loads database credentials from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing credentials.

    Returns:
        dict: Database credentials.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Credentials file not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {file_path}")
        sys.exit(1)

def create_database(creds, db_name):
    """
    Creates a PostgreSQL database using provided credentials.

    Args:
        creds (dict): Database credentials.
        db_name (str): Name of the database to be created.
    """
    try:
        conn = psycopg2.connect(dbname=creds["dbname"], user=creds["user"],
                                password=creds["password"], host=creds["host"], port=creds["port"])
        conn.autocommit = True
    except psycopg2.OperationalError as e:
        print(f"Unable to connect to the database server: {e}")
        return

    with conn.cursor() as cur:
        try:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database '{db_name}' created successfully.")
        except psycopg2.Error as e:
            print(f"Error creating database '{db_name}': {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    credentials = load_credentials('credentials.json')
    new_db_name = input("Enter the name of the new database to create: ").strip()

    if new_db_name:
        create_database(credentials, new_db_name)
    else:
        print("No database name provided. Exiting.")
