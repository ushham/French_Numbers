# Script Outline
This section (Verb comprehension) aims to help you improve listening comprehension for french verbs, and help with conjugating from english.

## Code outline
There is a csv that holds:
| From | To | Recall (eng-frn) | Last Recall |
|---|---|---|---|
| I am | Je suis | 1 | Datetime(2022. 08, 07)|
| Je suis | I am | 2 | Datetime(2022. 08, 07)|

The recall column holds the score (1-5), of how confident the user is at the question.
The numbers represent the following:
| Number | Meaning | Responce | 
| --- | --- | ---|
| 1 | New / Dont know | Ask again today |
| 2 | Not good | Ask again within a day |
| 3 | Know, but not comfortable | Ask again within a week |
| 4 | Good, could be better | Ask again within a month |
| 5 | Easy | Ask again within a year |

The numbers will alter how we rank the verbs to ask the user. For example, if there are two question with the same score, the one that was asked longer ago will take precidence.