print("Importing modules...", end="")
import generateMove as gm
import berserk
import pathlib
import random
import time
print("Done")

def strategy(game:gm.Chess):
    return random.choice(gm.getLegalMoves(game))

def startBot():
    with open(str(pathlib.Path(__file__).parent.resolve())+"\\TOKEN.txt", "r") as f: TOKEN = f.read()

    session = berserk.TokenSession(TOKEN)
    client = berserk.Client(session=session)

    areWePlaying = False

    while True:
        for event in client.bots.stream_incoming_events():
            print("EVENT", event)
            if event["type"] == "challenge" and not areWePlaying:
                if event["challenge"]["variant"]["key"] == "standard" and event["challenge"]["rated"] == False: # event["challenge"]["challenger"]["name"] == "Ertugrul2010"
                    gameid = event["challenge"]["id"]
                    client.bots.accept_challenge(gameid)
                    areWePlaying = True
                    break
                else:
                    client.bots.decline_challenge(event["challenge"]["id"])
            
            if event["type"] == "gameStart": 
                gameid = event["game"]["gameId"]
                game = gm.Chess(event["game"]["fen"])
                colourtext = event["game"]["color"]
                colour = 1 if colourtext == "white" else 0
                break
        
        for event in client.bots.stream_game_state(gameid):
            print("GAMESTATE", event)
            if event["type"] == "gameFull" and len(event["state"]["moves"].split()) % 2 == 1 - colour:
                move = strategy(game)
                movetext = gm.moveToString(move)
                print("I PLAYED: ", movetext, game.turn)
                client.bots.make_move(gameid, movetext)
                game.move(move)
                

            if event["type"] == "gameState":
                if len(event["moves"].split(" ")) % 2 == colour: continue
                else:
                    if event["status"] == "started":
                        print("THEY PLAYED: ", event["moves"].split(" ")[-1], game.turn)
                        game.move(gm.stringToMove(game, event["moves"].split(" ")[-1]))
                        move = strategy(game)
                        movetext = gm.moveToString(move)
                        client.bots.make_move(gameid, movetext)
                        game.move(move)
                        print("I MOVED: ", movetext, game.turn)
                    
                    if event["status"] == "mate":
                        client.bots.post_message(gameid, "Good Game! "+("Prepare yourself for another game!" if event["winner"] == colourtext else "You win!"))

            if event["type"] == "gameFinish":
                areWePlaying = False

game = gm.Chess("r1b1k2r/2ppqpbp/1pn2np1/pBP1p3/N3P3/1P3N2/P1QP1PPP/R1B1K2R w KQkq - 2 10")
print(game.castle)

moves = gm.getLegalMoves(game)

print(game.castle)

    # print(gm.numToCoord(move.start), gm.numToCoord(move.end), move.specialMoveType, move.specialMoveDesc, start == end)
    
# print(gm.getMoveCount(game, depth=4))

# for move in moves: print(gm.numToCoord(move.start), gm.numToCoord(move.end), move.specialMoveType, move.specialMoveDesc)

print(gm.writeFEN(game))
s = time.time()
print(gm.getMoveCount(game, depth=4))
print(time.time() - s)

"""
print(game.castle)
game.move(gm.stringToMove(game, "e1g1"))
print(gm.writeFEN(game))

print(game.castle)

moves = gm.getLegalMoves(game)
"""