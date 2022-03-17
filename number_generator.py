import os
import time
import random
import numpy as np
from playsound import playsound

import control as ct

class Number_Gen:
    path = ct.folder_path
    max_wrong = 5

    def __init__(self, max_n) -> None:
        self.max_number = max_n

    def run_clip(self, number):
        #Run the clip
        file_path = self.path + '/' + str(number) + ct.file_ext
        playsound(file_path)

        # Start timer to see how long reply takes
        time_start = time.time()

        user_answer = -1
        user_attempts = 0
        
        # Await user responce
        while (user_answer - number != 0) and (user_attempts <= self.max_wrong):
            user_answer = int(input())
            user_attempts += 1
        
        if user_answer != number:
            print("Correct anwer was: " + str(number) + '\n')

        else:
            print("Correct: " + str(number) + '\n')

        time_end = time.time() - time_start

        return time_end, user_attempts - 1

    
    def generate_num(self):
        num = random.randint(0, self.max_number)
        num = 5
        return num

    def ask_user(self):
        times = list()
        attempts = list()

        try:
            while True:
                num = self.generate_num()
                time_taken, user_ans = self.run_clip(num)
            
                times.append(time_taken)
                attempts.append(user_ans)

        except KeyboardInterrupt:
            return times, attempts

    def export_data(self):
        times, attempts = self.ask_user()
        time_arr = np.array(times)
        attemps_arr = np.array(attempts)

        return time_arr, attemps_arr

if __name__ == "__main__":
    x = Number_Gen(10)
    print(x.export_data())

