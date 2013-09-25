#!/usr/bin/env python

import sys
import os
import pickle
import time
#Then my own modules
import colour
import ai

def start():
    """Prints a welcome message and starts a new game or loads one depending on
    the user's input."""
    global savedgameexists
    global player1name
    global player2name
    global aion
    player1name = ""
    player2name = ""
    print title()
    print "Welcome to Connect 4, by Daniel Pope."
    print
    #Enables colours for consoles which do support colour (i.e. not Windows)
    try:
        if raw_input("Does your console support colours? (y/n) ") == "y":
            colour.enable()
            #All colour.* cariables are set the appropriate escape character to
            #turn the console text to the correct colour.
        else:
            print "In compatibility mode for monochrome consoles."
            #All colour.* variables are set to blank, so they won't print
            #anything to the console.
    except EOFError:
        closesequence()
    print
    print colour.cyan + "To start a new game, type 'new' followed by enter"
    if savedgame() == True: #Checks if there is saved data
        savedgameexists = True
        print
        print "Saved game detected."
        print "To load the previously saved game, type 'load' then enter."
        print
    print "For other commands, type 'help' followed by enter" + colour.default
    while True:
        try:
            userinput = raw_input()
        except EOFError:
            closesequence()
        if userinput.lower() == "new":
            sys.stdout.write(colour.cyan + \
                             "Enter number of human players (0, 1 or 2): " + \
                             colour.default)
            while True:
                try:
                    inp = raw_input()
                except EOFError:
                    closesequence()
                if inp == '1':
                    aion = 1
                    break
                elif inp == '2':
                    aion = 0
                    break
                elif inp == '0':
                    aion = 2
                    break
                sys.stderr.write(colour.red + \
                                 "Enter 1 or 2, or 0 will play its own game.\n"\
                                 + colour.default)
            firstrun()
            break
        elif userinput.lower() == "load" and savedgameexists == True:
            #Only available if there is a saved game
            load()
            break
        elif userinput.lower() == "delete" and savedgameexists == True:
            deletesavedgame()
            firstrun()
            break
        elif userinput.lower() == "quit":
            closesequence()
        elif userinput.lower() == "readme":
            readme()
        elif userinput.lower() == "help":
            print colour.cyan + "Type one of the following commands followed "\
                  + "by enter:"
            print "new\tStarts a new game."
            print "quit\tExits the game."
            print "readme\tDisplays the complete help file."
            if savedgameexists == True:
                #Makes sure the user is only given the instructions they can use
                print "load\tResumes the game from the saved checkpoint."
                print "delete\tDeletes the saved game."
            sys.stdout.write(colour.default)
        else:
            sys.stderr.write(colour.red + "Invalid entry. Type 'help' then" \
                             + " enter for help.\n" + colour.default)
            continue

def readme():
    """Prints the readme text file on the screen"""
    sys.stdout.write(colour.magenta)
    helpfile = open("README", "r")
    for line in helpfile.readlines():
        sys.stdout.write(line)
    helpfile.close()
    sys.stdout.write(colour.default)
    return

def savedgame():
    """Checks if a saved game exists"""
    try:
        savedata = open("savedata", "r")
        savedata.close()
        return True
    except:
        return False

def load():
    """Loads the saved data file, sets global variables and resumes the game."""
    savedata = open("savedata", "r")
    global player1name
    global player2name
    global player1score
    global player2score
    global col
    global row
    global grid
    global numberofmoves
    global resumestate
    global aion
    player1name = pickle.load(savedata)
    player2name = pickle.load(savedata)
    player1score = pickle.load(savedata)
    player2score = pickle.load(savedata)
    col = pickle.load(savedata)
    row = pickle.load(savedata)
    grid = pickle.load(savedata)
    numberofmoves = pickle.load(savedata)
    resumestate = pickle.load(savedata)
    aion = pickle.load(savedata)
    savedata.close()
    print colour.cyan + playerscores() + colour.default
    #Resumes the game from wherever left off. If the saved game was in progress,
    #resumestate() will call play(). If a new game needs to start, new() is
    #called instead.
    resumestate()
    
def deletesavedgame():
    """Deletes the saved data file"""
    os.remove("savedata")
    print colour.green + "Deleted. Starting new game." + colour.default
    print
    return

