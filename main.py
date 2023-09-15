##
# @mainpage     Kanoodle Solver
# @author       Daniel Epstein
# @date         August 20, 2023
# @purpose      The game Kanoodle consists of placing colored pieces 
#               on a rectangular board. This takes the starting position
#               and finds all viable solutions (if one exists).               

# Imports
from board import Board
from piece import Piece
from menu import Menu

##
# @function     startPiece
# @purpose      Starts a piece on the board
# @param        board - the board to put the pieces on
# @param        p - the piece to start
# @param        coords - the starting coordinate of the piece p
def startPiece(board, p, coords):

    # Move to starting position
    p.shape = coords.copy()
    board.placePiece(p)

    # Remove the pieces spaces from the open list
    for c in p.shape:
        board.opens.remove(c)
    

##
# @function     tryPlace
# @purpose      Recursively places all the pieces on the board in every avaliable viable position
# @param        pieces - the list of pieces that still need to be added
# @param        opens - the list of open spots remaining on the board
def tryPlace(pieces, opens):

    # Next piece to place is the first piece in pieces
    p = pieces[0]

    # For each orientation
    for j in range(p.flips):
        for i in range(p.rots):

            # Copy the opens to a local copy for the current piece
            pc = opens.copy()
            for c in pc:

                # For each open spot, 
                # 1 - move to the open spot,
                # 2 - if that is a valid placement, place the piece, then tryPlace next piece
                # 3 - remove the piece and try next spot

                # Move to open and check placement
                p.moveToOpen(c)
                if(board.isValidPlacement(p)):
                    board.placePiece(p)
                    #If there are more pieces to place, place the next piece
                    if(len(pieces) > 1):
                        # Copy the open spaces minus the spaces being taken up by the current piece
                        temp = opens.copy()
                        for t in p.shape:
                            temp.remove(t)
                        # Place the next piece
                        tryPlace(pieces[1:], temp)
                    else:
                        # Placed the last piece! Print the board
                        print(board)

                    # There aren't anymore solutions with this current placement, remove piece and try next                
                    board.removePiece(p)

            # Rotate the piece to try that solution
            p.rotate90()
        # Flip the piece to try that solution
        p.flip()

##
# @function     Main
if __name__ == "__main__":

    # The game board
    board = Board() 

    # Initialize each piece, starting at [-1, -1]
    # Pieces must start off the board, so that they can be moved to any position on the board 
    purple = Piece('P', [[-1, -1], [0, -1], [1, -1], [2, -1]], 2, 1)
    red = Piece('R', [[-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0]], 4, 2)
    lightpink = Piece('p', [[-1, -1], [-1, 0], [-1, 1], [0, 1], [-1, 2]], 4, 2)
    white = Piece('W', [[-1, -1], [-1, 0], [0, -1]], 4, 1)
    lightgreen = Piece('g', [[-1, -1], [0, -1], [-1, 0], [0, 0]], 1, 1)
    lightblue = Piece('b', [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1]], 4, 1)
    blue = Piece('B', [[-1, -1], [0, -1], [0, 0], [0, 1], [0, 2]], 4, 2)
    silver = Piece('+', [[-1, -1], [-2, -1], [-1, -2], [-1, 0], [0, -1]], 1, 1)
    yellow = Piece('Y', [[-1, -1], [0, -1], [1, -1], [1, 0], [-1, 0]], 4, 1)
    green = Piece('G', [[-1, -1], [-1, 0], [-1, 1], [0, 1], [0, 2]], 4, 2)
    pink = Piece('M', [[-1, -1], [0, -1], [0, 0], [1, 0], [1, 1]], 4, 1)
    orange = Piece('O', [[-1, -1], [0, -1], [0, 0], [0, 1]], 4, 2)

    # Pieces arranged in order of size to place the larger pieces first
    pieces = [silver, yellow, pink, green, lightpink, lightblue, red, blue, lightgreen, orange, purple, white]
    # silver, yellow, pink, green, lightpink, lightblue, red, blue, lightgreen, orange, purple, white


    # Start the Menu
    menu = Menu(pieces)
    starters = menu.run()
    menu.clear_screen()

    # Start all the pieces returned and then remove them from the pieces list
    removals = []
    for s in starters:
        startPiece(board, pieces[s.index], s.piece.shape)
        removals += [s.index]
    
    # Place all the remaining pieces!
    needsplace = [pieces[i] for i in range(len(pieces)) if i not in removals]
    tryPlace(needsplace, board.opens)
        