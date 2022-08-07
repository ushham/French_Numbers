import data_management as dm
import ranking as rk
import reader as rd

def main():
    #Combine new files
    db = dm.read_new_data()

    try:
        while True:
            #Pick question to ask
            row = rk.return_index(db)
            #Ask question
            rd.read_line(row[0])
            # TODO: Why is answer not being printed?
            rd.return_answer(row[0], row[1])
            user_score = rd.user_score(row[0])

            # Generate new score
            row = rk.update_score(user_score, row)
            # TODO: Update database
            print(row)
 
    except KeyboardInterrupt:
        return 0
        # dm.save_database(db)
        # dm.backup_database(db)

if __name__ == "__main__":

    main()
    # db = dm.read_new_data()
    # # row = rk.return_index(db)
    # # print(row)
    # print(db)