import pandas as pd
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine('postgresql://tg_bot:qwerty@localhost/telegram_db')

# Read catalog.ods to DataFrame
df = pd.read_excel('catalog.ods')

# Read "places" from DB to DataFrame
df_db = pd.read_sql_table('places', engine)

# Compare DataFrame, add new records to "places"
df_new = df[~df.isin(df_db)].dropna()
df_new.to_sql('places', engine, if_exists='append', index=False)
