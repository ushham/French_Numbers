import pandas as pd
import detectlanguage

def remove_phonetics(word):
    # Removes words within ()
    if " (" in word:
        strip_word = word.split(" (")[0]
    else:
        strip_word = word
    return strip_word

def remove_quotes(word):
    # Removes quote marks in the word
    return word.replace('"', "")

def split_slash(word):
    # If a backslash is in the word, then split in two
    new_word = word.split("/")
    output = [w.strip() for w in new_word]
    return output

def clean_input(word):
    cleaned = remove_quotes(remove_phonetics(word))
    return split_slash(cleaned)

def split_line(line):
    return line.split("	")

def check_lang(lst):
    langs = list()

    for w in lst:
        # Problem happening here!!!!
        lang_dic = detectlanguage.detect(w)
        
        langs.append(lang_dic)
        print(w, lang_dic)

    results = list()
    
    for word_dics in langs:
        for d in word_dics:
            if d["isReliable"]:
                results.append(d['language'])
    
    if len(set(results)) == 1:
        output = results[0]
    else:
        output = input("What language is (en/fr): " + str(lst))
    
    return output

def make_json(line):
    question, answer = line

    question, answer = clean_input(question), clean_input(answer)
    item = {
        "question": question,
        "answer": answer,
        "answer_lang": check_lang(answer)
    }
    return item

def read_txt(file_name):
    with open(file_name) as f:
        lines = f.readlines()

    cols = list()
    for l in lines:
        cols.append(l.replace('\n', "").split('\t'))

    return cols



if __name__ == "__main__":
    # input = clean_input(split_line("you have	tu as / vous aves")[1])
    
    # detectlanguage.configuration.api_key = "064c904a2b634949f95deab6b242c881"
    # print(make_json("twenty to two	deux heure moins vingt (mwa)"))
    # text = read_txt("anki_cards/_French.txt")
    # for i in text[:5]:
    #     print(make_json(i))
    check_lang(["J ai"])
    #TODO: print out database
    # TODO: make text-speech module 