import time
from tokenize import Number
import socketio

server_io = socketio.AsyncServer(async_mode='asgi')

app = socketio.ASGIApp(server_io, static_files={
    '/': '../angrymechatronics/pages/gameplay/index.tsx',
    '/socket.tsx': '../angrymechatronics/pages/gameplay/socket.tsx'
    })

timeLim = 5
pigNum = 3
birdNum = 5

timeStart = int(time.time())  # type: ignore

username = "hello"
kills = 0
birdLive = birdNum

@server_io.event
def connect(sid, socket):    
    print(sid, 'connected')

@server_io.event
def disconnect(sid):
    print(sid, 'disconnected')

def sendData(sid, int kills, int birdLive):
    server_io.emit([kills, birdLive], to = sid)

def win() :
    print("You Win")
    # send data to database
    exit()

def lose() :
    print("You Lose")
    # send data to database
    exit()



while(True):
    pigCaseX = 1 # pigCaseX = toffyfile.pigCaseX
    pigCaseY = 1 # pigCaseY = toffyfile.pigCaseY
    buttonPressed = 1 # buttonPressed = angiefile.buttonPressed

    timeElapsed = int(time.time())-timeStart
    print(timeLim - int(timeElapsed))

    if ((timeLim - timeElapsed == 0) or birdLive == 0) : lose()
    if (kills >= pigNum) : win()

    if (buttonPressed) :
        birdLive -= 1
        if (pigCaseX == 1 and pigCaseY == 1) :
            kills += 1
        