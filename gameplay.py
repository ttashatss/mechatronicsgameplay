import time

timeLim = 5
pigNum = 3
birdNum = 5

timeStart = int(time.time())

# username = username sent from ui
kills = 0
birdLive = birdNum

def win() :
    print("You Win")
    # send data to database
    exit()

def lose() :
    print("You Lose")
    # send data to database
    exit()

while(True):
    pigCase = 1 # pigCase = toffyfile.pigCase
    buttonPressed = 1 # buttonPressed = angiefile.buttonPressed

    timeElapsed = int(time.time())-timeStart
    print(timeLim - int(timeElapsed))

    if ((timeLim - timeElapsed == 0) or birdLive == 0) : lose()
    if (kills >= pigNum) : win()

    if (buttonPressed) :
        birdLive -= 1
        if (pigCase == 1) :
            kills += 1
        

