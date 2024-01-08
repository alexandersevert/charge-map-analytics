"""
This module is responsible for fetching electric vehicle (EV) charging station data
from the National Renewable Energy Laboratory (NREL) API and inserting it into a
PostgreSQL database. It handles the creation of the database table for storing the
data and ensures that the data is correctly inserted.

The module defines constants for the database table name and the request timeout
value, and includes functions for each step of the process: fetching data from the
API, creating the database table, and inserting the data into the database.
"""

import pandas as pd
import requests
import psycopg2
from tqdm import tqdm
from uszipcode import SearchEngine

RAW_TABLE_NAME = "nrel_api_raw"
REQUEST_TIMEOUT = 10


def api_to_df(zip_codes, api_key, endpoint, batch_id):
    """
    Fetches data from the NREL API for a given list of zip codes.

    Args:
        zip_codes (list): List of zip codes to query in the API.
        api_key (str): API key for the NREL API.
        endpoint (str): The endpoint of the data to be fetched.
        batch_id (int): Batch ID for the current request.

    Returns:
        pandas.DataFrame: Data fetched from the API.
    """
    zip_codes_str = ",".join(zip_codes)
    url = (
        f"https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key={api_key}"
        + f"&fuel_type=ELEC&zip={zip_codes_str}"
    )

    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    json_data = response.json()
    data_df = pd.DataFrame(json_data[endpoint])

    if not data_df.empty:
        data_df["batch_id"] = batch_id
        # Specify the columns you want to export
        export_columns = [
            "access_code",
            "access_detail_code",
            "date_last_confirmed",
            "expected_date",
            "fuel_type_code",
            "groups_with_access_code",
            "id",
            "open_date",
            "owner_type_code",
            "status_code",
            "updated_at",
            "facility_type",
            "geocode_status",
            "latitude",
            "longitude",
            "state",
            "zip",
            "country",
            "ev_dc_fast_num",
            "ev_level1_evse_num",
            "ev_level2_evse_num",
            "ev_network",
            "ev_renewable_source",
            "nps_unit_name",
            "batch_id",
        ]
        export_df = data_df[export_columns]
    else:
        export_df = pd.DataFrame()

    return export_df


def create_table(db_credentials, schema_name):
    """
    Creates a table in the PostgreSQL database to store NREL API data.

    Args:
        db_credentials (dict): Credentials for the PostgreSQL database.
        schema_name (str): Name of the database schema to use.
    """
    conn = None
    try:
        conn = psycopg2.connect(**db_credentials)
        cur = conn.cursor()

        create_table_query = f"""
        DROP TABLE IF EXISTS {schema_name}.{RAW_TABLE_NAME};
        CREATE TABLE IF NOT EXISTS {schema_name}.{RAW_TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            access_code VARCHAR(255),
            access_detail_code VARCHAR(255),
            date_last_confirmed DATE,
            expected_date DATE,
            fuel_type_code VARCHAR(255),
            groups_with_access_code VARCHAR(255),
            open_date DATE,
            owner_type_code VARCHAR(255),
            status_code VARCHAR(255),
            updated_at TIMESTAMP,
            facility_type VARCHAR(255),
            geocode_status VARCHAR(255),
            latitude FLOAT,
            longitude FLOAT,
            state VARCHAR(255),
            zip VARCHAR(255),
            country VARCHAR(255),
            ev_dc_fast_num FLOAT,
            ev_level1_evse_num FLOAT,
            ev_level2_evse_num FLOAT,
            ev_network VARCHAR(255),
            ev_renewable_source VARCHAR(255),
            nps_unit_name VARCHAR(255),
            batch_id INT
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        print(f"Table {schema_name}.{RAW_TABLE_NAME}' created successfully.")
    except Exception as e:
        print(f"Error in creating table: {e}")
    finally:
        if conn:
            conn.close()


def insert_data_to_postgres(data_df, db_credentials, schema_name):
    """
    Inserts data into the NREL API raw data table in the PostgreSQL database.

    Args:
        data_df (pd.DataFrame): DataFrame containing the data to insert.
        db_credentials (dict): Credentials for the PostgreSQL database.
        schema_name (str): Name of the database schema to use.
    """
    conn = None
    try:
        conn = psycopg2.connect(**db_credentials)
        cur = conn.cursor()

        # Construct the INSERT query
        columns = data_df.columns.tolist()
        values_placeholder = ", ".join(["%s"] * len(columns))
        insert_query = f"INSERT INTO {schema_name}.{RAW_TABLE_NAME} ({', '.join(columns)}) VALUES ({values_placeholder})"

        # Insert data
        for row in data_df.itertuples(index=False):
            try:
                cur.execute(insert_query, row)
            except Exception as e:
                print(f"Error inserting row: {row}")
                raise e

        conn.commit()
    except Exception as e:
        print(f"Error in inserting data to PostgreSQL: {e} {row}")
    finally:
        if conn:
            conn.close()


def fetch_and_insert_data(api_key, db_credentials, schema_name):
    """
    Fetches EV charging station data from the NREL API and inserts it into the database.

    Args:
        api_key (str): API key for the NREL API.
        db_credentials (dict): Credentials for the PostgreSQL database.
        schema_name (str): Name of the database schema to use.
    """
    create_table(db_credentials, schema_name)

    search = SearchEngine()
    all_zip_codes = [
        str(zipcode.zipcode) for zipcode in search.by_pattern("", returns=100000)
    ]

    chunk_size = 50
    zip_code_chunks = [
        all_zip_codes[i : i + chunk_size]
        for i in range(0, len(all_zip_codes), chunk_size)
    ]

    for batch_id in tqdm(range(len(zip_code_chunks)), desc="Processing batches"):
        zip_codes_chunk = zip_code_chunks[batch_id]
        data_df = api_to_df(zip_codes_chunk, api_key, "fuel_stations", batch_id)
        if not data_df.empty:
            insert_data_to_postgres(data_df, db_credentials, schema_name)
