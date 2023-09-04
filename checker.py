import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS places (
            name VARCHAR(255),
            address VARCHAR(255),
            google_map VARCHAR(255),
            latitude REAL,
            longitude REAL,
            description TEXT,
            picture VARCHAR(255)
        )
    """)
    connection.commit()


def update_table(df, engine):
    # Read "places" from DB to DataFrame
    df_db = pd.read_sql_table('places', engine)

    # Compare DataFrame, add new records to "places"
    df_new = df[~df.isin(df_db)].dropna()
    df_new.to_sql('places', engine, if_exists='append', index=False)


# Connect to Postgres
engine = create_engine('postgresql://tg_bot:qwerty@localhost/telegram_db')

# Read catalog.ods to DataFrame
df = pd.read_excel('catalog.ods')


try:
    with psycopg2.connect(
        host="localhost",
        database="telegram_db",
        user="tg_bot",
        password="qwerty"
    ) as connection:
        cursor = connection.cursor()
        create_table(cursor)
        engine = create_engine('postgresql://tg_bot:qwerty@localhost/telegram_db')
        df = pd.read_excel('catalog.ods')
        update_table(df, engine)
except (Exception, psycopg2.DatabaseError) as error:
    print("Error: %s" % error)
