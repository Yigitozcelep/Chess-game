from tkinter import *

root = Tk()
root.geometry("1005x944+500+20")
root.configure(bg="orange")
chess_frame = Frame(root)
chess_frame.grid(row=0, column=1)

info_frame = Frame(root)
info_frame.grid(row=0, column=0)

statu_label = Label(info_frame, text="State:", bg="orange", width=10)
statu_label.grid(row=0, column=0)

statu_label_result = Label(info_frame, text="0", width=10, bg="orange")
statu_label_result.grid(row=1, column=0, columnspan=2)

tahta = [[], [], [], [], [], [], [], []]

all_moves = []

map = [["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]
       ,["","","","","","","",""],["","","","","","","",""],["","","","","","","",""],["","","","","","","",""]]


green_elements = []
green_threats = set()

purple_elements = []
purple_threats = set()

green_and_purple_elements = []
green_and_purple_elements.append(green_elements)
green_and_purple_elements.append(purple_elements)

purple_sah_coor = (0,4)
green_sah_coor = (7,4)

def mapi_izle():
    if True:return
    data = []
    for x in map:
        data.append(["    " if a == "" else f"{a.team[0]}{a.button.cget('text')}" for a in x])
    for x in data:
        print(x)
    print("-------------------\n")

current_element = object
current_player = "green"



class Background:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        colors = ["black", "white"] if column % 2 == 0 else ["white", "black"]
        self.color = colors[0] if row % 2 == 0 else colors[1]
        self.button = Button(chess_frame, highlightbackground=self.color, width=12, heigh=7, command=self.do_something)
        self.button.grid(row=self.x, column=self.y)
        tahta[row].append(self.button)


    def do_something(self):
        if self.button.cget("highlightbackground") == "red":
            current_element.change_place(self.x, self.y)




for row in range(8):
    for column in range(8):
       Background(row, column)


class Common:
    def change_place(self, x, y):
        if 0 <= x <= 7 and 0 <= y <= 7:
            global current_player
            if map[x][y] != "":map[x][y].button.grid_forget()
            enemey_sah = green_sah_coor if self.team == "purple" else purple_sah_coor
            self.delete_element_in_list(map[x][y])
            map[x][y] = self
            map[self.x][self.y] = ""
            self.x = x
            self.y = y
            self.button.grid(row=x, column=y)
            all_moves.append([[i for i in row] for row in map])
            current_player = "green" if current_player == "purple" else "purple"
            elements = green_elements if current_player == "green" else purple_elements
            for x in elements:
                if x.check_illegal_move():break
            else:
                a = Label(chess_frame, text="Oyun bitti", font=("helvetica", 30, "bold"))
                a.grid(row=2, column=2, columnspan=3)


            self.all_white()
            self.collect_all_threads()

            if enemey_sah in self.all_threads:
                tahta[enemey_sah[0]][enemey_sah[1]].config(highlightbackground="blue")
            mapi_izle()

    def white_move(self):
        for column in range(8):
            for row in range(8):
                if tahta[row][column].cget("highlightbackground") == "blue":continue
                colors = ["black", "white"] if column % 2 == 0 else ["white", "black"]
                color = colors[0] if row % 2 == 0 else colors[1]
                tahta[row][column].config(highlightbackground=color)

    def all_white(self):
        for column in range(8):
            for row in range(8):
                colors = ["black", "white"] if column % 2 == 0 else ["white", "black"]
                color = colors[0] if row % 2 == 0 else colors[1]
                tahta[row][column].config(highlightbackground=color)



    def red_light(self):
        global current_element, current_player
        if not current_player == self.team:return
        current_element = self
        data = self.check_illegal_move()
        self.white_move()
        if not data:return
        for x,y in data:
            tahta[x][y].config(highlightbackground="red")



    def threads(self):
        for x in self.moves():
            self.all_threads.add(x)

    def collect_all_threads(self):
        self.all_threads.clear()
        for x in self.all_elements:
            x.threads()


    def delete_element_in_list(self, item):
        for elements in green_and_purple_elements:
            for index,value in enumerate(elements):
                if value == item:
                    del elements[index]

    def check_illegal_move(self):
        enemy_object = green_elements[0] if self.team == "purple" else purple_elements[0]
        our_sah_coor = green_sah_coor if self.team == "green" else purple_sah_coor
        data = []
        for x,y in self.moves():
            enemy_tas = map[x][y]
            savex, savey = self.x, self.y
            map[x][y] = self
            map[self.x][self.y] = ""
            if enemy_tas != "":self.delete_element_in_list(enemy_tas)
            self.x, self.y = x,y
            enemy_object.collect_all_threads()
            info = not our_sah_coor in enemy_object.all_threads
            mapi_izle()
            self.x, self.y = savex, savey
            map[x][y] = enemy_tas
            map[self.x][self.y] = self
            if enemy_tas != "":enemy_object.all_elements.append(enemy_tas)
            if info:data.append((x,y))
        return data



class Piyon(Common):
    def __init__(self, x, y, team):
        super().__init__()
        self.team = team
        self.all_elements = purple_elements if self.team == "purple" else green_elements
        self.all_threads = purple_threats if self.team == "purple" else green_threats

        self.enemy_all_elements = green_elements if self.team == "purple" else purple_elements
        self.enemy_all_threads =  green_threats if self.team == "purple" else purple_threats

        self.x = x
        self.y = y
        self.point = 100
        self.button = Button(chess_frame, text="Piyon", font=("helvetica", 30, "bold"), fg= self.team, command=self.red_light)
        self.button.grid(row=self.x, column=self.y)

    def moves(self):
        data = []

        if self.team == "purple" and self.x == 1:
                if map[self.x + 1][self.y] == "" and map[self.x + 2][self.y] == "":
                    data.append((self.x + 2, self.y))

        elif self.team == "green" and self.x == 6:
                if map[self.x - 1][self.y] == "" and map[self.x - 2][self.y] == "":
                    data.append((self.x - 2, self.y))

        if 0 <= self.x - 1 <= 7 and 0 <= self.y - 1 <= 7 and self.team == "green":
            x = map[self.x - 1][self.y - 1]
            if x != "" and x.team == "purple":
                data.append((self.x -1 , self.y -1))

        if 0 <= self.x - 1 <= 7 and 0 <= self.y + 1 <= 7 and self.team == "green":
            x = map[self.x - 1][self.y + 1]
            if x != "" and x.team == "purple":
                data.append((self.x -1 , self.y + 1))

        if 0 <= self.x - 1 <= 7 and map[self.x - 1][self.y] == "" and self.team == "green":
            data.append((self.x - 1, self.y))

        #Purple team
        if 0 <= self.x + 1 <= 7 and 0 <= self.y + 1 <= 7 and self.team == "purple":
            x = map[self.x + 1][self.y + 1]
            if x != "" and x.team == "green":
                data.append((self.x + 1, self.y + 1))

        if 0 <= self.x + 1 <= 7 and 0 <= self.y - 1 <= 7 and self.team == "purple":
            x = map[self.x + 1][self.y - 1]
            if x != "" and x.team == "green":
                data.append((self.x + 1, self.y - 1))

        if 0 <= self.x + 1 <= 7 and map[self.x + 1][self.y] == "" and self.team == "purple":
            data.append((self.x + 1, self.y))

        # Geçerken alma

        if self.team == "green" and 0 <= self.y -1 <= 7 and self.x == 3 and map[self.x][self.y -1] != "" and \
                map[self.x][self.y -1].button.cget("text") == "Piyon" and map[self.x][self.y -1].team != self.team:

            if all_moves[-2][1][self.y-1] == map[self.x][self.y-1]:
                data.append((self.x -1, self.y -1))

        if self.team == "green" and 0 <= self.y + 1 <= 7 and self.x == 3 and map[self.x][self.y + 1] != "" and \
                map[self.x][self.y + 1].button.cget("text") == "Piyon" and map[self.x][self.y + 1].team != self.team:

            if all_moves[-2][1][self.y + 1] == map[self.x][self.y + 1]:
                data.append((self.x - 1, self.y + 1))

        if self.team == "purple" and 0 <= self.y -1 <= 7 and map[self.x][self.y -1] != "" and self.x == 4 and \
                map[self.x][self.y -1].button.cget("text") == "Piyon" and map[self.x][self.y -1].team != self.team:

            if all_moves[-2][6][self.y-1] == map[self.x][self.y-1]:
                data.append((self.x + 1, self.y -1))

        if self.team == "purple" and 0 <= self.y + 1 <= 7 and map[self.x][self.y + 1] != "" and self.x == 4 and\
                map[self.x][self.y + 1].button.cget("text") == "Piyon" and map[self.x][self.y + 1].team != self.team:

            if all_moves[-2][6][self.y + 1] == map[self.x][self.y + 1]:
                data.append((self.x + 1, self.y + 1))

        return data


    def change_place(self, x, y):
        global current_player
        if self.x != x and self.y != y and map[x][y] == "":
            map[self.x][y].button.grid_forget()
            self.delete_element_in_list(map[self.x][y])
        if map[x][y] != "": map[x][y].button.grid_forget()
        self.delete_element_in_list(map[x][y])
        map[x][y] = self
        map[self.x][self.y] = ""
        self.x = x
        self.y = y
        self.button.grid(row=x, column=y)
        self.white_move()
        all_moves.append([[i for i in row] for row in map])
        current_player = "green" if current_player == "purple" else "purple"
        if self.team == "green" and x == 0:
            self.do_vezir()
        if self.team == "purple" and x == 7:
            self.do_vezir()
        self.all_white()
        enemey_sah = green_sah_coor if self.team == "purple" else purple_sah_coor
        self.collect_all_threads()
        if enemey_sah in self.all_threads:
            tahta[enemey_sah[0]][enemey_sah[1]].config(highlightbackground="blue")
        elements = green_elements if current_player == "green" else purple_elements
        for x in elements:
            if x.check_illegal_move(): break
        else:
            a = Label(chess_frame, text="Oyun bitti", font=("helvetica", 30, "bold"))
            a.grid(row=2, column=2, columnspan=3)
        mapi_izle()

    def do_vezir(self):
        self.button.grid_forget()
        self.delete_element_in_list(self)
        v = Vezir(self.x, self.y, self.team)
        map[self.x][self.y] = v
        self.all_elements.append(v)


    def threads(self):
        if self.team == "green":
            if 0 <= self.x - 1 <= 7 and 0 <= self.y -1 <= 7:
                self.all_threads.add((self.x -1, self.y -1))
            if 0 <= self.x - 1 <= 7 and 0 <= self.y + 1 <= 7:
                self.all_threads.add((self.x -1, self.y + 1))

        if self.team == "purple":
            if 0 <= self.x + 1 <= 7 and 0 <= self.y -1 <= 7:
                self.all_threads.add((self.x + 1, self.y -1))
            if 0 <= self.x + 1 <= 7 and 0 <= self.y + 1 <= 7:
                self.all_threads.add((self.x + 1, self.y + 1))


class At(Common):
    def __init__(self, x, y, team):
        super().__init__()
        self.team = team
        self.x = x
        self.y = y
        self.point = 300
        self.all_elements = purple_elements if self.team == "purple" else green_elements
        self.all_threads = purple_threats if self.team == "purple" else green_threats
        self.enemy_all_elements = green_elements if self.team == "purple" else purple_elements
        self.enemy_all_threads = green_threats if self.team == "purple" else purple_threats
        self.button = Button(chess_frame, text="At", font=("helvetica", 30, "bold"), fg= self.team, command=self.red_light)
        self.button.grid(row=self.x, column=self.y)


    def moves(self):
        moves = [(self.x + 2, self.y + 1), (self.x + 2, self.y - 1), (self.x + 1, self.y + 2), (self.x + 1, self.y -2),
                (self.x-1 , self.y +2), (self.x -1, self.y -2), (self.x - 2, self.y + 1), (self.x -2, self.y -1)]
        possible_moves = []
        for x,y in moves:
            if x >= 0 and y >= 0 and x <= 7 and y <= 7:
                    if map[x][y] == "" or map[x][y].team != self.team:
                        possible_moves.append((x,y))
        return possible_moves



class Fil(Common):
    def __init__(self, x, y, team):
        super().__init__()
        self.team = team
        self.x = x
        self.y = y
        self.point = 310
        self.all_elements = purple_elements if self.team == "purple" else green_elements
        self.all_threads = purple_threats if self.team == "purple" else green_threats
        self.enemy_all_elements = green_elements if self.team == "purple" else purple_elements
        self.enemy_all_threads = green_threats if self.team == "purple" else purple_threats
        self.button = Button(chess_frame, text="Fil", font=("helvetica", 30, "bold"), fg= self.team, command=self.red_light)
        self.button.grid(row=self.x, column=self.y)


    def moves(self):
        data = []
        for num in range(1,8):
            if 0 <= self.x + num <= 7 and 0 <= self.y + num <= 7:
                if map[self.x + num][self.y + num] == "" or map[self.x + num][self.y + num].team != self.team:
                    data.append((self.x + num, self.y + num))
                    if not map[self.x + num][self.y + num] == "":break

                else:break

        for num in range(1, 8):
            if 0 <= self.x - num <= 7 and 0 <= self.y + num <= 7:
                if map[self.x - num][self.y + num] == "" or map[self.x - num][self.y + num].team != self.team:
                    data.append((self.x - num, self.y + num))
                    if not map[self.x - num][self.y + num] == "":break

                else:break

        for num in range(1, 8):
            if 0 <= self.x - num <= 7 and 0 <= self.y - num <= 7:
                if map[self.x - num][self.y - num] == "" or map[self.x - num][self.y - num].team != self.team:
                    data.append((self.x - num, self.y - num))
                    if not  map[self.x - num][self.y - num] == "":break
                else:break

        for num in range(1, 8):
            if 0 <= self.x + num <= 7 and 0 <= self.y - num <= 7:
                if map[self.x + num][self.y - num] == "" or map[self.x + num][self.y - num].team != self.team:
                    data.append((self.x + num, self.y - num))
                    if not map[self.x + num][self.y - num] == "":break
                else:break

        return data



class Kale(Common):
    def __init__(self, x, y, team):
        super().__init__()
        self.team = team
        self.x = x
        self.y = y
        self.point = 500
        self.before_move = False
        self.all_elements = purple_elements if self.team == "purple" else green_elements
        self.all_threads = purple_threats if self.team == "purple" else green_threats
        self.enemy_all_elements = green_elements if self.team == "purple" else purple_elements
        self.enemy_all_threads = green_threats if self.team == "purple" else purple_threats
        self.button = Button(chess_frame, text="Kale", font=("helvetica", 30, "bold"), fg= self.team, command=self.red_light)
        self.button.grid(row=self.x, column=self.y)

    def moves(self):
        data = []
        for num in range(1,8):
            if 0 <= self.y + num <= 7:
                if map[self.x][self.y + num] == "" or map[self.x][self.y + num].team != self.team:
                    data.append((self.x, self.y + num))
                    if map[self.x][self.y + num] != "":break
                else:break

        for num in range(1, 8):
            if 0 <= self.y - num <= 7:
                if map[self.x][self.y - num] == "" or map[self.x][self.y - num].team != self.team:
                    data.append((self.x, self.y - num))
                    if map[self.x][self.y - num] != "":break
                else:break


        for num in range(1, 8):
            if 0 <= self.x + num <= 7:
                if map[self.x + num][self.y] == "" or map[self.x + num][self.y].team != self.team:
                    data.append((self.x + num, self.y))
                    if map[self.x + num][self.y] != "":break
                else:break

        for num in range(1, 8):
            if 0 <= self.x - num <= 7:
                if map[self.x - num][self.y] == "" or map[self.x - num][self.y].team != self.team:
                    data.append((self.x - num, self.y))
                    if map[self.x - num][self.y] != "":break
                else:break
        return data



    def change_place(self, x, y):
        if 0 <= x <= 7 and 0 <= y <= 7:
            global current_player
            if map[x][y] != "":map[x][y].button.grid_forget()
            self.delete_element_in_list(map[x][y])
            map[x][y] = self
            map[self.x][self.y] = ""
            self.x = x
            self.y = y
            self.button.grid(row=x, column=y)
            self.all_white()
            all_moves.append([[i for i in row] for row in map])
            current_player = "green" if current_player == "purple" else "purple"
            self.before_move = True
            enemey_sah = green_sah_coor if self.team == "purple" else purple_sah_coor
            self.collect_all_threads()
            if enemey_sah in self.all_threads:
                tahta[enemey_sah[0]][enemey_sah[1]].config(highlightbackground="blue")
            elements = green_elements if current_player == "green" else purple_elements
            for x in elements:
                if x.check_illegal_move(): break
            else:
                a = Label(chess_frame, text="Oyun bitti", font=("helvetica", 30, "bold"))
                a.grid(row=2, column=2, columnspan=3)

            mapi_izle()


class Sah(Common):
    def __init__(self, x, y, team):
        super().__init__()
        self.team = team
        self.x = x
        self.y = y
        self.all_elements = purple_elements if self.team == "purple" else green_elements
        self.all_threads = purple_threats if self.team == "purple" else green_threats
        self.enemy_all_elements = green_elements if self.team == "purple" else purple_elements
        self.enemy_all_threads = green_threats if self.team == "purple" else purple_threats
        self.before_move = False
        self.point = 0
        self.button = Button(chess_frame, text="Şah", font=("helvetica", 30, "bold"), fg= self.team, command=self.red_light)
        self.button.grid(row=self.x, column=self.y)

    def moves(self):
        data = [(self.x + 1, self.y),(self.x + 1, self.y + 1), (self.x + 1, self.y -1),(self.x, self.y + 1),
                (self.x, self.y -1), (self.x - 1, self.y),(self.x -1, self.y +1), (self.x -1, self.y-1)]

        result = []
        for x,y in data:
            if 0 <= x <= 7 and 0 <= y <= 7:
                if map[x][y] == "" or map[x][y].team != self.team:
                    result.append((x,y))

        #Rok Yeşil Sağ taraf
        if self.team == "green" and self.before_move == False:
            x = map[7][7]
            if x != "" and x.button.cget("text") == "Kale" and x.before_move == False:
                self.collect_all_threads()

                if map[7][6] == "" and map[7][5] == "" and not (7,4) in self.enemy_all_threads and \
                        not (7,5) in self.enemy_all_threads and not (7,6) in self.enemy_all_threads:
                    result.append((7,6))
        #Rok Yeşil sol taraf
        if self.team == "green" and self.before_move == False:
            x = map[7][0]
            if x != "" and x.button.cget("text") == "Kale" and x.before_move == False:
                self.collect_all_threads()

                if map[7][1] == "" and map[7][2] == "" and map[7][3] == "" and not (7,2) in self.enemy_all_threads and \
                        not (7,3) in self.enemy_all_threads and not (7,4) in self.enemy_all_threads:
                    result.append((7,2))

        #Rok pempe sağ taraf
        if self.team == "purple" and self.before_move == False:
            x = map[0][7]
            if x != "" and x.button.cget("text") == "Kale" and x.before_move == False:
                self.collect_all_threads()

                if map[0][6] == "" and map[0][5] == "" and not (0,4) in self.enemy_all_threads and \
                        not (0,5) in self.enemy_all_threads and not (0,6) in self.enemy_all_threads:
                    result.append((0,6))

        #Rok pempe sol taraf
        if self.team == "purple" and self.before_move == False:
            x = map[0][0]
            if x != "" and x.button.cget("text") == "Kale" and x.before_move == False:
                self.collect_all_threads()

                if map[0][1] == "" and map[0][2] == "" and map[0][3] == "" and not (0,2) in self.enemy_all_threads and \
                        not (0,3) in self.enemy_all_threads and not (0,4) in self.enemy_all_threads:
                    result.append((0,2))

        return result

    def threads(self):
        data = [(self.x + 1, self.y),(self.x + 1, self.y + 1), (self.x + 1, self.y -1),(self.x, self.y + 1),
                (self.x, self.y -1), (self.x - 1, self.y),(self.x -1, self.y +1), (self.x -1, self.y-1)]

        for x,y in data:
            if 0 <= x <= 7 and 0 <= y <= 7:
                if map[x][y] == "" or map[x][y].team != self.team:
                    self.all_threads.add((x,y))

    def change_place(self, x, y):
        global green_sah_coor, purple_sah_coor
        if 0 <= x <= 7 and 0 <= y <= 7:
            global current_player
            if self.before_move == False and x == 7 and y == 6:
                self.green_right_rock()
            if self.before_move == False and x == 7 and y == 2:
                self.green_left_rock()
            if self.before_move == False and x == 0 and y == 6:
                self.purple_right_rock()
            if self.before_move == False and x == 0 and y == 2:
                self.purple_left_rock()

            if map[x][y] != "":map[x][y].button.grid_forget()
            self.delete_element_in_list(map[x][y])
            map[x][y] = self
            map[self.x][self.y] = ""
            self.x = x
            self.y = y
            if self.team == "green":
                green_sah_coor = (self.x, self.y)
            elif self.team == "purple":
                purple_sah_coor = (self.x, self.y)

            self.button.grid(row=x, column=y)
            all_moves.append([[i for i in row] for row in map])
            current_player = "green" if current_player == "purple" else "purple"
            self.before_move = True
            enemey_sah = green_sah_coor if self.team == "purple" else purple_sah_coor
            self.collect_all_threads()
            self.all_white()
            if enemey_sah in self.all_threads:
                tahta[enemey_sah[0]][enemey_sah[1]].config(highlightbackground="blue")
            elements = green_elements if current_player == "green" else purple_elements
            for x in elements:
                if x.check_illegal_move(): break
            else:
                a = Label(chess_frame, text="Oyun bitti", font=("helvetica", 30, "bold"))
                a.grid(row=2, column=2, columnspan=3)
            mapi_izle()

    def green_right_rock(self):
        map[7][5],map[7][7] = map[7][7],""
        map[7][5].button.grid(row=7, column=5)
        map[7][5].y = 5

    def green_left_rock(self):
        map[7][0],map[7][3] = "",map[7][0]
        map[7][3].button.grid(row=7, column=3)
        map[7][3].y = 3

    def purple_right_rock(self):
        map[0][5], map[0][7] = map[0][7], ""
        map[0][5].button.grid(row=0, column=5)
        map[0][5].y = 5

    def purple_left_rock(self):
        map[0][0], map[0][3] = "", map[0][0]
        map[0][3].button.grid(row=0, column=3)
        map[0][3].y = 3

    def check_illegal_move(self):
        enemy_object = green_elements[0] if self.team == "purple" else purple_elements[0]
        our_sah_coor = green_sah_coor if self.team == "green" else purple_sah_coor
        data = []
        for x, y in self.moves():
            save_sah_coor = our_sah_coor
            our_sah_coor = (x,y)
            enemy_tas = map[x][y]
            savex, savey = self.x, self.y
            map[x][y] = self
            map[self.x][self.y] = ""
            if enemy_tas != "": self.delete_element_in_list(enemy_tas)
            self.x, self.y = x, y
            enemy_object.collect_all_threads()
            info = not our_sah_coor in enemy_object.all_threads
            mapi_izle()
            self.x, self.y = savex, savey
            map[x][y] = enemy_tas
            map[self.x][self.y] = self
            if enemy_tas != "": enemy_object.all_elements.append(enemy_tas)
            if info: data.append((x, y))
            our_sah_coor = save_sah_coor
        return data


class Vezir(Common):
    def __init__(self, x, y, team):
        super().__init__()
        self.team = team
        self.x = x
        self.y = y
        self.point = 900
        self.all_elements = purple_elements if self.team == "purple" else green_elements
        self.all_threads = purple_threats if self.team == "purple" else green_threats
        self.enemy_all_elements = green_elements if self.team == "purple" else purple_elements
        self.enemy_all_threads = green_threats if self.team == "purple" else purple_threats
        self.button = Button(chess_frame, text="Vezir", font=("helvetica", 30, "bold"), fg= self.team, command=self.red_light)
        self.button.grid(row=self.x, column=self.y)

    def moves(self):
        data = []
        for num in range(1, 8):
            if 0 <= self.x + num <= 7 and 0 <= self.y + num <= 7:
                if map[self.x + num][self.y + num] == "" or map[self.x + num][self.y + num].team != self.team:
                    data.append((self.x + num, self.y + num))
                    if not map[self.x + num][self.y + num] == "": break

                else:
                    break

        for num in range(1, 8):
            if 0 <= self.x - num <= 7 and 0 <= self.y + num <= 7:
                if map[self.x - num][self.y + num] == "" or map[self.x - num][self.y + num].team != self.team:
                    data.append((self.x - num, self.y + num))
                    if not map[self.x - num][self.y + num] == "": break

                else:
                    break

        for num in range(1, 8):
            if 0 <= self.x - num <= 7 and 0 <= self.y - num <= 7:
                if map[self.x - num][self.y - num] == "" or map[self.x - num][self.y - num].team != self.team:
                    data.append((self.x - num, self.y - num))
                    if not map[self.x - num][self.y - num] == "": break
                else:
                    break

        for num in range(1, 8):
            if 0 <= self.x + num <= 7 and 0 <= self.y - num <= 7:
                if map[self.x + num][self.y - num] == "" or map[self.x + num][self.y - num].team != self.team:
                    data.append((self.x + num, self.y - num))
                    if not map[self.x + num][self.y - num] == "": break
                else:
                    break

        for num in range(1,8):
            if 0 <= self.y + num <= 7:
                if map[self.x][self.y + num] == "" or map[self.x][self.y + num].team != self.team:
                    data.append((self.x, self.y + num))
                    if map[self.x][self.y + num] != "":break
                else:break

        for num in range(1, 8):
            if 0 <= self.y - num <= 7:
                if map[self.x][self.y - num] == "" or map[self.x][self.y - num].team != self.team:
                    data.append((self.x, self.y - num))
                    if map[self.x][self.y - num] != "":break
                else:break


        for num in range(1, 8):
            if 0 <= self.x + num <= 7:
                if map[self.x + num][self.y] == "" or map[self.x + num][self.y].team != self.team:
                    data.append((self.x + num, self.y))
                    if map[self.x + num][self.y] != "":break
                else:break

        for num in range(1, 8):
            if 0 <= self.x - num <= 7:
                if map[self.x - num][self.y] == "" or map[self.x - num][self.y].team != self.team:
                    data.append((self.x - num, self.y))
                    if map[self.x - num][self.y] != "":break
                else:break
        return data


class Purple:
    def __init__(self):
        self.all_elements = purple_elements
        self.total_point = 0

        # Taşları oluşturmak
        self.all_elements.append(Kale(0, 0, "purple"))
        self.all_elements.append(Kale(0, 7, "purple"))
        self.all_elements.append(At(0,1, "purple"))
        self.all_elements.append(At(0,6, "purple"))
        self.all_elements.append(Fil(0,5, "purple"))
        self.all_elements.append(Fil(0,2, "purple"))
        self.all_elements.append(Vezir(0,3, "purple"))
        self.all_elements.append(Sah(0,4, "purple"))
        for x in range(8):
            self.all_elements.append(Piyon(1,x, "purple"))

        self.calculate_point()

        for element in self.all_elements:
            map[element.x][element.y] = element


    def calculate_point(self):
        t = 0
        for x in self.all_elements:
            t += x.point



class Green:
    def __init__(self):
        self.all_elements = green_elements
        self.total_point = 0

        # Taşları oluşturmak
        self.all_elements.append(Kale(7, 0, "green"))
        self.all_elements.append(Kale(7, 7, "green"))
        self.all_elements.append(At(7, 1, "green"))
        self.all_elements.append(At(7, 6, "green"))
        self.all_elements.append(Fil(7, 5, "green"))
        self.all_elements.append(Fil(7, 2, "green"))
        self.all_elements.append(Vezir(7, 3, "green"))
        self.all_elements.append(Sah(7, 4, "green"))
        for x in range(8):
            self.all_elements.append(Piyon(6, x, "green"))


        for element in self.all_elements:
            map[element.x][element.y] = element






class Interface:
    def __init__(self):
        self.team_purple = Purple()
        self.team_green = Green()



Interface()

root.mainloop()



