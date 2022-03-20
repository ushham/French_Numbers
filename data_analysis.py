import numpy as np
import control as ct
import json
import os
import visualisation

class DataAnalysis:
    
    def __init__(self) -> None:
        self.data_path = ct.data_save_folder_path
        self.combined_file = self.data_path + '/CombinedData.json'

        self.get_data()

    
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

        # TODO: check if this works with different starting indicies

        error_mat = np.zeros((rows, cols))

        for ln in self.full_data:
            for sub_ln in ln["Runs"]:
                i = sub_ln["Number"]
                for j in sub_ln["Guesses"]:
                    if i != j:
                        error_mat[i-1, j-1] += 1

        return error_mat



if __name__ == "__main__":
    x = DataAnalysis()
    err_mat = x.make_error_mat()
    visualisation.matrix_heat_map(err_mat)