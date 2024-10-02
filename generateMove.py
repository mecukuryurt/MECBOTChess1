class Move:
    def __init__(self, start:int, end:int, piece:tuple, targetedpiece:tuple, special:tuple = (None,None)):
        self.start = start
        self.end = end
        self.piece = piece
        self.specialMoveType = special[0] 
        self.specialMoveDesc = special[1]
        self.targetedPiece = targetedpiece

class Chess:
    infinity = 9999999
    startingBoard = [(0, 4), (0, 2), (0, 3), (0, 5), (0, 6), (0, 3), (0, 2), (0, 4), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 4), (1, 2), (1, 3), (1, 5), (1, 6), (1, 3), (1, 2), (1, 4)]
    def __init__(self, board: list = startingBoard, turn: bool = 1, castling: dict = {"wk": True,"wq": True,"bk": True,"bq": True}, enPassant:int = None, halfmove:int = 0, fullmove:int = 0, moves:list = [], castlingAtTheBeginning: list = {"wk": True,"wq": True,"bk": True,"bq": True}):
        self.board = board
        self.turn = turn
        self.castle = castling
        self.enPassant = enPassant
        self.halfmove = halfmove
        self.fullmove = fullmove
        self.moves = moves
        if self.enPassant != None:
            if self.enPassant >= 16 and self.enPassant <= 23: # Black played a double forward move
                self.moves.append(Move(self.enPassant - 8, self.enPassant + 8, (Pieces.Black, Pieces.Pawn), Pieces.Empty))
            if self.enPassant >= 40 and self.enPassant <= 47: # White played a double forward move
                self.moves.append(Move(self.enPassant + 8, self.enPassant - 8, (Pieces.White, Pieces.Pawn), Pieces.Empty))
        self.castlingAtTheBeginning = castlingAtTheBeginning

    def move(self, move: Move, ignoreerroronnotyourturn = False):
        piece = self.board[move.start]
        if (piece[0] != self.turn) and not ignoreerroronnotyourturn: print(piece[0], self.turn); raise Exception("It is not "+ {0:"black", 1:"white"}[self.turn] + "'s turn!")

        self.moves.append(move)        

        self.enPassant = None

        if move.specialMoveType == None:
            self.board[move.start] = Pieces.Empty
            self.board[move.end]   = piece

            if piece[1] == Pieces.Pawn: # Check if there will be En Passant available after this move
                if abs(move.start - move.end) == 16: # Double forward move
                    if self.board[move.end+1] == (1 - piece[0], Pieces.Pawn) or self.board[move.end-1] == (1 - piece[0], Pieces.Pawn): # En passant available
                        self.enPassant = (move.start - move.end) / 2 + move.end
                    
        else:
            if move.specialMoveType == "enp":
                self.board[move.start] = Pieces.Empty
                self.board[move.end]   = piece
                self.board[move.specialMoveDesc] = Pieces.Empty

            elif move.specialMoveType == "castle":
                self.board[move.start] = Pieces.Empty
                self.board[move.end]   = piece
                self.board[move.specialMoveDesc.start] = Pieces.Empty
                self.board[move.specialMoveDesc.end]   = move.specialMoveDesc.piece
                self.castle[{0:"b", 1:"w"}[piece[0]] + "k"] = False
                self.castle[{0:"b", 1:"w"}[piece[0]] + "q"] = False
            
            elif move.specialMoveType == "pro":
                pawncolour = self.board[move.start][0]
                self.board[move.start] = Pieces.Empty
                self.board[move.end]   = (pawncolour , move.specialMoveDesc)

        """
        Special Move Type  -       Meaning          -   Special Move Description
        enp                      En Passant             Gives the captured piece when played
        castle                    Castling              Gives the rook movement when played
        pro                     Pawn Promotion          Gives the promotion option for pawn (PieceType)
        """

        # Update castling rights
        if piece[1] == Pieces.King:
            self.castle[{0:"b", 1:"w"}[piece[0]] + "k"] = False
            self.castle[{0:"b", 1:"w"}[piece[0]] + "q"] = False

        # Update castling rights
        if piece[1] == Pieces.Rook:
            for kingpos, square in enumerate(self.board):
                if square[0] == piece[0] and piece[1] == Pieces.King: break

            # moving a rook, so move.start is that rook's pos.
            if move.start - kingpos < 0: # The queenside rook.
                self.castle[{0:"b", 1:"w"}[piece[0]] + "q"] = False

            if move.start - kingpos > 0: # The kingside rook.
                self.castle[{0:"b", 1:"w"}[piece[0]] + "k"] = False

        self.turn = 1 - self.turn

    def backupTheGame(self): return Chess(self.board[:], self.turn, dict(self.castle), self.enPassant, self.halfmove, self.fullmove, self.moves[:], self.castlingAtTheBeginning)