def firstrun():
    """Inputs players' names, then starts a new game"""
    global player1name
    global player2name
    global player1score
    global player2score
    player1score = 0
    player2score = 0
    player1name, player2name = getnames()
    print
    new()
    
def new():
    """Starts a new game"""
    global col
    global row
    global numberofmoves
    print colour.cyan + "What size grid would you like?"
    while True:
        try:
            col = input(colour.cyan + " Width: " + colour.default)
            row = input(colour.cyan + "Height: " + colour.default)
        except EOFError:
            closesequence()
        except:
            sys.stderr.write(colour.red + "Invalid input, try again.\n" + \
                             colour.default)
            continue
        #Sets limits between 4x4 and 19x17 grid
        if col < 4 or row < 4 or col > 19 or row > 17:
            sys.stderr.write(colour.red + "Row and column lengths must be "\
                             + "between 4 and 19.\n" + colour.default)
            continue
        break
    makegrid(col, row) #Makes the list nest where counters get stored.
    numberofmoves = 0
    play() #Now all variables have been set, standard gameplay starts.
    return

def playerscores():
    """
    Returns the player names, the character of their counter and their scores.
    """
    return colour.green + "\nScores:\nO  " + player1name + ": " + \
           str(player1score) + "\nX  " + player2name + ": " + str(player2score)\
           + "\n" + colour.default

def getnames():
    """Allows the input of 2 player's names"""
    #If AI is being used, set the names automatically
    if aion == 1:
        p1 = "You"
        p2 = "Computer"
    elif aion == 2:
        p1 = "Computer 1"
        p2 = "Computer 2"
    else:
        try:
            p1 = raw_input(colour.cyan + "Player 1, please enter your name: " \
                           + colour.default)
            p2 = raw_input(colour.cyan + "Player 2, please enter your name: " +\
                           colour.default)
        except EOFError:
            closesequence()
        #Names cannot be blank or equal to each other.
        if p1 == p2 or p1 == "" or p2 == "":
            sys.stderr.write(colour.red + "Invalid names. They cannot be left" \
                             + "blank or the same.\n" + colour.default)
            return getnames()
    print
    print colour.green + p1 + " will use O, " + p2 + " will use X." + \
          colour.default
    return (p1, p2)

def makegrid(c, r):
    """Defines a new grid list, where the counters are stored."""
    global grid
    global col
    global row
    grid = [] #Erase contents of the grid to start afresh
    col = c #Changes col and row to the parameters entered
    row = r
    y = 0 #Make a list defining a blank column
    ylist = []
    while y < row:
        ylist.append(' ')
        y = y + 1
    x = 0 #Define a row, each with a COPY of ylist to make a nested list
    while x < col:
        grid.append(ylist[:])
        x = x + 1
    return

def printgrid():
    """Gives a graphical representation of grid, in a form the user can
    understand"""
    def intersection():
        """Returns a horizontal line to space each row out"""
        return colour.blue + " " * (40 - (2 * col)) + "|" + ("---|" * col) + \
               colour.default
    def printrow(rowno):
        """Returns a spaced out version of a given row"""
        x = 0
        out = " " * (40 - (2 * col)) + colour.blue + "|"
        while x < col:
            #adds the element from each column on the same row with a spacer
            out = out + " " + grid[x][rowno] + colour.blue + " |"
            x = x + 1
        return out + colour.default
    #The first line gets printed with column headings
    x = 0
    line1 = " " * (40 - (2 * col))
    while x < col:
        line1 = line1 + "  " + str(x + 1)
        if x < 9: #Adds an extra space in place of the second digit taken by
                  #higher numbers
            line1 = line1 + " "
        x = x + 1
    print colour.white + line1 + colour.default #Prints the number headings
    x = row - 1 #Working backwards - row 0 is the bottom of the board
    while x >= 0:
        print intersection()
        print printrow(x)
        x = x - 1
    print intersection()
    print colour.white + line1 + colour.default
    print
    return

def minigrid():
    """Prints a small version of the grid, suitable for portable devices."""
    x = 0
    line1 = ""
    while x < col:
        line1 = line1 + str(x + 1)[-1]
        x = x + 1
    print colour.white + line1 + colour.default
    y = row - 1
    while y >= 0:
        out = ""
        x = 0
        while x < col:
            out = out + grid[x][y]
            x = x + 1
        print out
        y = y - 1
    print colour.white + line1 + colour.default
    print
    return

