from collect import *

while True:
    # give conditions for shot chart
    condition_names = "posID, gameID, screens, passes, type, result, contested, game_clock, quarter, shot_clock, distance"
    print("Possible options: " + condition_names)
    where = input("Enter where clause: ")
    coords = get_all_poss(where)

    # create and show shot chart
    create_court(coords)
