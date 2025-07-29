import pandas as pd
import os 
from sqlalchemy import create_engine 
import logging 
import time

# Logging setup
logging.basicConfig(
    filename="logs/ingestion_db.log",   # Removed extra dot in filename
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# Create engine
engine = create_engine('sqlite:///warehouse.db')

# Function to ingest dataframe into the database
def ingest_db(df, table_name, engine):
    '''This function will ingest the dataframe into a database table'''
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

# Function to load and ingest CSV files
def load_raw_data():
    '''This function will load the CSVs as dataframes and ingest into the DB'''
    start = time.time()
    
    for file in os.listdir('.'):
        if file.endswith('.csv'):
            filepath = os.path.join('.', file)
            df = pd.read_csv(filepath)
            print(df.shape)
            ingest_db(df, file[:-4], engine)

    end = time.time()
    total_time = (end - start) / 60
    logging.info('-------Ingestion Complete-------')
    logging.info(f'Total Time Taken: {total_time:.2f} minutes')

# Correct __name__ check
if __name__ == '__main__':
    load_raw_data()