def title():
    """Displays the title spread, used at the top of each stage in the game"""
    printlines(2)
    return colour.green + "#" * 80 + "\n" + "#" * 35 + colour.white + \
           " Connect 4 " + colour.green + "#" * 34 + "\n" + "#" * 80 + "\n" + \
           colour.default

def play():
    """Standard gameplay, when all the global variables have been set"""
    global numberofmoves
    global player1score
    global player2score
    global resumestate
    resumestate = play #If saved, game will resume here
    print
    print colour.green + "Type 'help' followed by enter to learn other useful" \
          + " commands" + colour.default
    while numberofmoves < col * row: #If board is full, leave the loop
        print title()
        printmode()
        if (aion == 1 and numberofmoves % 2 == 0) or aion == 2:
            print ai.aiout
            ai.aiout = ""
        else:
            print
        #Even number - player 1's turn, odd number - player 2's turn
        if numberofmoves % 2 == 0:
            print colour.cyan + player1name + ", it's your turn (O)." + \
                  colour.default
            #Inserts this character into the grid
            currentsymbol = colour.yellow + "O" + colour.default
        else:
            print colour.cyan + player2name + ", it's your turn (X)." + \
                  colour.default
            currentsymbol = colour.red + "X" + colour.default
        #As well as checking for column numbers, getuserinput also checks for
        #commands.
        if (aion == 1 and numberofmoves % 2 == 1) or aion == 2:
            time.sleep(1.5)
            placecounter(currentsymbol, ai.aiinput(grid, currentsymbol))
        else:
            column = getuserinput("all")
            placecounter(currentsymbol, column)
        if checkwinner() == True: #Checks for winners
            resumestate = new #If saved now, it will resume starting a new game
            print title()
            printmode()
            sys.stdout.write(colour.green)
            #The last player to place a counter wins
            if aion == 2:
                print ai.aiout
                ai.aiout = ""
            if numberofmoves % 2 == 0:
                print "Winner! Well done " + player1name
                player1score = player1score + 1
            else:
                if aion == 1 and numberofmoves % 2 == 1:
                    print ai.aiout
                    ai.aiout = ""
                print "Winner! Well done " + player2name
                player2score = player2score + 1
            sys.stdout.write(colour.default)
            print playerscores()
            getuserinput("command") #Only checks for commands
        numberofmoves = numberofmoves + 1
    #When there are no more moves available, this code is executed
    print title()
    printmode()
    sys.stderr.write(colour.red + "No more available moves!\n" + colour.default)
    resumestate = new
    getuserinput("command")
    return

def getuserinput(config):
    """Checks if the user's input is valid. Also checks for commands"""
    def commands():
        global printmode
        """Looks through this list and executes the relevant code"""
        if command.lower() == "quit":
            closesequence()
        elif command.lower() == "save":
            save()
            return getuserinput(config)
        elif command.lower() == "new":
            new()
        elif command.lower() == "restart":
            start()
        elif command.lower() == "scores":
            print playerscores()
            return getuserinput(config)
        elif command.lower() == "load":
            if savedgame() == True:
                load()
            else:
                sys.stderr.write("No saved file exists!")
                return getuserinput(config)
        elif command.lower() == "readme":
            readme()
            return getuserinput(config)
        elif command.lower() == "help":
            sys.stdout.write(colour.magenta)
            print "Type one of the following commands followed by enter:"
            print "new\tClears the board and starts the round again, whilst"
            print "\tkeeping player names and scores in memory."
            print "restart\tStarts the game completely afresh: resets the"
            print "\tscores and player names as well."
            print "scores\tDisplays the players' current scores."
            print "save\tSaves the current game to be resumed from that point."
            if savedgame() == True:
                print "load\tLoads the game from the saved checkpoint."
            print "quit\tCloses the window."
            print "readme\tDisplays the whole readme file in the console."
            print "mini\tDisplays a smaller version of the grid in the future."
            print "large\tDisplays large grids in the future."
            print colour.default
            return getuserinput(config)
        elif command.lower() == "mini":
            printmode = minigrid
            print "Mini print mode selected."
            return getuserinput(config)
        elif command.lower() == "large":
            printmode = printgrid
            print "Large print mode selected."
            return getuserinput(config)
        else:
            sys.stderr.write(colour.red + "Unrecognised input. Type 'help' " \
                             + "followed by enter for more information.\n" + \
                             colour.default)
            return getuserinput(config)
    sys.stdout.write(colour.cyan)    
    if config == "all": #Different message, depending on what it is looking for
        sys.stdout.write("Enter a column number to drop your counter: ")
    else:
        sys.stdout.write("Enter a command name to continue: ")
    sys.stdout.write(colour.default)
    try:
        command = raw_input()
    except EOFError:
        closesequence()
    if config == "all": #'all' checks for numbers or commands
        try:
            colselection = int(command)
        except: #If it's not a number, it'll be a command.
            return commands()
    else: #'command' just checks for commands
        return commands()
    if colselection < 1 or colselection > col:
        sys.stderr.write(colour.red + "Invalid column number.\n" + \
                         colour.default)
        return getuserinput(config)
    #Checks if the top value in a column is occupied or not.
    elif grid[colselection - 1][row - 1] != ' ':
        sys.stderr.write(colour.red + "Column full. Pick another.\n" + \
                         colour.default)
        return getuserinput(config)
    else:
        return colselection - 1

