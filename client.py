import socketio
import time

# def send() :
#     send data to database

# standard Python
sio = socketio.Client()

@sio.event
def connect():
    print("gameplay connected!")
    sio.emit('client2', 'connected')

@sio.on('gameplay')
def gameplay(username):
    timeLim = 5
    pigNum = 3
    birdNum = 5

    timeStart = int(time.time())  # type: ignore

    global kills
    kills = 0

    global birdLive
    birdLive = birdNum

    while(True):
        sio.emit('back', [kills, birdLive])
        pigCaseX = 0 # pigCaseX = toffyfile.pigCaseX
        buttonPressed = 1 # buttonPressed = angiefile.buttonPressed

        # timeElapsed = int(time.time())-timeStart
        # print(timeLim - int(timeElapsed))

        # (timeLim - timeElapsed == 0) or 
        if (birdLive == 0) :
            print('You Lose')
            sio.emit('lose','You Lose')
            # send()
            exit()

        if (kills >= pigNum) :
            print('You Win')
            sio.emit('win','You Win')
            # send()
            exit()

        if (buttonPressed) :
            birdLive -= 1
            if (pigCaseX == 1) :
                kills += 1

@sio.on('toclient2')
def toclient2(data) :
    print('client2', data)
    gameplay(data)


sio.connect("http://localhost:8000")