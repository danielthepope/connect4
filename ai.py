import colour
import random
import sys

debug = False #Set to True, and messages will be printed as it works out where
              #to go.
aiout = "" #Message which can be printed on the screen below the board during
           #gameplay.

def aiinput(board, currentsymbol):
    """The giant AI function, which when given a board in the form of a list,
    will perceive every available move, work out which is the best to go for
    and then return the column number."""
    global aiout
    #Slightly different variations
    def check3horiz(symbol):
        """
        Checks for a horizontal combination of 3 in a row of the given symbol.
        If it can be blocked or added to by the computer's move, that column
        number is returned. Else it returns -1 and the next check commences.
        """
        sys.stdout.write(debug * ("Checking" + str(symbol) + "horizontally\n"))
        combinations = []
        x = 0
        while x < len(board) - 2:
            y = 0
            while y < len(board[0]):
                if board[x][y] == symbol and board[x + 1][y] == symbol and \
                   board[x + 2][y] == symbol:
                    add = x, y
                    sys.stdout.write(debug * (
                        "3 in a row found horizontally at" + str(add) + "\n"))
                    combinations.append(add)
                y = y + 1
            x = x + 1
        for (x, y) in combinations:
            if x != 0:
                if y == 0 and board[x - 1][y] == ' ':
                    return x - 1
                elif board[x - 1][y - 1] != ' ' and board[x - 1][y] == ' ':
                    return x - 1
            if x + 3 != len(board):
                if y == 0 and board[x + 3][y] == ' ':
                    return x + 3
                elif board[x + 3][y - 1] != ' ' and board[x + 3][y] == ' ':
                    return x + 3
        #If there are no combinations, or no combinations that can be won,
        sys.stdout.write(debug * ("Nothing for me to block\n"))
        return -1

    def check3vert(symbol):
        """
        Checks for a vertical combination of 3 in a row of the given symbol.
        If it can be blocked or added to by the computer's move, that column
        number is returned. Else it returns -1 and the next check commences.
        """
        sys.stdout.write(debug * ("Checking" + str(symbol) + "vertically\n"))
        combinations = []
        x = 0
        while x < len(board):
            y = 2
            while y < len(board[0]):
                if board[x][y] == symbol and board[x][y - 1] == symbol and\
                   board[x][y - 2] == symbol:
                    add = x, y
                    sys.stdout.write(debug * (
                        "3 in a row found vertically at" + str(add) + "\n"))
                    combinations.append(add)
                y = y + 1
            x = x + 1
        for (x, y) in combinations:
            if y != len(board[0]) - 1:
                if board[x][y + 1] == ' ':
                    return x
        #If there are no combinations, or no combinations that can be won,
        sys.stdout.write(debug * ("Nothing for me to block\n"))
        return -1

    def check3diagdn(symbol):
        """
        Checks diagonally down-right for a combination of 3 in a row of the
        given symbol.
        If it can be blocked or added to by the computer's move, that column
        number is returned. Else it returns -1 and the next check commences.
        """
        sys.stdout.write(debug * ("Checking" + str(symbol)
                                  + "diagonally down right\n"))
        combinations = []
        x = 0
        while x < len(board) - 2:
            y = 2
            while y < len(board[0]):
                if board[x][y] == symbol and board[x + 1][y - 1] == symbol and \
                   board[x + 2][y - 2] == symbol:
                    add = (x, y)
                    sys.stdout.write(debug * (
                        "3 in a row found diagonally down-right at" + str(add)
                        + "\n"))
                    combinations.append(add)
                y = y + 1
            x = x + 1
        for (x, y) in combinations:
            if y < len(board[0]) - 1 and x > 0:
                if board[x - 1][y] != ' ' and board[x - 1][y + 1] == ' ':
                    return x - 1
            if x < len(board) - 3:
                if y == 3:
                    if board[x + 3][0] == ' ':
                        return x + 3
                if y > 3:
                    if board[x + 3][y - 3] == ' ' and board[x + 3][y - 4] != \
                       ' ':
                        return x + 3
        #If there are no combinations, or no combinations that can be won,
        sys.stdout.write(debug * ("Nothing to block\n"))
        return -1

    def check3diagup(symbol):
        """
        Checks diagonally up-right for a combination of 3 in a row of the
        given symbol.
        If it can be blocked or added to by the computer's move, that column
        number is returned. Else it returns -1 and the next check commences.
        """
        sys.stdout.write(debug * ("Checking" + str(symbol) +
                                  "diagonally up right\n"))
        combinations = []
        x = 0
        while x < len(board) - 2:
            y = 0
            while y < len(board[0]) - 2:
                if board[x][y] == symbol and board[x + 1][y + 1] == symbol and \
                   board[x + 2][y + 2] == symbol:
                    add = (x, y)
                    sys.stdout.write(debug * (
                        "3 in a row found diagonally up-right at" + str(add) +
                        "\n"))
                    combinations.append(add)
                y = y + 1
            x = x + 1
        for(x, y) in combinations:
            if y < len(board[0]) - 3 and x < len(board) - 3:
                if board[x + 3][y + 2] != ' ' and board[x + 3][y + 3] == ' ':
                    return x + 3
            if y > 0 and x > 0:
                if y == 1 and board[x - 1][y - 1] == ' ':
                    return x - 1
                if y > 1 and board[x - 1][y - 1] == ' ' and board[x - 1][y - 2]\
                   != ' ':
                    return x - 1
        #If there are no combination, or no combinations that can be won,
        sys.stdout.write(debug * ("Nothing to block\n"))
        return -1

    def check2horiz(symbol):
        """
        Checks for a horizontal combination of 2 in a row of the given symbol.
        If it can be blocked or added to by the computer's move, that column
        number is returned. Else it returns -1 and the next check commences.
        """
        sys.stdout.write(debug * ("Checking" + str(symbol) +
                                  "horizontally (x2)\n"))
        combinations = []
        x = 0
        while x < len(board) - 1:
            y = 0
            while y < len(board[0]):
                if board[x][y] == symbol and board[x + 1][y] == symbol:
                    add = x, y
                    sys.stdout.write(debug * ("2 in a row found horizontally at"
                                              + str(add) + "\n"))
                    combinations.append(add)
                y = y + 1
            x = x + 1
        for (x, y) in combinations:
            if x != 0:
                if y == 0 and board[x - 1][y] == ' ':
                    return x - 1
                elif board[x - 1][y - 1] != ' ' and board[x - 1][y] == ' ':
                    return x - 1
            if x + 2 != len(board):
                if y == 0 and board[x + 2][y] == ' ':
                    return x + 2
                elif board[x + 2][y - 1] != ' ' and board[x + 2][y] == ' ':
                    return x + 2
        #If there are no combinations, or no combinations that can be won,
        sys.stdout.write(debug * ("Nothing for me to block\n"))
        return -1

    def check2vert(symbol):
        """
        Checks for a vertical combination of 2 in a row of the given symbol.
        If it can be blocked or added to by the computer's move, that column
        number is returned. Else it returns -1 and the next check commences.
        """
        sys.stdout.write(debug * ("Checking" + str(symbol) + "vertically\n"))
        combinations = []
        x = 0
        while x < len(board):
            y = 1
            while y < len(board[0]):
                if board[x][y] == symbol and board[x][y - 1] == symbol:
                    add = x, y
                    sys.stdout.write(debug * ("2 in a row found vertically at"
                                              + str(add) + "\n"))
                    combinations.append(add)
                y = y + 1
            x = x + 1
        for (x, y) in combinations:
            if y != len(board[0]) - 1:
                if board[x][y + 1] == ' ':
                    return x
        #If there are no combinations, or no combinations that can be won,
        sys.stdout.write(debug * ("Nothing for me to block\n"))
        return -1

    def check2diagdn(symbol):
        """
        Checks diagonally down-right for a combination of 2 in a row of the
        given symbol.
        If it can be blocked or added to by the computer's move, that column
        number is returned. Else it returns -1 and the next check commences.
        """
        sys.stdout.write(debug * ("Checking" + str(symbol) +
                                  "diagonally down right(x2)\n"))
        combinations = []
        x = 0
        while x < len(board) - 1:
            y = 1
            while y < len(board[0]):
                if board[x][y] == symbol and board[x + 1][y - 1] == symbol:
                    add = (x, y)
                    sys.stdout.write(debug * (
                        "2 in a row found diagonally down-right at" + str(add)
                        + "\n"))
                    combinations.append(add)
                y = y + 1
            x = x + 1
        for (x, y) in combinations:
            if y < len(board[0]) - 1 and x > 1:
                if board[x - 1][y] != ' ' and board[x - 1][y + 1] == ' ':
                    return x - 1
            if x < len(board) - 2:
                if y == 2:
                    if board[x + 2][0] == ' ':
                        return x + 2
                if y > 3:
                    if board[x + 2][y - 2] == ' ' and board[x + 2][y - 3] != \
                       ' ':
                        return x + 2
        #If there are no combinations, or no combinations that can be won,
        sys.stdout.write(debug * ("Nothing to block\n"))
        return -1

    def check2diagup(symbol):
        """
        Checks diagonally up-right for a combination of 2 in a row of the
        given symbol.
        If it can be blocked or added to by the computer's move, that column
        number is returned. Else it returns -1 and the next check commences.
        """
        sys.stdout.write(debug * ("Checking" + str(symbol) +
                                  "diagonally up right (x2)\n"))
        combinations = []
        x = 0
        while x < len(board) - 1:
            y = 0
            while y < len(board[0]) - 1:
                if board[x][y] == symbol and board[x + 1][y + 1] == symbol:
                    add = (x, y)
                    sys.stdout.write(debug * (
                        "2 in a row found diagonally up-right at" + str(add)
                        + "\n"))
                    combinations.append(add)
                y = y + 1
            x = x + 1
        for(x, y) in combinations:
            if y < len(board[0]) - 2 and x < len(board) - 2:
                if board[x + 2][y + 1] != ' ' and board[x + 2][y + 2] == ' ':
                    return x + 2
            if y > 0 and x > 0:
                if y == 1 and board[x - 1][y - 1] == ' ':
                    return x - 1
                if y > 1 and board[x - 1][y - 1] == ' ' and board[x - 1][y - 2]\
                   != ' ':
                    return x - 1
        #If there are no combination, or no combinations that can be won,
        sys.stdout.write(debug * ("Nothing to block\n"))
        return -1
    #The AI is told which symbol it has to play, so it will play against the
    #other symbol.
    if currentsymbol == colour.red + "X" + colour.default:        
        comp = colour.red + "X" + colour.default
        human = colour.yellow + "O" + colour.default
    else:
        human = colour.red + "X" + colour.default
        comp = colour.yellow + "O" + colour.default
    aiout = ""
    
    #Working out the best place to move
    #Priority list with each function to check in sequence. If a check returns
    #a number, placecolumn in that number
    checks = ((check3horiz, comp), (check3vert, comp), (check3diagdn, comp),
              (check3diagup, comp), (check3horiz, human), (check3vert, human),
              (check3diagdn, human), (check3diagup, human), (check2horiz, comp),
              (check2diagup, comp), (check2diagdn, comp), (check2vert, comp),
              (check2horiz, human), (check2diagup, human),
              (check2diagdn, human))

    #Does all the checks in the priority list
    for (function, param) in checks:
        computermove = function(param)
        if computermove != -1:
            sys.stdout.write(debug * ("Intelligent"))
            #Adds a message to be printed underneath the board
            aiout = colour.green + "Computer's move: " + \
                    str(computermove + 1) + colour.default
            return computermove
    
    #If here, none of the priority checks worked, so go eenie meenie miney moe
    #and pick a random one
    while True:
        drop = random.randint(0, len(board)-1)
        if board[drop][-1] == ' ':
            sys.stdout.write(debug * ("Random"))
            #Adds a message to be printed underneath the board
            aiout = colour.green + "Computer's move: " + str(drop + 1) + \
                    colour.default
            return drop
        #else it will pick another random one
