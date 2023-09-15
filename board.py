##
# @file         Board.py
# @author       Daniel Epstein
# @date         August 20, 2023
# @purpose      A class that represents a kanoodle board

# Imports
import piece

class Board():

    ##
    # @function     init
    # @purpose      Board constructor. Creates an instance of the Board
    # @param        self - the Board instance
    def __init__(self):
        self.board = []
        self.opens = []
        for i in range(5):
            self.board.append(['X'] * 11)
            for j in range(11):
                self.opens.append([i, j])

    ##
    # @function     str
    # @purpose      String version of the board so it can be printed
    # @param        self - the Board instance
    def __str__(self):
        bstr = ""
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                # Changes the ANSI Code to print the board in colors close to the actual pieces
                s=""
                match self.board[r][c]:
                    case 'P':   
                        s="\033[0;35m"
                    case 'R':
                        s="\033[0;31m"
                    case '+':
                        s="\033[0;37m"
                    case 'W':
                        s="\033[1;37m"
                    case 'p':
                        s="\033[1m"
                    case 'b':
                        s="\033[1;34m"
                    case 'B':
                        s="\033[0;34m"
                    case 'g':
                        s="\033[1;32m"
                    case 'G':
                        s="\033[0;32m"
                    case 'Y':
                        s="\033[1;33m"
                    case 'O':
                        s="\033[0;31m"
                    case 'M':
                        s="\033[1;35m"
                    case _:
                        s="\033[1;30m"
                bstr += s + self.board[r][c] + "\033[0m "
            bstr +="\n"
        return bstr

    ##
    # @function     isEmptySpot
    # @purpose      Checks if a given spot on the board is not currently holding a piece
    # @param        self - the Board instance
    # @param        r - the row of the spot to check
    # @param        c - the column of the spot to check
    def isEmptySpot(self, r, c):
        return self.board[r][c] == 'X'

    ##
    # @function     isValidPlacement
    # @purpose      Checks if the current position of a piece is a valid placement for that piece
    # @param        self - the Board instance
    # @param        piece - the piece to check the placement of
    def isValidPlacement(self, piece):
        # A placement is valid if 
        # - all the coordinates that make up the shape are on the board and currently empty
        # - placing the piece here would not isolate any other open spaces, 
        # thus making it impossible to place a piece there
        for c in piece.shape:
            if(c[0] < 0 or c[0] > 4 or c[1] < 0 or c[1] > 10 or not self.isEmptySpot(c[0], c[1])):
                return False
        return self.openSpotForEachPiece(piece)

    ##
    # @function     placePiece
    # @purpose      Overwrites the coordinates on the board to place the piece
    # @param        self - the Board instance
    # @param        piece - the piece to place
    def placePiece(self, piece):
        for c in piece.shape:
            self.board[c[0]][c[1]] = piece.color
    
    ##
    # @function     removePiece
    # @purpose      Overwrites the coordinates on the board to remove the placed piece
    # @param        self - the Board instance
    # @param        piece - the piece to remove
    def removePiece(self, piece):
        for c in piece.shape:
            self.board[c[0]][c[1]] = 'X'

    ##
    # @function     openSpotForEachPiece
    # @purpose      Checks that no open spots would be isolated
    # @param        self - the Board instance
    # @param        piece - the piece to check the placement of
    def openSpotForEachPiece(self, piece):
        # Copy the remaining open spots and remove the spots taken up by piece
        other = self.opens.copy()
        traversed = []
        for c in piece.shape:
            other.remove(c)
            traversed.append(c)

        # For each open spot, if the spot is empty, count the connected spots
        # If any spot is not connected to at least 3 other spots, it is considered "isolated"
        # because a kanoodle piece could not possibly fit there 
        for o in other:
            if(self.isEmptySpot(o[0], o[1])):
                t = 1 + self.countConnected(o[0], o[1], traversed.copy())
                if(t < 4):
                    return False
        return True
        
    ##
    # @function     countConnected
    # @purpose      Recursive function to count the number of connected spots to a given spot
    # @param        self - the Board instance
    # @param        r - the row number of the current spot
    # @param        c - the column number of the current spot
    # @param        traversed - the list of spots that are already part of the current connection
    def countConnected(self, r, c, traversed):
        if(r < 0 or r > 4 or c < 0 or c > 10 or [r, c] in traversed or not self.isEmptySpot(r, c)):
            return 0
        else:
            traversed.append([r, c])
            connected = self.countConnected(r + 1, c, traversed) + self.countConnected(r - 1, c, traversed) + self.countConnected(r, c + 1, traversed) + self.countConnected(r, c - 1, traversed)
            return 1 + connected

