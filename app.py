import asyncio

from quart import Quart, websocket

app = Quart(__name__)


async def receive_loop(send_queue):
    while True:
        data = await websocket.receive()
        await send_queue.put(data)


async def send_loop(send_queue):
    while True:
        data = await send_queue.get()
        await websocket.send(data)


@app.websocket("/")
async def ws():
    send_queue = asyncio.Queue()
    receive_task = asyncio.create_task(receive_loop(send_queue))
    send_task = asyncio.create_task(send_loop(send_queue))
    await asyncio.gather(receive_task, send_task)
