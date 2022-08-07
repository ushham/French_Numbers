# French (Belgian) listening testing

This is a program to test your listening of numbers on a foreign language. It is currently set up to test you on Belgian numbers (the same as French, but there are different words for 70 and 90).

There are two different tests you can use. Either test yourself for **Number Comprehension**, or **Verb Comprehension**.

## How to Run

The script `run_script.py`, the user has the following input choices:

| Name        | Optional Arguments | Default Value | Description                                                           |
| ----------- | ------------------ | ------------- | --------------------------------------------------------------------- |
| Help        | --h                | -             | Help message                                                          |
| Min Number  | --mn               | 0             | Minimum number you will be asked                                      |
| Max Number  | --mx               | 100           | Maximum number you will be asked                                      |
| Read files  | --r                | False         | The program will play files instead of generating number using espeak |
| Export Data | --e                | True          | Exports the data to a json file                                       |

## User Control

| Variable                | Description                                                                                               |
| ----------------------- | --------------------------------------------------------------------------------------------------------- |
| `audio_folder_path`     | Path to the folder containing the audio files (only required if `--r` is set to True).                    |
| `csv_path`              | Path to the csv file containing words for text-to-speech (only required for using script `make_audio.py`) |
| `file_ext`              | Audio file extension type.                                                                                |
| `pico_lang`             | If the user is using the `make_audio.py` script, this controls the voice used when producing audio clips. |
| `espeak_lang`           | The language used for speak synthesis when `--r` is set to False.                                         |
| `data_save_folder_path` | Folder the json files are saved to when `--e` is set to True.                                             |
| `data_file_ext`         | Data type the database is saved as.                                                                       |

## Text-to-Speech

The script `make_audio.py` produces audio clips, based on user inputs from a csv file. This allows for custom pronunciation/names for numbers.

If the user wants to use these produced audio files, they can set `--r` to True.

The text-to-speech synthesiser used in this script is [pico](https://github.com/naggety/picotts).



Otherwise, the program creates the voice on the fly, using [espeak](http://espeak.sourceforge.net).



## Data Export

The following data is exported to a json file when the export data value is set to true:

- Start time `Start_time` (unix time stamp in seconds, float), time the program started running.

- Lesson time `Run_time` (seconds, float), the time the user ran the program for.

- Maximum number `Max_num` (int), maximum number that could be asked by the program.

- Minimum number `Min_num` (int), minimum number that could be asked by the program.

- Individual test information `Runs` (list):
  
  - Number asked `Number` (int), number asked user by program.
  
  - User guess `Guesses` (list, int), list of inputs the user gave.
  
  - Response time `Time` (seconds, float), Time for the user to respond correctly.
  
  - Number of incorrect attempts `Attempts` (int).



## Visualisation

Currently the visualisations are triggered by running the `data_extract.py` script.

The only visualisation that is currently produced is the error matrix, where the y axis presents the number to guess, and the x axis presents the incorrect answers given by the user.

**Visualisations TODO:**

- Distribution of questions asked user.
- Print out interesting stats