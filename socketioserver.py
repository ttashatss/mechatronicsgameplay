import socketio
from aiohttp import web

HOST = '127.0.0.1'
PORT = 8000

# create a Socket.IO server
sio = socketio.AsyncServer(async_mode='aiohttp', logger=False, engineio_logger=False, cors_allowed_origins='*')

app = web.Application()
sio.attach(app)

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('client2')
def client2(sid, data):
    print('client2', data)

@sio.on('client3')
def client3(sid, data):
    print('client3', data)

@sio.on('username')
async def username(sid, data):
    print('username', data)
    await sio.emit('toclient3', data)
    
@sio.on('back')
async def back(sid, data):
    print(data)
    await sio.emit('score', data)

# @sio.on('win')
# async def win(sid, data):
#     await sio.emit('win', data)
#     print(data)

# @sio.on('lose')
# async def lose(sid, data):
#     await sio.emit('lose', data)
#     print(data)

@sio.on('mechanics')
async def mechanics(sid, data):
    # print('mechanicss', data)
    await sio.emit('toclient2', data)




if __name__ == '__main__':
    web.run_app(app, host=HOST, port=PORT)


