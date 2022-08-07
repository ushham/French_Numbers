from operator import index
from time import time
import pandas as pd
from datetime import datetime

import control as ct

def read_new_data(new_file, database):
    # This function takes a csv that contains the new verbs and adds the verbs to the existing database
    new_data = pd.read_csv(new_file)


def backup_database(database):
    # Backs up the database incase overwritten due to my bad code
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    database.to_csv(ct.database_backup_folder + str(time_stamp) + '.csv', index=False)
    return 0



print(backup_database(1))