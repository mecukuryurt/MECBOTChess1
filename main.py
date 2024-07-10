import generateMove as gm

mygame = gm.Chess("8/q4PK1/1k6/8/8/8/8/8 w - - 0 1")
moves = gm.getLegalMoves(mygame)
print(len(moves))
textmoves = []

for move in moves:
    textmoves.append(gm.numToCoord(move.start) + gm.numToCoord(move.end))
    print(textmoves)