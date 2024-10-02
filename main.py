print("Importing modules...", end="")
import generateMove as gm
import berserk
import pathlib
import random
import time
print("Done")

def strategy(game:gm.Chess):
    print("STRATEGY RUNNING")
    print(game.turn)
    result = gm.getBestEvaluation(game, 2)
    print(result[0], gm.moveToString(result[1]))
    return result[1]

def startBot():
    with open(str(pathlib.Path(__file__).parent.resolve())+"\\TOKEN.txt", "r") as f: TOKEN = f.read()

    session = berserk.TokenSession(TOKEN)
    client = berserk.Client(session=session)

    areWePlaying = False

    while True:
        for event in client.bots.stream_incoming_events():
            print("EVENT", event)
            if event["type"] == "challenge" and not areWePlaying:
                if event["challenge"]["variant"]["key"] in "standardfromPosition" and event["challenge"]["rated"] == False: # event["challenge"]["challenger"]["name"] == "Ertugrul2010"
                    gameid = event["challenge"]["id"]
                    client.bots.accept_challenge(gameid)
                    areWePlaying = True
                    break
                else:
                    client.bots.decline_challenge(event["challenge"]["id"])
            
            if event["type"] == "gameStart": 
                gameid = event["game"]["gameId"]
                game = gm.readFEN(event["game"]["fen"])
                colourtext = event["game"]["color"]
                colour = 1 if colourtext == "white" else 0
                break
        
        for event in client.bots.stream_game_state(gameid):
            print("GAMESTATE", event)
            try: game
            except:
                game = gm.readFEN(event["initialFen"])
                for move in event["state"]["moves"].split():
                    game.move(move)
            try: colour = 1 if event["white"]["id"] == "mecbotchess1" else 0
            except: pass
            print("colour, turn", colour, game.turn)
            if event["type"] == "gameFull" and game.turn == colour: # len(event["state"]["moves"].split())
                print("CALCULATE", gm.writeFEN(game))
                move = strategy(game)
                movetext = gm.moveToString(move)
                print("I PLAYED: ", movetext, game.turn)
                client.bots.make_move(gameid, movetext)
                game.move(move)
                

            if event["type"] == "gameState":
                if game.turn == colour: continue # len(event["moves"].split(" ")) % 2
                else:
                    if event["status"] == "started":
                        print("THEY PLAYED: ", event["moves"].split(" ")[-1], game.turn)
                        if game.turn != colour:
                            game.move(gm.stringToMove(game, event["moves"].split(" ")[-1]))
                            print("CALCULATE", gm.writeFEN(game))
                            move = strategy(game)
                            movetext = gm.moveToString(move)
                            client.bots.make_move(gameid, movetext)
                            game.move(move)
                            print("I MOVED: ", movetext, game.turn)
                    
                    if event["status"] in "materesign":
                        client.bots.post_message(gameid, "Good Game! "+("Prepare yourself for another game!" if event["winner"] == colourtext else "You win!"))

            if event["type"] == "gameFinish":
                areWePlaying = False

# game = gm.readFEN("r4rk1/p7/1q2b2p/3p1pp1/2P2p2/8/PPQN1nPP/R1B2RK1 b - - 0 1")
# game = gm.readFEN("q2r3k/6pp/8/3Q2N1/8/8/5PPP/6K1 w - - 0 1")
# game = gm.readFEN("q2r3k/6pp/7N/3Q4/8/8/5PPP/6K1 w - - 4 3")
# game = gm.readFEN("8/8/7p/6N1/6k1/8/5PPP/6K1 b - - 1 8")

"""
moves = gm.getLegalMoves(game)
print(bool(game.turn))
print(gm.evaluate(game))

for move in moves:
    if move.end == gm.coordToNum("g5"):
        print(gm.moveToString(move))


print(game.turn)
t1 = time.time()
result = gm.getBestEvaluation(game, 1)
t2 = time.time()
print(game.turn, result)
print(result[0], gm.moveToString(result[1]), t2- t1)
"""

startBot()