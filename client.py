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
    gameplay()

@sio.on('gameplay')
def gameplay():
    print("gameplay called")

    @sio.on('toclient2')
    def toclient2(data) :
        print('client2', data)
        pigCaseX = data[1]
        button_curr = data[2]

        if (button_curr) :
            print('button is pressed') 
            if (pigCaseX == 1) :
                sio.emit('back', [1, -1])
            else :
                sio.emit('back', [0, -1])
            time.sleep(1) 

        time.sleep(1)   
         

# @sio.on('toclient2')
# def toclient2(data) :
#     # print('client2', data)
#     gameplay(data)


sio.connect("http://localhost:8000")