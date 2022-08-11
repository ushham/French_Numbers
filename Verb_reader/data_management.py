import pandas as pd
from datetime import datetime

import control as ct

def read_database():
    return pd.read_csv(ct.database_loc)

def save_database(df):
    df.to_csv(ct.database_loc, index=False)
    return 0

def read_new_data(new_file=ct.new_data, database=ct.database_loc):
    # This function takes a csv that contains the new verbs and adds the verbs to the existing database
    new_data = pd.read_csv(new_file)
    data_base = pd.read_csv(database)

    # Copy the column names and populate the new data with the same columns
    cols = data_base.columns
    recall_name = cols[3]
    recall_num = cols[4]
    ef_score = cols[5]
    review_date = cols[6]

    new_data[recall_name] = 0
    new_data[recall_num] = 0
    new_data[ef_score] = 2.5
    new_data[review_date] = ''

    data_base = pd.concat([data_base, new_data], ignore_index=True)
    return data_base

def backup_database(database):
    # Backs up the database incase overwritten due to my bad code
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    database.to_csv(ct.database_backup_folder + str(time_stamp) + '.csv', index=False)
    return 0

def update_dataframe(db, row, index):
    db.iloc[index, :] = row
    return db

if __name__ == "__main__":
    db = "/Users/ushhamilton/Documents/03_Programming/Python/french_nums/Verb_reader/csv_store/database.csv"
    new = "/Users/ushhamilton/Documents/03_Programming/Python/french_nums/Verb_reader/csv_store/new.csv"

    print(read_new_data(new, db))