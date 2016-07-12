import random
import re
ALPHA = 'ABCDEFGHIJ'
playerShips, computerShips, computerShots = [], [], []
destroy = False

class Ship:
    def __init__(self, owner, size):
        self.size = size
        self.owner = owner 
        self.pos = []
        if self.owner == 'computer':
            self.computerPlaceShip()
        else:
            self.playerPlaceship()  
 
    def checkVert(self,board, row, col):
        
        '''
            Iterates through proposed location of vertical
            ship to verify no other ship is in the way.
        '''

        for check in range(row, row+self.size): 
            if board[(check, col)] != '.':
                return False
        return True 

    def checkHoriz(self,board, row, col):

        '''
            Iterates through proposed location of horizontal
            ship to verify no other ship is in the way
        '''

        for check in range(col, col+self.size):
            if board[(row, check)] !='.':
                return False
        return True      

    def placeVert(self, start):

        '''
            Takes starting position for a vertical shipand adds 
            this ship to the board and to it's own pos list.
        '''

        r, c = start
        for row in range(r, r+self.size):
            board[(row, c)] = 'S'
            self.pos.append((row, c))                

    def placeHoriz(self, start):
        
        '''
            Takes starting position for a horizontal ship and adds
            this ship to the board and to it's own pos list.
        '''

        r,c = start
        for col in range(c, c+self.size):
            board[(r, col)] = 'S'
            self.pos.append((r,col))          
    
    def computerPlaceShip(self):  
    
        '''
            Randomizes direction of a hip then places ship on board
            for computer ships.
        '''

        def availVerts():
            
            '''
                Picks a column at random and makes a list
                of available positions to place ship in 
                that column
            '''

            avail = []
            while not avail:
                col = random.randint(0,9)
                for row in range(10):
                    if row+self.size<11 and self.checkVert(board, row, col):   
                        avail.append((row, col))
            return avail

        def availHoriz():
            
            '''
                Picks a row at random and makes a list
                of available positions to place ship in 
                that row
            '''

            avail = []
            while not avail:
                row = random.randint(0,9)
                for col in range(10):
                    if col+self.size<11 and self.checkHoriz(board, row, col):
                        avail.append((row, col))
            return avail

        def placeShip(availList, choice):

            '''
                Picks a position randomly from available posititions
                then places the ship on the board.
            '''

            start = random.choice(availList)
            if choice == 'v':
                self.placeVert(start)
            else:
                self.placeHoriz(start)            

        choice = random.choice(('v', 'h'))
        if choice == 'v':
            placeShip(availVerts(), choice)
        else:
            placeShip(availHoriz(), choice)
    
    def chooseDirection(self):

        '''
            Player input for direction of ship
            Two optional choices: 'v' and 'h'            
        '''

        valid = False
        while not valid:
            choice = raw_input('(h)orizontal or (v)ertical for the {} hole ship?'.format(self.size)) 
            if choice.upper() == 'H' or choice.upper()=='V':
                valid = True                    
        return choice   

    def choosePosition(self):

        '''
            Player input for position of ship
        '''

        valid = False
        while not valid:    
            pos = raw_input('What posistion (row,col) to place the ship?')
            if testInput(pos):
                valid = True
        return pos

    def playerPlaceship(self):
        
        '''
            Function to find a place for each of the players' ships.
        '''

        valid = False
        while not valid:
            printBoard() 
            validInput = False
            choice = self.chooseDirection()
            pos = self.choosePosition()
            row, col = separateInput(pos)
            col += 10   #The player owns the board on the right. all cols are offset by 10
            if choice.upper() == 'V':
                if self.size+row<11: #keeps the ship on the board
                    if self.checkVert(board, row, col): #make sure player has valid location
                        self.placeVert((row, col))
                        valid = True
                    else: 
                        print '\n'*10+"The ship does not fit there"+'\n'*10
                else:
                    print '\n'*10+"Please keep it on the board. Try setting it a little higher."+'\n'*10
            else:
                if self.size+col<21: #keeps the ship on the board
                    if self.checkHoriz(board, row, col): #make sure player has valid location
                        self.placeHoriz((row, col))
                        valid = True
                    else:
                        print '\n'*10+"The ship does not fit there"+'\n'*10
                else:
                    print '\n'*10+"Please keep it on the board. Try setting it a little to the left"+'\n'*10
            

