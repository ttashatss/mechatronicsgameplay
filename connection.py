import socketio
import websockets
import asyncio
import time

def win() :
    print("You Win")
    # send data to database
    exit()

def lose() :
    print("You Lose")
    # send data to database
    exit()


PORT = 7890
print("Server listening on port " + str(PORT))

async def echo(websocket, path):
    print("A client just connected")
    try: 
        async for message in websocket:
            print("Recieved Message from client " + message)
            timeLim = 5
            pigNum = 3
            birdNum = 5

            timeStart = int(time.time())  # type: ignore

            kills = 0
            birdLive = birdNum

            while(True):
                await websocket.send(str([kills,birdLive]))
                pigCaseX = 0 # pigCaseX = toffyfile.pigCaseX
                buttonPressed = 1 # buttonPressed = angiefile.buttonPressed

                timeElapsed = int(time.time())-timeStart
                print(timeLim - int(timeElapsed))

                if ((timeLim - timeElapsed == 0) or birdLive == 0) : lose()
                if (kills >= pigNum) : win()

                if (buttonPressed) :
                    birdLive -= 1
                    if (pigCaseX == 1 and pigCaseY == 1) :
                        kills += 1
                        
    except websockets.exceptions.ConnectionClosed as e:  # type: ignore
        print("Client disconnected")

start_server = websockets.serve(echo, "localhost", 7890)  # type: ignore

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()