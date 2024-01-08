import json
import psycopg2
from get_nrel_api import fetch_and_insert_data

SCHEMA_NAME = "staging"

def load_credentials(file_path):
    """
    Loads credentials from a JSON file.

    Args:
        file_path (str): Path to the JSON file containing credentials.

    Returns:
        dict: Credentials.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Credentials file not found: {file_path}")
        raise
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {file_path}")
        raise

def load_config():
    with open('data_ingestion/config.json', 'r') as file:
        return json.load(file)

def create_schema(db_credentials):
    """
    Creates a schema in the PostgreSQL database.

    Args:
        db_credentials (dict): Credentials for the PostgreSQL database.
    """
    conn = None
    try:
        conn = psycopg2.connect(**db_credentials)
        cur = conn.cursor()

        create_schema_query = f"""
        CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};
        """
        cur.execute(create_schema_query)
        conn.commit()
        print(f"Schema '{SCHEMA_NAME}' created successfully.")
    except Exception as e:
        print(f"Error in creating schema: {e}")
    finally:
        if conn:
            conn.close()

def main():
    credentials_path = 'credentials.json'
    db_credentials = load_credentials(credentials_path)
    create_schema(db_credentials)

    config = load_config()

    nrel_api_key = config['NREL_API_KEY']
    fetch_and_insert_data(nrel_api_key, db_credentials, SCHEMA_NAME)

if __name__ == "__main__":
    main()