def testInput(inp):

    '''
        Determines if player input is valid
    '''

    return re.match(r'[a-j](?:10|[1-9])$', inp) 

def separateInput(inp):

    '''
        Separates player input from visual row & col
        Returns usable row and col
    '''

    row, col = inp[0], inp[1:]
    return (ALPHA.index(row.upper()), int(col)-1)   

def buildBoard():

    '''
        Returns two blank boards. 
        The first is the visual board for the player
        The second is the board for the computer to make it's decisions.
    '''

    return {(x,y):'.' for x in range(10) for y in range(20)}, {(x,y):'.' for x in range(10) for y in range(10, 20)}    

def addShips():

    '''
        Iterates through ship sizes and creates ships of those sizes
        for both the player and the computer.
    '''

    for size in [5, 4, 3, 3, 2]:
        computerShips.append(Ship('computer', size))
        playerShips.append(Ship('player', size))

def printBoard():

    '''
        Displays the board for the player.
    '''

    print '             COMPUTER                             PLAYER'
    print '   1  2  3  4  5  6  7  8  9  10        1  2  3  4  5  6  7  8  9  10\n'
    for x in range(10):
        print ALPHA[x]+' ',
        for y in range(20):
            display = '.' if board[(x,y)]=='S' and y<10 else board[(x,y)]
            print display+' ',
            if y==9: print '    {} '.format(ALPHA[x]),
        print'\n'
    
def playerShoots():

    '''
        User inputs shot. function validates input and returns
        tuple with row, col.
    '''

    validInput = False    
    while not validInput:
        shot = raw_input('SHOOT >')
        if testInput(shot):
            validInput = True
            return separateInput(shot)            
    
def computerSearch(destroy):

    '''
        Computer radomizes shot
        Verifies if shot is new
        Adds shot to shot list
        changes the board.
    '''

    validShot = False
    while not validShot:
        rowShot = random.randint(0, 9)
        colShot = random.randint(10, 19)
        shot = (rowShot, colShot)
        if shot not in computerShots:
            computerShots.append(shot)
            validShot = True
            if board[shot] == '.':
                board[shot] = ' '
                computerBoard[shot] = ' '
                return shot, False
            else:
                board[shot] = 'H'
                computerBoard[shot] = 'H'
                hitPlayerShip(shot)
                return shot, True

def computerDestroy(lastShot):
    print "Last Shot", lastShot
    search()
    
def computerShoots(destroy):
    print 'destroy = ', destroy
    if destroy:
        computerDestroy(lastShot)        
    else:
        lastShot, destroy = computerSearch(destroy)


def hitPlayerShip(shot):
    for ship in playerShips:
        for spot in ship.pos:
            if shot == spot:
                ship.pos[ship.pos.index(shot)]="H"
                if ship.pos.count("H")==ship.size:
                    print "He sunk your ship"
                    playerShips.pop(playerships.index(ship))
    

def hitComputerShip(shot):

    '''
        When a computer Ship is hit, the ship changes it's hole from 'S'
        to 'H' then checks if it has been sunk. If sunk, it's removed from
        computerShips list.
    '''

    for ship in computerShips:
        for spot in ship.pos:
            if shot == spot:
                ship.pos[ship.pos.index(shot)]="H"
                if ship.pos.count("H")==ship.size:
                    print "YOU \n\n\n\n    SUNK \n\n\n\n           MY \n\n\n\n               SHIP!!!!"
                    computerShips.pop(computerShips.index(ship))

######################### MAIN ################################
board, computerBoard = buildBoard()
addShips()
while computerShips:
    newShot = False
    printBoard()
    print
    while not newShot:
        shot = playerShoots()
        if board[shot] == '.':
            board[shot] = ' '
            print "\n"*10+random.choice(["Nothing But Water", 
                                         "YOU MISSED", 
                                         "What a great wave you made", 
                                         "AIRBALL!!!"])+"\n"*10
            newShot = True
        elif board[shot] == 'S':
            board[shot] = 'H'
            hitComputerShip(shot)
            newShot = True
        else:
            print "Didn't you already do that? Try a new shot please."
    computerShoots(destroy)
printBoard()


