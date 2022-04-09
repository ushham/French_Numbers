import numpy as np
import control as ct
from datetime import datetime
import json
import os
import visualisation

class DataAnalysis:
    sec_to_hr = 3600
    sec_to_min = 60

    def __init__(self) -> None:
        self.data_path = ct.data_save_folder_path
        self.combined_file = self.data_path + '/CombinedData.json'

        self.get_data()

    @staticmethod
    def utc_is_today(timestamp):
        date_ts = datetime.fromtimestamp(timestamp)
        today_date = datetime.today()
        return (today_date - date_ts).days < 1

    @staticmethod
    def incorrect_number_locations(num_asked, num_answerwed):
        error_spots = list()

        len_num = len(str(num_asked))
        for i in range(len_num):
            division_num = 10 ** i
            int_ask = (num_asked // division_num) % 10
            int_ans = (num_answerwed // division_num) % 10
            
            if int_ask != int_ans:
                # Add a tuple of number that didnt get, and the base
                error_row = (int_ask, i)
                error_spots.append(error_row)
        
        return error_spots

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

    def make_hist_data(self):
        max_num = self.max_number_asked()
        num_digits = len(str(max_num))

        # This is an array that holds the number of times a digit from 1-10 was wrong for each base (1, 10s, 100s, ...)
        hist_arr = np.zeros((10, num_digits))

        for ln in self.full_data:
            for atp in ln["Runs"]:
                for gs in atp["Guesses"]:
                    error_list = self.incorrect_number_locations(atp["Number"], gs)
                    
                    for ele in error_list:
                        hist_arr[ele[0], ele[1]] += 1
        
        vert_sum = np.sum(hist_arr, axis=0)
        hist_arr = hist_arr / vert_sum

        return hist_arr

    def print_stats(self):
        total_run_time = 0
        total_time_today = 0

        #### Calculate run times #####
        for ln in self.full_data:
            #Total Run time (seconds):
            total_run_time += float(ln["Run_time"])
            if self.utc_is_today(float(ln["Start_time"])):
                total_time_today += float(ln["Run_time"])
            
        total_run_time = str(round(total_run_time / self.sec_to_hr, 2)) + " Hours"
        total_time_today = str(round(total_time_today / self.sec_to_min, 2)) + " Minutes"

        #### Calculate errors ####
        error_count_today = 0
        error_count_total = 0

        total_atempts = 0
        today_atempts = 0

        for ln in self.full_data:
            for atp in ln["Runs"]:
                error_count_total += int(atp["Attemps"])
                total_atempts += 1
                if self.utc_is_today(float(ln["Start_time"])):
                    error_count_today += int(atp["Attemps"])
                    today_atempts += 1

        print("Total time spent today (mins): " + total_time_today)
        print("Total time using the app (hrs): " + total_run_time)
        print("Today " + str(round(error_count_today / today_atempts * 100, 0)) + "% of your answers were wrong, on average your mistake ratio is " + str(round(error_count_total / total_atempts * 100, 0)) + "%")



if __name__ == "__main__":
    x = DataAnalysis()
    err_mat = x.make_error_mat()
    visualisation.matrix_heat_map(err_mat)
    # print(x.make_hist_data())
    # visualisation.histogram_errors(x.make_hist_data())
