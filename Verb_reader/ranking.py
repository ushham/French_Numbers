import pandas as pd
import control as ct
import numpy as np
from datetime import datetime

def update_score(user_score, row):
    # This uses the Supermemo program https://www.supermemo.com/en/archives1990-2015/english/ol/sm2

    last_score = row[3]
    num_reviews = row[4]
    ef = row[5]

    def update_ef():
        return max(1.3, ef + (0.1 - (5 - user_score) * (0.08 + (5 - user_score) * 0.02)))
    
    if num_reviews == 0 or user_score < 3:
        new_score = 1
        new_ef = ef

    elif last_score == 1:
        new_score = 6
        new_ef = update_ef()

    else: 
        new_score = last_score * ef
        new_ef = update_ef()

    row[3] = new_score
    row[4] += 1
    row[5] = new_ef
    row[6] = datetime.today()


    return row

def return_index(df):
    #Find minimum number in score
    df = df[df.score == np.min(df.score)]

    row = np.random.choice(df.index.values, 1)
    return df.loc[row].values.tolist()[0], row


if __name__ == "__main__":
    import data_management as dm
    df = dm.read_database()
    print(return_index(df))