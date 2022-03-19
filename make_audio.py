import os
import csv
import control as ct

class Make_Audio:

    def __init__(self, path_to_csv) -> None:
        self.csv_file = path_to_csv
        self.data = self.csv_to_list()
        self.pass_all = False

    def csv_to_list(self):
        # Converts a csv to a list with the data for producing number files
        file = open(self.csv_file)
        csvreader = csv.reader(file)

        data = list()
        line_count = 0

        for row in csvreader:
            if line_count == 0:
                print("The header is: " + str(row) + ". We are expecting [File_name (int), Text of number (str)]")

            else:
                data.append(row)
            
            line_count += 1
        
        return data

    def run_command(self, file_name, text):
        string_command = "pico2wave -l " + ct.pico_lang + " -w" + ct.audio_folder_path + str(file_name) + ct.file_ext + " " + text

        #Checks if file already exists
        if os.path.exists(ct.folder_path + str(file_name) + ct.file_ext) and not(self.pass_all):
            print("A file already exists for " + str(file_name) + ct.file_ext + ". Do you want to overwrite this? (y/n), Over write all files (ya)")
            user_choose = input()
            
            if user_choose == "ya":
                self.pass_all = True
        
        else:
            user_choose = "y"

        if user_choose == "Y" or user_choose == "y" or self.pass_all:
            os.system(string_command)
            print("Exported file " + str(file_name) + ct.file_ext)
        
        return 0

    def list_to_audio(self):
        #Assuming list items are given in format: [number (file name), text to synthesis]

        for it in self.data:
            file_name, text = it
            self.run_command(file_name, text)
        self.pass_all = False
        return 0


if __name__ == "__main__":
    # Test for producing french numbers
    # ls = [[1, "un"], [2, "deux"], [3, "trois"]]
    # audio_maker = Make_Audio(ls)
    # audio_maker.list_to_audio()

    #Read given csv file
    csv_path = "/home/ohamilton/Documents/03_Programming/01_Python/French_Numbers/French_numbers.csv"
    audio_maker = Make_Audio(csv_path)
    print(audio_maker.list_to_audio())
    # audio_maker.list_to_audio()