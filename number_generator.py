import os
import time
import random
import numpy as np
import json
from playsound import playsound
import argparse

import control as ct

class Number_Gen:
    path = ct.audio_folder_path
    max_wrong = 5

    def __init__(self, min_n, max_n, read_files=True, export_data=True) -> None:
        self.start_time = time.time()
        self.min_number = min_n
        self.max_number = max_n
        self.play_file = read_files
        self.export_d = export_data

        if read_files:
            self.num_arr = self.num_range_from_files()
            self.max_number = max(self.num_arr)
            self.min_number = min(self.num_arr)

    def num_range_from_files(self):
        num_files = os.listdir(self.path)
        num_files = [x.split('.')[0] for x in num_files if x[-len(ct.file_ext):] == ct.file_ext]
        return num_files

    @staticmethod
    def speak_text(number):
        # espeak string
        voice_type = ['+m2', '+m3','+m7', '+f1', '+f2', '+f3']
        lang = 'fr-be'

        rand_voice = lang + random.choice(voice_type)

        string_parse = "espeak -v " + rand_voice + " " + str(number)
        os.system(string_parse)

    def run_clip(self, number):
        user_guesses = list()

        #Run the clip
        file_path = self.path + '/' + str(number) + ct.file_ext

        if self.play_file:
            playsound(file_path)
        else:
            self.speak_text(number)

        # Start timer to see how long reply takes
        time_start = time.time()

        user_answer = -1
        user_attempts = 0
        
        # Await user responce
        while (user_answer - number != 0) and (user_attempts <= self.max_wrong):
            user_answer = input()
            
            # User asks for a repeat play of audio
            if user_answer == "r":
                if self.play_file:
                    playsound(file_path)
                else:
                    self.speak_text(number)

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
                if self.play_file:
                    num = int(random.choice(self.num_arr))
                else:
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
            "Max_num": self.min_number, 
            "Min_num": self.max_number,
            "Speaker": "pico" if self.play_file else "espeak",
            "Runs": []
        }

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
        if self.export_d:
            self.end_time = time.time()
            self.publish_data()
        return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run french numbers code.')
    parser.add_argument('min_number', metavar='min_N', type=int, default=0, help='The min number that you will be asked')
    parser.add_argument('max_number', metavar='max_N', type=int, default=100, help='The max number that you will be asked')
    parser.add_argument('--r', metavar='--read_files', default=False, action='store', help='Allows you to choose if files are read, or generated (default)')
    parser.add_argument('--e', metavar='--export_data', default=True, action='store', help='Choose whether data is exported (export is default)')


    args = parser.parse_args()

    x = Number_Gen(args.min_number, args.max_number, read_files=args.r, export_data=args.e)
    x.export_data()

