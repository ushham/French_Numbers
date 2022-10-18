import pandas as pd
import numpy as np
import random
import os

pico_lang = "fr-FR"
espeak_lang = 'fr-be'

def speak_text(word):
    # espeak string
    voice_type = ['+m2', '+m3','+m7', '+f1', '+f2', '+f3']
    lang = espeak_lang

    rand_voice = lang + random.choice(voice_type)

    string_parse = "espeak -v " + rand_voice + " " + word
    os.system(string_parse)

def filter_db(db):
    filter_col = 'Rating'
    db['prob'] = 1 / (db[filter_col] + 1)
    return db.sample(n=1, weights=db['prob'])


if __name__ == "__main__":
    file = "wordlist.csv"
    database = pd.read_csv(file)
    filter_db(database)

    try:
        while True:
            row = filter_db(database)
            speak_text(row["French"].iloc[0])
            user_score = input()

            print(row['English'].iloc[0])

            database.at[row.index[0], 'Rating'] = user_score
            print("here: " + database.at[row.index[0], 'Rating'])
    except KeyboardInterrupt:
        database.to_csv("wordlist2.csv", index=False)
