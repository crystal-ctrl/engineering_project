import pandas as pd
from sodapy import Socrata
from sqlalchemy import create_engine

# Get cases df from API
case_client = Socrata("data.virginia.gov",
                 "NngCh4cIYdkg2eNP2DqZs1iAq",
                 username="chiting1013@gmail.com",
                 password="W4eK8vAE8MkevAp")

cases = case_client.get("bre9-aqqr", limit=100000)
case_df = pd.DataFrame.from_records(cases)

# Get vaccines df from API
vax_client = Socrata("data.virginia.gov",
                 "NngCh4cIYdkg2eNP2DqZs1iAq",
                 username="chiting1013@gmail.com",
                 password="W4eK8vAE8MkevAp",
                timeout=10)
vaccines = vax_client.get("28k2-x2rj", limit=500000)
vaccine_df = pd.DataFrame.from_records(vaccines)


# Create an SQLite database
engine = create_engine('sqlite:///covid.db')

# create table for each df in DB
case_df.to_sql("case_data", con=engine, if_exists='replace', index=False)
vaccine_df.to_sql("vaccine_data", con=engine, if_exists='replace', index=False)
