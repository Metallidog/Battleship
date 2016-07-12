from tkinter import *
from collections import OrderedDict
import random


tk=Tk()
canvas = Canvas(tk, width = 900, height = 400)
canvas.pack()
board_squares = []
computer_board = []
game_text = ''
game_state = 'place ships'
comp_ships = OrderedDict([('Carrier', {'size': 5, 'hole_list':[]}), 
                          ('Battleship', {'size': 4, 'hole_list':[]}), 
                          ('Submarine', {'size': 3, 'hole_list': []}), 
                          ('Destroyer', {'size': 3, 'hole_list': []}), 
                          ('Patrol', {'size': 2, 'hole_list': []}) ])
player_ships = OrderedDict([('Carrier', {'size': 5, 'hole_list':[]}), 
                            ('Battleship', {'size': 4, 'hole_list':[]}), 
                            ('Submarine', {'size': 3, 'hole_list': []}), 
                            ('Destroyer', {'size': 3, 'hole_list': []}), 
                            ('Patrol', {'size': 2, 'hole_list': []}) ])

class Hole:
    def __init__(self, row, col, pos, sq_color, cr_color):
        row = row if 400%(row+1)<400 else row+100 #make a space between boards
        self.sq_range = (row, col, row+40, col+40)
        self.cr_range = (row+10, col+10, row+30, col+30)
        self.sq_color = sq_color
        self.cr_color = cr_color
        self.pos = pos      
        self.content = 'water' 

    def draw(self):
        canvas.create_rectangle(self.sq_range, fill=self.sq_color)
        canvas.create_oval(self.cr_range, fill=self.cr_color)        
    

def init_board():
    position = 0
    for row in range(0,800,40):
        for col in range(0,400,40):
            hole = Hole(row, col, position, 'green', 'white')
            board_squares.append(hole)
            position += 1

def pick_random_hole(size):
    hole = random.randint(0,99)    
    return {'up': (hole//10==(hole-size+1)//10, [h for h in range(hole-size+1,hole+1)]), 
               'down': (hole//10==(hole+size-1)//10, [h for h in range(hole, hole+size)]),
               'left': (hole-((size-1)*10)>-1, [h for h in range(hole-((size-1)*10),hole+1, 10 )]),
               'right':(hole+((size-1)*10)<100, [h for h in range(hole, hole+((size-1)*10)+1, 10)])
               }, hole   
    
def find_room(size):
    choices = ['up', 'down', 'left', 'right']
    dir_dic, hole = pick_random_hole(size)
    while True:
        if not choices: 
            choices = ['up', 'down', 'left', 'right']
            dir_dic, hole = pick_random_hole(size) #in case no directions work for original hole
        random.shuffle(choices)
        choice = choices.pop()
        if dir_dic[choice][0] and\
           [board_squares[h].content for h in dir_dic[choice][1]].count('water')==size: 
            for h in dir_dic[choice][1]:
                #board_squares[h].sq_color = 'grey'
                board_squares[h].content = 'ship'     
            return dir_dic[choice][1] 
   
def add_ships():
    for ship in comp_ships:
        comp_ships[ship]['hole_list'] = find_room(comp_ships[ship]['size'])
    draw_board()
                
def draw_board():
    for hole in board_squares:
        hole.draw()

def find_pos(event):
    x, y = event.x, event.y
    if x<400:
        for hole in board_squares:
            if event.x>hole.sq_range[0] and\
               event.y>hole.sq_range[1] and\
               event.x<hole.sq_range[2] and\
               event.y<hole.sq_range[3]:
                change_color(hole)
    
def check_for_sink(hole):
    for ship in comp_ships:
        if hole.pos in comp_ships[ship]['hole_list']:
            comp_ships[ship]['hole_list'].remove(hole.pos)
            print (ship, comp_ships[ship]['hole_list'])    
            if len(comp_ships[ship]['hole_list'])==0:
                print ('you sunk my ship') 
  
def get_player_ship():
    for size in [5,4,3,3,2]:
        yield size
 
def player_place_ships():        
        try: 
            size = next(gps)      
            #size = player_ships[ship]['size']
            draw_placement_ships(size)        
            return ('place ships', size)       
        except StopIteration:
            return ('play', 0)  

def choose_horiz_vert(event):
    if 400 < event.x < 500 and 10 < event.y < 45:
        return 'horizontal'
    elif 400 < event.x < 430 and 45 < event.y < 180:
        return 'vertical'
    

def draw_placement_ships(size): 
    canvas.create_rectangle(405,10,405+(size*18),40, fill='blue')
    canvas.create_rectangle(405,50,425,50+(size*25), fill='blue')
    for h in range(size):
        canvas.create_oval(405+(18*h), 14, 420+(18*h), 36, fill='yellow')
        canvas.create_oval(407, 50+(25*h), 423, 71+(25*h), fill='yellow')
    
def change_color(hole):
    if hole.content == 'ship':
        hole.content = 'HIT'
        hole.cr_color = 'red'
        check_for_sink(hole)
    elif hole.content == 'water':
        hole.content = 'MISS'
        hole.cr_color = 'gray'
    draw_board()

def event_handler(event):
    global game_state
    if game_state == 'place ships':   
        dir_choice = choose_horiz_vert(event)
        if dir_choice: 
            canvas.create_rectangle(401, 1, 499, 300, fill='gray')
            game_state, size = player_place_ships()   
            print (dir_choice, size)
    else:
        find_pos(event)

gps = get_player_ship()
init_board()
draw_placement_ships(5)
add_ships()
canvas.bind("<Button-1>", event_handler)
mainloop()
