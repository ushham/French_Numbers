from asyncore import read
import os
import random


def read_line(text):
    voice_type = ['+m2', '+m3','+m7', '+f1', '+f2', '+f3']
    lang = 'fr'

    rand_voice = lang + random.choice(voice_type)

    string_parse = "espeak -v " + rand_voice + " " + "'" + text + "'"
    os.system(string_parse)
    return 0

def user_responce(line):
    us = input()

    try:
        us = int(us)
    except:
        read_line(line)
        us = user_responce(line)
    
    if us > 5:
        us = 5

    return us



if __name__ == "__main__":
    print(user_responce("nous sommes"))