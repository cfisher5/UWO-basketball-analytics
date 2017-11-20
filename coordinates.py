from tkinter import *
import mysql.connector
import math


def get_coordinates(posID, gameID, type):

    cnx = mysql.connector.connect(host='localhost', user='root', database="UWO_tracking")
    cursor = cnx.cursor()

    root = Tk()

    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    canvas = Canvas(frame, bd=0, width=500, height=472)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    frame.pack(fill=BOTH, expand=1)

    img = PhotoImage(file="basketball-court.gif")
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    if type == "defender":
        get_coords = (
            "SELECT xcoord, ycoord FROM data WHERE posID = %s AND gameID = %s"
        )
        cursor.execute(get_coords, (posID, gameID))
        results = cursor.fetchall()
        x, y = 0, 0
        for pos in results:
            x = pos[0]
            y = pos[1]

        canvas.create_oval(x - 3, y - 3, x + 3, y + 3)

    def press_button(event):
        circ = canvas.create_oval(event.x-3, event.y-3, event.x+3, event.y+3)
        accept = input("Confirm Location? y/n ")
        if accept == "y":
            print("SAVING " + str(event.x))
            print("SAVING " + str(event.y))

            if type == 'shooter':
                insert_coords = (
                    "UPDATE data SET xcoord = %s, ycoord = %s "
                    "WHERE posID = %s AND gameID = %s")
            else:
                insert_coords = (
                    "UPDATE data SET def_xcoord = %s, def_ycoord = %s "
                    "WHERE posID = %s AND gameID = %s")

            cursor.execute(insert_coords, (str(event.x), str(event.y), posID, gameID))
            cnx.commit()
            cnx.close()

            canvas.quit()
            root.destroy()
        else:
            canvas.delete(circ)

    canvas.bind("<ButtonPress-1>", press_button)
    root.mainloop()


def get_all_poss(where_clause):
    cnx = mysql.connector.connect(host='localhost', user='root', database="UWO_tracking")
    cursor = cnx.cursor()

    get_coords = (
        "SELECT xcoord, ycoord, result FROM data " + where_clause
    )
    cursor.execute(get_coords)
    results = cursor.fetchall()
    arr = []
    for i in results:
        if i[0] is not None:
            arr.append(i)
    cnx.close()
    return arr


def create_court(coord_array):

    root = Tk()
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    canvas = Canvas(frame, bd=0, width=500, height=472)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    frame.pack(fill=BOTH, expand=1)
    img = PhotoImage(file="basketball-court.gif")
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))


    plot_coordinates(canvas, coord_array)
    root.mainloop()


def plot_coordinates(canvas, coord_array):

    for point in coord_array:

        x = point[0]
        y = point[1]
        make_miss = point[2]

        if make_miss == "make":
            canvas.create_oval(x-5, y - 5, x + 5, y + 5, fill="green")
        elif make_miss == "miss":
            # circ = canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
            canvas.create_line(x-4,y+4,x+4,y-4, fill="red", width=2)
            canvas.create_line(x-4,y-4,x+4,y+4, fill="red", width=2)
        elif make_miss == "foul":
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")
        else:
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="orange")


def calculate_squared_distance(posID, gameID):

    cnx = mysql.connector.connect(host='localhost', user='root', database="UWO_tracking")
    cursor = cnx.cursor()
    get_coords = (
        "SELECT xcoord, ycoord, def_xcoord, def_ycoord FROM data WHERE posID = %s AND gameID = %s"
    )
    cursor.execute(get_coords, (posID, gameID))
    results = cursor.fetchone()

    shooter_x = results[0]
    shooter_y = results[1]
    def_x = results[2]
    def_y = results[3]

    x_distance = float(def_x) - float(shooter_x)
    x_distance = x_distance * x_distance

    y_distance = float(def_y) - float(shooter_y)
    y_distance = y_distance * y_distance

    distance = x_distance + y_distance

    distance = math.sqrt(distance)
    print(distance)

    set_distance = (
        "UPDATE data SET distance = %s WHERE posID = %s AND gameID = %s"
    )

    cursor.execute(set_distance, (distance, posID, gameID))
    cnx.commit()
    cnx.close()




