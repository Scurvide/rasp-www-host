import asyncio
import websockets

async def request_command():
    async with websockets.connect(
            'ws://192.168.1.107:8000' ) as websocket:
        name = 'Mog'
        await websocket.send(name)
        
        command = await websocket.recv()
        print(f'< {command}')

asyncio.get_event_loop().run_until_complete(request_command)
