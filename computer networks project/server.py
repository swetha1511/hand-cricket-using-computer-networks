import socket
from _thread import *
import pickle
from game import Game

server = "localhost"
port = 5555


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Using IPV4 IP adress
                                                        # Using TCP Sockets
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()   # keeps id of the clients that gets connected
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount #Is for total players and another info cpount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":  # reset is for send back the client because of no data
                        game.resetWent()
                    elif data == "score":                   # done-bat = 1 for player completed batting
                        print("no pblem")                   # done-bat = 0 for player not done batting
                        print("game.done_bat[0] = ", game.done_bat[0], "and game.done_bat[1] =", game.done_bat[1])
                        if game.done_bat[0] == 1 and game.bothWent():
                            print("2nd player as batsman")
                            game.score[1] = game.batsman(1, 0, game.score[1])
                            print("completed1")
                        elif game.bothWent():
                            print("1nd player as batsman")
                            game.score[0] = game.batsman(0, 1, game.score[0])
                            print("completed2")
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2    # game id is to many clients to play but in 2's
    print(idCount)
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)  # this is for new game if 3 players join
        print("Creating a new game...")
    else:
        print("2nd connected")
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))  # gameId is for which client is playing which game of the dictionary