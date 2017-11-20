from coordinates import *
import csv
import mysql.connector


def save_excel_data():
    cnx = mysql.connector.connect(host='localhost', user='root', database="UWO_tracking")
    cursor = cnx.cursor()

    gameID = input("Enter the game ID on the .csv file:\n")

    with open("games/"+ gameID +".csv", 'r') as csv_file:
        game_data = csv.reader(csv_file, delimiter=',')
        next(game_data, None)
        for row in game_data:

            pos_ID = row[0]
            game_ID = gameID
            screens = row[1]
            passes = row[2]
            type = row[3]
            result = row[4]
            contested = row[5]
            if contested == '':
                contested = "NULL"
            shot_clock = row[6]
            if shot_clock == '':
                shot_clock = None
            shooter = row[7]
            if shooter == '':
                shooter = "NULL"

            get_pos = (
                "SELECT * FROM data WHERE posID = %s AND gameID = %s"
            )
            cursor.execute(get_pos, (pos_ID, gameID))
            results = cursor.fetchone()

            if results is None:

                insert_pos = (
                    "INSERT INTO data (posID, gameID, screens, passes, type, result, contested, shot_clock, shooter)"
                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                )

                cursor.execute(insert_pos, (pos_ID, game_ID, screens, passes, str(type), str(result), str(contested), shot_clock, str(shooter)))
                cnx.commit()

                if result != "to":

                    print("Enter shot location for shot with posID=" + str(pos_ID))
                    get_coordinates(pos_ID, gameID, "shooter")

                    # print("Enter defender location")
                    # get_coordinates(pos_ID, gameID, "defender")
                    #
                    # calculate_squared_distance(pos_ID, gameID)

    cnx.close()

def input_data():
    cnx = mysql.connector.connect(host='localhost', user='root', database="UWO_tracking")
    cursor = cnx.cursor()

    gameID = input("Enter the game ID: ")
    num_pos = input("Number of total possessions? ")
    i = 1

    while i <= int(num_pos):

        print("Possession " + str(i))
        pos_ID = i
        screens = input("Number of screens? ")
        passes = input("Number of passes? ")
        p_type = input("Possession type? (hq/oreb/fb) ")
        result = input("Possession result? (make/miss/foul/oreb) ")
        contested = input("Contest level? (low/medium/high) ")
        game_clock = input("Game clock: ")
        q = input("Quarter? ")
        shot_clock = input("Shot clock: ")

        confirm = input("Enter to confirm, any key to retry: ")
        if confirm == "":

            insert_pos = (
                "INSERT INTO data (posID, gameID, screens, passes, type, result, contested, game_clock, quarter, shot_clock)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )

            cursor.execute(insert_pos, (pos_ID, int(gameID), int(screens), int(passes), str(p_type), str(result), str(contested),
                                        str(game_clock), int(q), int(shot_clock)))
            cnx.commit()
            get_coordinates(pos_ID, gameID, "shooter")
            print("Enter defender location")
            get_coordinates(pos_ID, gameID, "defender")

            calculate_squared_distance(pos_ID, gameID)
            i += 1

        else:
            print("re-enter data")
