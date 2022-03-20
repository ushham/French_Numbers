import os
import time
import random
from matplotlib.font_manager import json_dump
import numpy as np
import json
from playsound import playsound

import control as ct

class Number_Gen:
    path = ct.audio_folder_path
    max_wrong = 5

    def __init__(self, min_n, max_n) -> None:
        self.start_time = time.time()
        self.min_number = min_n
        self.max_number = max_n

    def run_clip(self, number):
        user_guesses = list()

        #Run the clip
        file_path = self.path + '/' + str(number) + ct.file_ext
        playsound(file_path)

        # Start timer to see how long reply takes
        time_start = time.time()

        user_answer = -1
        user_attempts = 0
        
        # Await user responce
        while (user_answer - number != 0) and (user_attempts <= self.max_wrong):
            user_answer = input()
            
            # User asks for a repeat play of audio
            if user_answer == "r":
                playsound(file_path)
                user_answer = -1

            else:
                user_answer = int(user_answer)
                user_guesses.append(user_answer)
                user_attempts += 1
        
        if user_answer != number:
            print("Correct anwer was: " + str(number) + '\n')

        else:
            print("Correct: " + str(number) + '\n')

        time_end = time.time() - time_start

        return user_guesses, time_end, user_attempts - 1


    def ask_user(self):
        nums_asked = list()
        nums_guessed = list()
        times = list()
        attempts = list()

        try:
            while True:
                num = random.randint(self.min_number, self.max_number)
                nums_asked.append(num)
                user_guesses, time_taken, user_ans = self.run_clip(num)
            
                nums_guessed.append(user_guesses)
                times.append(time_taken)
                attempts.append(user_ans)

        except KeyboardInterrupt:
            return nums_asked[:-1], nums_guessed, times, attempts

    def publish_data(self):
        file_name = ct.data_save_folder_path + '/' + str(round(self.start_time)) + ct.data_file_ext
        run_time = self.end_time - self.start_time

        # File is structured as:
        # Number to guess, list of guesses, time for coreect answer, number of wrong results
        
        data_line = {
            "Start_time": self.start_time,
            "Run_time": run_time,
            "Runs": []
        }
        
        # json.dump(data_line, f)

        for row in range(len(self.nums_arr)):
            row_data = {
                "Number": int(self.nums_arr[row]),
                "Guesses": list(self.guessed_arr[row]),
                "Time": float(self.time_arr[row]),
                "Attemps": int(self.attemps_arr[row]),
                "Result": str(self.nums_arr[row] == self.guessed_arr[row][-1])
            }
            data_line["Runs"].append(row_data)

        with open(file_name, 'w') as f:
            json.dump(data_line, f, indent=4)
        return 0

    def export_data(self):
        nums_asked, nums_guessed, times, attempts = self.ask_user()
        self.nums_arr = np.array(nums_asked)
        self.guessed_arr = np.array(nums_guessed, dtype=object)
        self.time_arr = np.array(times)
        self.attemps_arr = np.array(attempts)

        # Publish the data
        self.end_time = time.time()
        self.publish_data()
        return 0

if __name__ == "__main__":
    x = Number_Gen(1, 9)
    x.export_data()