def placecounter(symbol, column):
    """Lets a counter drop to the lowest available space on the board"""
    rowcheck = 0 #Checks the bottom one first
    while rowcheck < row:
        if grid[column][rowcheck] == ' ':
            grid[column][rowcheck] = symbol
            break
        else:
            rowcheck = rowcheck + 1 #Look at the next highest one
    return

def checkwinner():
    """
    Checks the whole board to find an instance of 4 counters in a row.
    Works on any board size
    """
    #Check horizontally
    x = 0
    while x < col - 3:
        y = 0
        while y < row:
            if grid[x][y] != ' ' and grid[x][y] == grid[x + 1][y] == \
               grid[x + 2][y] == grid[x + 3][y]:
                return True
            y = y + 1
        x = x + 1
    #Check vertically
    x = 0
    while x < col:
        y = 3
        while y < row:
            if grid[x][y] != ' ' and grid[x][y] == grid[x][y - 1] == \
               grid[x][y - 2] == grid[x][y - 3]:
                return True
            y = y + 1
        x = x + 1
    #Diagonally, down right
    x = 0
    while x < col - 3:
        y = 3
        while y < row:
            if grid[x][y] != ' ' and grid[x][y] == grid[x + 1][y - 1] == \
               grid[x + 2][y - 2] == grid[x + 3][y - 3]:
                return True
            y = y + 1
        x = x + 1
    #Diagonally, up right
    x = 0
    while x < col - 3:
        y = 0
        while y < row - 3:
            if grid[x][y] != ' ' and grid[x][y] == grid[x + 1][y + 1] == \
               grid[x + 2][y + 2] == grid[x + 3][y + 3]:
                return True
            y = y + 1
        x = x + 1
    return False
            

def save():
    """
    Saves the game to the file savedata in the same order as the load
    sequence
    """
    savedata = open("savedata", "w")
    pickle.dump(player1name, savedata)
    pickle.dump(player2name, savedata)
    pickle.dump(player1score, savedata)
    pickle.dump(player2score, savedata)
    pickle.dump(col, savedata)
    pickle.dump(row, savedata)
    pickle.dump(grid, savedata)
    pickle.dump(numberofmoves, savedata)
    pickle.dump(resumestate, savedata)
    pickle.dump(aion, savedata)
    savedata.close()
    print colour.green + "Checkpoint saved." + colour.default
    return

def closesequence():
    """Prompts the user to save if necessary, then exists gracefully."""
    if player1name != "":
        #This means there could be something to save, so prompt the user
        print colour.cyan + "Would you like to save first? (y/n)" + \
              colour.default
        try:
            yn = raw_input()
        except EOFError:
            closesequence()
        if yn == "y":
            save()
    sys.exit()

def printlines(x):
    """Prints a given number of lines"""
    i = 0
    while i < x:
        print
        i = i + 1
    return

#Now a load of global variables...
grid = [] #Nested lists containing data for each cell
col = 0 #Defines the width
row = 0 #Defines the height
numberofmoves = 0 #Counts the number of moves played in the game
player1name = ""
player2name = ""
player1score = 0 #Number of games each player has won
player2score = 0
resumestate = new #This decides how to load a game. Saved in the savefile
printmode = printgrid #Default printing method. Not saved in the savefile
aion = 0
savedgameexists = False

#And this final function gets it all going :)
start()
