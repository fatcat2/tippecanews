import os

from pg8000 import Connection, connect


def get_database_connection() -> Connection:
    """Helper function to get the database connection

    Params:
        database (str): the database you want to retrieve data from.

    Returns:
        A database connection object to interact with.
    """
    try:
        conn = connect(
            os.getenv("POSTGRES_USERNAME"),
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DATABASE"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

        return conn
    except Exception as e:
        print(e)
        return None
