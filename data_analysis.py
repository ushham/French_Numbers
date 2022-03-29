import numpy as np
import control as ct
from datetime import datetime
import json
import os
import visualisation

class DataAnalysis:
    sec_to_hr = 3600
    def __init__(self) -> None:
        self.data_path = ct.data_save_folder_path
        self.combined_file = self.data_path + '/CombinedData.json'

        self.get_data()

    @staticmethod
    def utc_is_today(timestamp):
        date_ts = datetime.fromtimestamp(timestamp)
        today_date = datetime.today()
        return (today_date - date_ts).days < 1

    def combine_data(self):
        json_hold = list()
        files_to_read = os.listdir(self.data_path)
        for f in files_to_read:
            file_name = os.path.splitext(f)
            if file_name[1] == ct.data_file_ext and file_name[0] != "CombinedData":
                 data_ext = open(self.data_path + "/" + f)
                 data = json.load(data_ext)
                 json_hold.append(data)

        with open(self.combined_file, 'w') as f:
            json.dump(json_hold, f, indent=4)

        return 0

    def get_data(self):
        self.combine_data()

        data_ext = open(self.combined_file)
        self.full_data = json.load(data_ext)
        return 0

    
    def max_number_asked(self):
        nums = list()
        for ln in self.full_data:
            for sub_ln in ln["Runs"]:
                nums.append(sub_ln["Number"])
        return max(nums)

    def max_number_answered(self):
        nums = list()
        for ln in self.full_data:
            for sub_ln in ln["Runs"]:
                nums.extend(sub_ln["Guesses"])
        return max(nums)

    def make_error_mat(self):
        rows = self.max_number_asked()
        cols = self.max_number_answered()

        error_mat = np.zeros((rows, cols))

        #Setting the asked column to one, means that we are assuming every number has been asked once.
        #However for our use this is not a problem if a number was never asked, that row in the error matrix
        #Has to be 0 by definition, so we will be dividing 0 / 1, not leading to an incorrect result.
        asked_col = np.ones((rows))

        for ln in self.full_data:
            for sub_ln in ln["Runs"]:
                i = sub_ln["Number"]
                for j in sub_ln["Guesses"]:
                    if i != j:
                        asked_col[i - 1] += 1
                        error_mat[i-1, j-1] += 1

        asked_mat = np.tile(asked_col, (cols, 1))
        error_mat = error_mat / asked_mat.T

        return error_mat

    def print_stats(self):
        total_run_time = 0
        total_time_today = 0

        for ln in self.full_data:
            #Total Run time (seconds):
            total_run_time += float(ln["Run_time"])
            if self.utc_is_today(float(ln["Start_time"])):
                total_time_today += float(ln["Run_time"])
        
        return total_run_time / self.sec_to_hr, total_time_today / self.sec_to_hr



if __name__ == "__main__":
    x = DataAnalysis()
    err_mat = x.make_error_mat()
    visualisation.matrix_heat_map(err_mat, [0, 200], [0, 200])
    print(x.print_stats())