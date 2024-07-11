import generateMove as gm

mygame = gm.Chess("5kr1/8/8/5pP1/8/6K1/8/8 w - f6 0 1")
moves = gm.getLegalMoves(mygame)
print(len(moves))
textmoves = []

for move in moves:
    textmoves.append(gm.numToCoord(move.start) + gm.numToCoord(move.end))
print(textmoves)