def readFEN(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        board = []
        pieces    = fen.split(" ")[0]
        whoseTurn = fen.split(" ")[1]
        castles   = fen.split(" ")[2]
        enpassant = fen.split(" ")[3]
        halfmove  = fen.split(" ")[4]
        fullmove  = fen.split(" ")[5]

        # Prepearing the board
        pieces1 = ""
        for char in pieces: 
            if char != "/": pieces1 += char
        # print(pieces1)
        for piece in pieces1:
            equivalent = {
                "r": Pieces.Rook,
                "n": Pieces.Knight,
                "b": Pieces.Bishop,
                "q": Pieces.Queen,
                "k": Pieces.King,
                "p": Pieces.Pawn
            }
            if not piece.lower() in equivalent.keys():
                piece = int(piece)
                pieceCode = (None, None)
                for i in range(piece): board.append(pieceCode)

            else:
                pieceNum = equivalent[piece.lower()]
                color = Pieces.White if piece.isupper() else Pieces.Black
                pieceCode = (color, pieceNum)
                board.append(pieceCode)

        whoseTurn = Pieces.White if whoseTurn == "w" else Pieces.Black
        # print(board)
        # Parsing the castling situations
        castling = {"wk": True if "K" in castles else False,
                    "wq": True if "Q" in castles else False,
                    "bk": True if "k" in castles else False,
                    "bq": True if "q" in castles else False
        }
        # Finding the number of the square to make En Passant
        enp = None if enpassant == "-" else coordToNum(enpassant)
        
        return Chess(board, whoseTurn, castling, enp, halfmove, fullmove, [], castling)

class Pieces:
    Pawn   = 1
    Knight = 2
    Bishop = 3
    Rook   = 4
    Queen  = 5
    King   = 6

    White = 1
    Black = 0

    ttp = { # Text To Piece
        "r": Rook,
        "n": Knight,
        "b": Bishop,
        "q": Queen,
        "k": King,
        "p": Pawn
    }
    ptt = {} # Piece to Text
    for key in list(ttp.keys()):
        ptt[ttp[key]] = key

    Empty = (None, None)
    AllPieces = (Knight, Bishop, Rook, Queen, King, Pawn)

def writeFEN(game:Chess):
    fen = ""
    # print(Pieces)
    counter = 0
    for i, square in enumerate(game.board):
        if square == Pieces.Empty: 
            counter += 1
        
        else:
            if counter == 0:
                piece = Pieces.ptt[square[1]]
                color = square[0]
                fen += piece.upper() if color == 1 else piece
                # print(piece)
            else:
                fen += str(counter)
                counter = 0
                piece = Pieces.ptt[square[1]]
                color = square[0]
                fen += piece.upper() if color == 1 else piece

        if i % 8 == 7: 
            fen += str(counter) if counter != 0 else ""
            counter = 0
            fen += "/"

    castling = " "
    if game.castle["wk"]: castling += "K"
    if game.castle["wq"]: castling += "Q"
    if game.castle["bk"]: castling += "k"
    if game.castle["bq"]: castling += "q"

    if castling == " ": castling = " -"

    return fen[:-1] + " " + {0:"b", 1:"w"}[game.turn] + castling + " - - -"

################# UTILITIES ##########################
def coordToNum(coord):
    columns = "abcdefgh"
    col = coord[0]
    row = coord[1]
    colnum = columns.index(col)
    row = 8 - int(row)
    num = row * 8 + colnum
    return num

def numToCoord(num):
    columns = "abcdefgh"
    colnum = num % 8
    col = columns[colnum]
    row = 8 - (num // 8)
    return col+str(row)

def moveToString(move: Move):
    text = ""
    if move.specialMoveType in [None, "enp", "castle"]:
        text = numToCoord(move.start) + numToCoord(move.end)
    
    else:
        if move.specialMoveType == "pro":
            text = text + Pieces.ptt[move.specialMoveDesc]
    
    return text

def stringToMove(game: Chess, move: str):
    start = move[0:2]
    end = move[2:4]
    startsq = coordToNum(start)
    endsq = coordToNum(end)
    if len(move) == 5 and game.board[startsq][1] == Pieces.Pawn: # Pawn Promotion
        special = Pieces.ttp[move[-1]]
        return Move(startsq, endsq, game.board[startsq], game.board[endsq], special=("pro", special))
    
    if game.board[startsq][1] == Pieces.King and abs(startsq - endsq) == 2: # Castling 
        colour = {0:"b",1:"w"}[game.board[startsq][0]]
        numColour = game.board[startsq][0]
        if startsq - endsq < 0: rook = numColour*56 + 7; rookgoesto = numColour*56+5 # Castle kingside
        if startsq - endsq > 0: rook = numColour*56;     rookgoesto = numColour*56+3 # Castle queenside   
            
        return Move(startsq, endsq, game.board[startsq], Pieces.Empty, special=("castle", Move(rook, rookgoesto, (game.board[startsq][0], Pieces.Rook), Pieces.Empty)))
    
    if game.board[endsq] == Pieces.Empty and game.board[startsq][1] == Pieces.Pawn: # En Passant
        return Move(startsq, endsq, game.board[startsq], Pieces.Empty, ("enp", int(endsq + (game.board[startsq][0]-0.5)*16)))
    
    else:
        return Move(startsq, endsq, game.board[startsq], game.board[endsq], (None, None))

################## PIECE MOVEMENTS ######################
def isNearToBorder(num):
    row = num // 8
    col = num % 8
    if   (row == 7) and not (col in [0, 7]): return +8, +7, +9 ## Bottom edge
    elif (row == 0) and not (col in [0, 7]): return -8, -7, -9 ## Top edge
    elif (col == 7) and not (row in [0, 7]): return +1, -7, +9 ## Right edge
    elif (col == 0) and not (row in [0, 7]): return -1, -9, +7 ## Left edge

    elif (row == 0) and (col == 0): return -9, -8, -7, -1, +7 ## Top-left corner
    elif (row == 0) and (col == 7): return -7, -9, -8, +1, +9 ## Top-right corner
    elif (row == 7) and (col == 0): return +7, -9, -1, +8, +9 ## Bottom-left corner
    elif (row == 7) and (col == 7): return +9, +7, +8, -7, +1 ## Bottom-right corner
    # return Where cannot the piece go

    else: return [False]

def normalMovement(game:Chess, piece:int, straight:bool = True, diagonal:bool = True, limit = None, ignoreerroronthereisnopiece:bool = False, piececolour = 2):
    if not straight and not diagonal: return []
    if piececolour == 2: piececolour = game.board[piece][0]

    board = game.board
    if board[piece] == Pieces.Empty and not ignoreerroronthereisnopiece: raise TypeError("An empty square given, expected a piece")
    num = piece
    if diagonal and not straight: directions = [-9, -7, 7, 9]
    if straight and not diagonal: directions = [-8, -1, 1, 8]
    if straight and diagonal:     directions = [-9, -8, -7, -1, 1, 7, 8, 9]
    # print(board[piece])
    probs = [] # Probabilities
    for i in directions:
        if i in isNearToBorder(piece): continue
        num = piece
        distance = 0
        while True:
            num += i
            # print(isNearToBorder(num), i, numToCoord(num))
            distance += 1
            piecethere = board[num]
            if piecethere == Pieces.Empty: # there is no piece
                probs.append(Move(piece, num, board[piece], piecethere))

            elif piecethere[0] == 1 - piececolour and piecethere[1] != Pieces.King: # Enemy piece
                probs.append(Move(piece, num, board[piece], piecethere))
                break

            elif piecethere[0] == piececolour: # Friendly piece
                break
            else: pass

            if distance == limit: break
            else: pass

            if isNearToBorder(num) == [False]: continue
            elif i in isNearToBorder(num): break

    return probs

def getQueenMovement  (game:Chess, piece:int): moves = normalMovement(game, piece, straight=True,  diagonal=True,  ignoreerroronthereisnopiece=True);  return moves
def getBishopMovement (game:Chess, piece:int): moves = normalMovement(game, piece, straight=False, diagonal=True , ignoreerroronthereisnopiece=True);  return moves
def getRookMovement   (game:Chess, piece:int): moves = normalMovement(game, piece, straight=True,  diagonal=False, ignoreerroronthereisnopiece=True); return moves
def getKingMovement   (game:Chess, piece:int): 
    moves = normalMovement(game, piece, straight=True,  diagonal=True, limit=1, ignoreerroronthereisnopiece=True)
    # Check for the castling
    castling = game.castle
    for icouldntfindname in castling.keys():
        colour = {0:"b",1:"w"}[game.board[piece][0]]
        numColour = game.board[piece][0]
        if colour in icouldntfindname and castling[icouldntfindname] == True:
            if icouldntfindname[1] == "k":
                if not (game.board[piece+1] == game.board[piece+2] == Pieces.Empty): continue
                if isTheSquareThreatened(game, piece, 1-numColour) == True or  isTheSquareThreatened(game, piece+1, 1-numColour) == True: continue
                target = numColour*56 + 6; rook = numColour*56 + 7; rookgoesto = numColour*56+5

            if icouldntfindname[1] == "q": 
                if not (game.board[piece-1] == game.board[piece-2] == game.board[piece-3] == Pieces.Empty): continue
                if isTheSquareThreatened(game, piece-1, 1-game.board[piece][0]) == True or isTheSquareThreatened(game, piece, 1-game.board[piece][0]) == True: continue
                target = numColour*56 + 2; rook = numColour*56    ; rookgoesto = numColour*56+3
               
            moves.append(Move(piece, target, game.board[piece], Pieces.Empty, special=("castle", Move(rook, rookgoesto, (game.board[piece][0], Pieces.Rook), Pieces.Empty))))

    return moves

def getPawnMovement   (game:Chess, piece:int): 
    moves = []
    board = game.board
    pawn = board[piece]
    startingsquaresforpawns = {
        Pieces.White: (48, 55),
        Pieces.Black: (8, 15)
    }
    promotionranges = {
        Pieces.White: (0, 7),
        Pieces.Black: (56, 63)
    }

    direction = -8 if pawn[0] == Pieces.White else +8
    captures = []
    if 1+direction not in isNearToBorder(piece): captures.append(piece+1+direction) # Diagonal movement generates issues when the piece is at the border
    if direction-1 not in isNearToBorder(piece): captures.append(piece-1+direction)

    if piece >= startingsquaresforpawns[pawn[0]][0] and piece <= startingsquaresforpawns[pawn[0]][1]: # Double pawn move
        if board[piece + (direction*2)] == Pieces.Empty and board[piece + direction] == Pieces.Empty: moves.append(Move(piece, piece+(direction*2), pawn, board[piece + (direction*2)]))
    
                                # is enp targeting the black pieces? == is the piece white?
    if game.enPassant != None and (game.enPassant < 24) == (pawn[0] == Pieces.White) and game.enPassant in captures: # There is en Passant!
        try: 
            if captures[0] == game.enPassant: moves.append(Move(piece, captures[0], pawn, board[captures[0]], special = ("enp", int(captures[0] + (pawn[0]-0.5)*16))))
        except: pass
        try: 
            if captures[1] == game.enPassant: moves.append(Move(piece, captures[1], pawn, board[captures[0]], special = ("enp", int(captures[1] + (pawn[0]-0.5)*16))))
        except: pass

    if board[piece+direction] == Pieces.Empty: # Simple forward move
        if piece+direction >= promotionranges[pawn[0]][0] and piece+direction <= promotionranges[pawn[0]][1]:
            for p in Pieces.AllPieces[:-2]:
                moves.append(Move(piece, piece+direction, pawn, Pieces.Empty, special=("pro", p)))
    
        else: moves.append(Move(piece, piece+direction, pawn, Pieces.Empty))
    
    for capture in captures: # Detect diagonal captures
        target = board[capture]
        if target[0] == 1 - pawn[0] and abs((capture%8) - (piece%8)) == 1:
            if capture >= promotionranges[pawn[0]][0] and capture <= promotionranges[pawn[0]][1]:
                for p in Pieces.AllPieces[:-2]:
                    moves.append(Move(piece, capture, pawn, board[capture], special=("pro", p)))
            else:
                moves.append(Move(piece, capture, pawn, board[capture]))

    return moves

def getKnightMovement (game:Chess, piece:int): 
    def setDirectionsForKnight(num):
        directions = []
        row = num // 8
        col = num % 8
        if row > 1 and col > 0: directions.append(-17)
        if row > 1 and col < 7: directions.append(-15)
        if row > 0 and col > 1: directions.append(-10)
        if row > 0 and col < 6: directions.append(-6)
        if row < 7 and col > 1: directions.append(+6)
        if row < 7 and col < 6: directions.append(+10)
        if row < 6 and col > 0: directions.append(+15)
        if row < 6 and col < 7: directions.append(+17)
        return directions
    
    board = game.board
    knight = board[piece]
    moves = []
    for d in setDirectionsForKnight(piece):
        target = piece + d
        if board[target][0] == 1 - knight[0] or board[target] == Pieces.Empty:
            moves.append(Move(piece, target, knight, board[target]))
    return moves

def getPsuedoLegalMoves(game:Chess):
    allMoves = []
    for i, piece in enumerate(game.board):
        if piece[0] == game.turn:
            if piece == Pieces.Empty: continue
            elif piece[1] == Pieces.Queen:  allMoves += getQueenMovement(game, i)
            elif piece[1] == Pieces.Bishop: allMoves += getBishopMovement(game, i)
            elif piece[1] == Pieces.Rook:   allMoves += getRookMovement(game, i)
            elif piece[1] == Pieces.Knight: allMoves += getKnightMovement(game, i)
            elif piece[1] == Pieces.Pawn:   allMoves += getPawnMovement(game, i)
            elif piece[1] == Pieces.King:   allMoves += getKingMovement(game, i)
            else: pass
    
        
    return allMoves

def getLegalMoves(game:Chess):
    allMoves = getPsuedoLegalMoves(game)
    legalMoves = []

    for move in allMoves:
        altgame = game.backupTheGame()  # Alternative game
        turn = game.turn
        # print(moveToString(move), game.castle, altgame.castle, id(game.castle) == id(altgame.castle), type(altgame.castle))
        altgame.move(move, ignoreerroronnotyourturn=True)
        for i, piece in enumerate(altgame.board):
            if piece[0] == turn and piece[1] == Pieces.King:
                # Check if the kings are at neigbouring squares.
                doKingsSeeEachOther = False
                disallowedDirections = isNearToBorder(i)
                for drc in [-9,-8,-7,-1,1,7,8,9]:
                    if drc not in disallowedDirections:
                        try:
                            if altgame.board[i + drc][1] == Pieces.King:
                                print(numToCoord(i), numToCoord(i+drc))
                                doKingsSeeEachOther = True
                                break
                        except: pass
                if doKingsSeeEachOther: print(doKingsSeeEachOther)
                if doKingsSeeEachOther: break

                isKingInCheck = isTheSquareThreatened(altgame, i, 1-turn)
                if not isKingInCheck:
                    legalMoves.append(move)
                    break
        # print(moveToString(move), game.castle, altgame.castle)
        del altgame
        # game.undoMove(move, ignoreerroronnotyourturn=True)

    return legalMoves

def isTheSquareThreatened(game:Chess, square:int, whoIsEnemy):
    if whoIsEnemy not in [0,1]: raise TypeError("Expected 0 or 1")
    board = game.board
    colour = board[square][0]
    game.board[square] = 1 - whoIsEnemy, board[square][1] # If an empty square is given, Knight Movement function generates issue about the piece colour (None in this situation). 

    for threat in getKnightMovement(game, square): # Knight Threats
        if board[threat.end] == Pieces.Empty: continue
        if board[threat.end][1] == Pieces.Knight: game.board[square] = colour, board[square][1]; return True

    game.board[square] = colour, board[square][1]

    for threat in normalMovement(game, square, False, True, ignoreerroronthereisnopiece=True, piececolour=1 - whoIsEnemy): # Diagonal Threats
        if board[threat.end] == Pieces.Empty: continue
        if board[threat.end][1] in [Pieces.Queen, Pieces.Bishop]:
            return True

    for threat in normalMovement(game, square, True, False, ignoreerroronthereisnopiece=True, piececolour=1 - whoIsEnemy): # Straight Threats
        if board[threat.end] == Pieces.Empty: continue
        if board[threat.end][1] in [Pieces.Queen, Pieces.Rook]: return True

    # Pawn Threats
    direction = -8 if whoIsEnemy == Pieces.Black else +8
    captures = []
    if 1+direction not in isNearToBorder(square): captures.append(square+1+direction)
    if direction-1 not in isNearToBorder(square): captures.append(square-1+direction)

    for threat in captures:
        # print(writeFEN(game))
        if board[threat][0] == whoIsEnemy and abs((threat%8) - (square%8)) == 1 and board[threat][1] in (Pieces.Queen, Pieces.Bishop, Pieces.Pawn): return True
        else: continue

    return False

def getMoveCount(game:Chess = readFEN(), depth:int = 1):
    if depth == 1: return len(getLegalMoves(game))
    else:
        moveCount = 0
        for move in getLegalMoves(game):
            altgame = game.backupTheGame()  # Alternative game

            altgame.move(move, True)
            moveCountFromRecrFunc = getMoveCount(altgame, depth-1)
            moveCount += moveCountFromRecrFunc

            del altgame
            # game.undoMove(move, True)
    return moveCount

def isKingInCheck(game:Chess, whichKing:int = Pieces.White): # The output = (isKingInCheck, isCheckMate)
    kings = [(i, piece[0]) for i, piece in enumerate(game.board) if piece[1] == Pieces.King]
    if game.board[kings[0][0]][0] == Pieces.White: kings[0], kings[1] = kings[1], kings[0]

    gameTurnBackup = game.turn
    if whichKing == Pieces.White:
        # Calculate legal moves of white
        game.turn = Pieces.White
        whiteMobility = getMoveCount(game, 1)

        isWkingInCheck = isTheSquareThreatened(game, kings[1][0], 0)
        game.turn = gameTurnBackup
        if whiteMobility == 0 and isWkingInCheck: return True, True
        if whiteMobility != 0 and isWkingInCheck: return True, False
        if not isWkingInCheck: return False, None # idk if it's checkmate or not

    if whichKing == Pieces.Black:
        # Calculate legal moves of black
        game.turn = Pieces.Black
        blackMobility = getMoveCount(game, 1)

        isBkingInCheck = isTheSquareThreatened(game, kings[0][0], 1)
        game.turn = gameTurnBackup
        if blackMobility == 0 and isBkingInCheck: return True, True
        if blackMobility != 0 and isBkingInCheck: return True, False
        if not isBkingInCheck: return False, None # idk if it's checkmate or not

def isStalemate(game):
    kings = [(i, piece[0]) for i, piece in enumerate(game.board) if piece[1] == Pieces.King]
    if game.board[kings[0][0]][0] == Pieces.White: kings[0], kings[1] = kings[1], kings[0]

    gameTurnBackup = game.turn

    game.turn = Pieces.White
    whiteMobility = getMoveCount(game, 1)

    isWkingInCheck = isTheSquareThreatened(game, kings[1][0], 0)
    game.turn = gameTurnBackup
    if whiteMobility == 0 and not isWkingInCheck and game.turn == Pieces.White: return True

    # Calculate legal moves of black
    game.turn = Pieces.Black
    blackMobility = getMoveCount(game, 1)

    isBkingInCheck = isTheSquareThreatened(game, kings[0][0], 1)
    game.turn = gameTurnBackup
    if blackMobility == 0 and not isBkingInCheck and game.turn == Pieces.Black: return True

def evaluate(game:Chess):
    board = game.board

    evaluation = 0

    kings = [(i, piece[0]) for i, piece in enumerate(board) if piece[1] == Pieces.King]
    if board[kings[0][0]][0] == Pieces.White: kings[0], kings[1] = kings[1], kings[0]
    # after this swap operation, list should look like this: [(Black King Square, Colour Black), (White King Square, Colour White)]

    gameTurnBackup = game.turn
    # Calculate legal moves of white
    game.turn = Pieces.White
    whiteMobility = getMoveCount(game, 1)

    isWkingInCheck = isTheSquareThreatened(game, kings[1][0], 0)
    if whiteMobility == 0 and isWkingInCheck: return -Chess.infinity
    if whiteMobility == 0 and not isWkingInCheck: return 0 # stalemate btw

    # Calculate legal moves of black
    game.turn = Pieces.Black
    blackMobility = getMoveCount(game, 1)

    isBkingInCheck = isTheSquareThreatened(game, kings[0][0], 1)
    if blackMobility == 0 and isBkingInCheck: return Chess.infinity
    if blackMobility == 0 and not isBkingInCheck: return 0 # stalemate

    game.turn = gameTurnBackup

    evaluation += (whiteMobility - blackMobility) / 10

    pieceWeight = {
        "wk" : 200,
        "wq" : 9,
        "wr" : 5,
        "wb" : 3,
        "wn" : 3,
        "wp" : 1,
        "bk" : -200,
        "bq" : -9,
        "br" : -5,
        "bb" : -3,
        "bn" : -3,
        "bp" : -1
    }

    pawnsOnFile = {1:[i for i in range(9)], 0: [i for i in range(9)]}
    pawns = []
    pawnData = {
        "wi" : 0,
        "wb" : 0,
        "wd" : 0,
        "bi" : 0,
        "bb" : 0,
        "bd" : 0
    }

    for i, piece in enumerate(game.board):
        if piece == Pieces.Empty: continue
        colour = {0: "b", 1:"w"}[piece[0]]
        pieceType = Pieces.ptt[piece[1]]
        evaluation += pieceWeight[colour + pieceType]
        evaluation = round(evaluation * 10) /10

        if piece[1] == Pieces.Pawn: # Check for pawns. Add the values to check for doubled, isolated and blocked pawns later
            pawns.append(i)
            pawnsOnFile[piece[0]][i % 8] += 1

    for pawn in pawns:
        if pawnsOnFile[board[pawn][0]][(pawn % 8) - 1] == pawnsOnFile[board[pawn][0]][(pawn % 8) + 1] == 0: pawnData[{0: "b", 1:"w"}[board[pawn][0]] + "i"] += 1 # Isolated Pawn
        if pawnsOnFile[board[pawn][0]][(pawn % 8)] >= 2: pawnData[{0: "b", 1:"w"}[board[pawn][0]] + "d"] += 1 # Doubled Pawn
        if len(getPawnMovement(game, pawn)) == 0: pawnData[{0: "b", 1:"w"}[board[pawn][0]] + "b"] += 1 # Blocked Pawn

    isolated = pawnData["wi"]-pawnData["bi"]
    doubled = pawnData["wd"]-pawnData["bd"]
    blocked = pawnData["wb"]-pawnData["bb"]
    evaluation -= (isolated + doubled + blocked) / 2

    return evaluation

def getBestEvaluation(game:Chess = readFEN(), depth = 1):
    def alphaBeta(game:Chess = readFEN(), alpha = -Chess.infinity, beta = Chess.infinity, depth = 1, maximizingPlayer = bool(game.turn)):
        if depth == 0 or abs(evaluate(game)) == Chess.infinity or isStalemate(game): return evaluate(game), 0
        else:
            moves = getLegalMoves(game)

            movesWithCheck = []
            for x in moves:
                altGame = game.backupTheGame()
                altGame.move(x)
                if isKingInCheck(altGame, altGame.turn)[0]:
                    movesWithCheck.append(x)
                    moves.remove(x)
                del altGame
            moves = movesWithCheck + moves
            evaluations = {}

            if maximizingPlayer: # Maximizing player # game.turn == Pieces.White
                maxEval = -Chess.infinity

                for move in moves:
                    altGame = game.backupTheGame()
                    altGame.move(move)
                    result = alphaBeta(altGame, alpha, beta, depth-1, False)

                    maxEval = max(maxEval, result[0])
                    alpha = max(alpha, result[0])
                    evaluation = result[0]
                    evaluations[move] = evaluation

                    if beta <= alpha: break
                    del altGame
                
                bestMoves = []
                for possibleMove in evaluations.keys():
                    if evaluations[possibleMove] == maxEval:
                        bestMoves.append(possibleMove)

                return maxEval, bestMoves[0]

            else: # Minimizing player # if game.turn == Pieces.Black
                minEval = +Chess.infinity

                for move in moves:
                    altGame = game.backupTheGame()
                    altGame.move(move)
                    result = alphaBeta(altGame, alpha, beta, depth-1, True)

                    minEval = min(minEval, result[0])
                    beta = min(beta, result[0])
                    evaluation = result[0]
                    evaluations[move] = evaluation

                    if beta <= alpha: break
                    del altGame

                bestMoves = []
                for possibleMove in evaluations.keys():
                    if evaluations[possibleMove] == minEval:
                        bestMoves.append(possibleMove)
                
                return minEval, bestMoves[0]

            print("how did you get here")
            raise Exception("How did you get here! Give the maximizing player!")

    def minimax(game:Chess = readFEN(), depth=1):
        currentEval = evaluate(game)
        if depth == 0 or abs(currentEval) == Chess.infinity: return currentEval, 0 # eval, bestMove
        else: 
            evaluations = {}
            moves = getLegalMoves(game)
            for move in moves:
                altGame = game.backupTheGame() # Alternative Game
                altGame.move(move)
                result = minimax(altGame, depth-1)
                evaluation = result[0] * game.turn
                evaluations[move] = evaluation
                del altGame
            
            bestEval = 0
            bestMoves = []
            for possibleMove in evaluations.keys():
                if evaluations[possibleMove] > bestEval:
                    bestMoves.clear()
                    bestEval = evaluations[possibleMove]
                    bestMoves.append(possibleMove)
                if evaluations[possibleMove] == bestEval:
                    bestMoves.append(possibleMove)

            return bestEval, bestMoves[0]  # bestEval, bestMove
        
    # return alphaBeta(game, -Chess.infinity, Chess.infinity, depth)
    return alphaBeta(game, -Chess.infinity, Chess.infinity, depth, bool(game.turn))