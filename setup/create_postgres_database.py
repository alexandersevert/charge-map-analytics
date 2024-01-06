"""
This script reads database connection details from 'credentials.json' and
creates a new PostgreSQL database. The user must have the necessary permissions
to create a database.

Usage:
    Run the script. Ensure 'credentials.json' is present.
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

def create_database(creds):
    """
    Creates a PostgreSQL database using provided credentials.

    Args:
        creds (dict): Database credentials.
    """
    try:
        conn = psycopg2.connect(dbname="postgres", user=creds["user"],
                                password=creds["password"], host=creds["host"], port=creds["port"])
        conn.autocommit = True
    except psycopg2.OperationalError as e:
        print(f"Unable to connect to the database server: {e}")
        return

    with conn.cursor() as cur:
        try:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(creds["dbname"])))
            print(f"Database '{creds['dbname']}' created successfully.")
        except psycopg2.Error as e:
            print(f"Error creating database '{creds['dbname']}': {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    credentials = load_credentials('credentials.json')
    create_database(credentials)
