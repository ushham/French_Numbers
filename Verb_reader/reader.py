import os
import random

def read_line(text):
    voice_type = ['+m2', '+m3','+m7', '+f1', '+f2', '+f3']
    lang = 'fr'

    rand_voice = lang + random.choice(voice_type)

    string_parse = "espeak -v " + rand_voice + " " + "'" + text + "'"
    os.system(string_parse)
    return 0

def user_score(line):
    us = input()

    try:
        us = int(us)
    except:
        read_line(line)
        us = user_score(line)
    
    if us > 5:
        us = 5

    return us

def return_answer(line, answer):
    answer = input()

    if answer != ' ':
        read_line(line)
        return_answer(line, answer)
    else:
        print(str(answer))

    return 0



if __name__ == "__main__":
    print(return_answer("nous sommes"))
