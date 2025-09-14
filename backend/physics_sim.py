from block import Block
import asyncio
import websockets
import json
import time

start_time = time.time()

'''
1. Learn asynchronous/await & websocket 
2. Implement that connecting python and js
3. Connected js and html 
4. Test if 1 basic block works!
5. Implement wall ricochet
6. Implement second block
7. Implement block collision (MVP)
'''
# Minimum viable product: Only left & right (1d), able to enter in x, y, mass, forces of each box


async def physics(websocket):
    fps = 30
    blocks = [Block(500, 500, -300, 300, 2)]

    while True:
        for b in blocks:
            b.step(1 / 30) # Simulates each block separately

        state = {"blocks": [{"x": b.x, "y": b.y} for b in blocks]} # creates a dict of the position of each blocks (which themselves are dicts)
        await websocket.send(json.dumps(state)) # only pauses THIS COROUTINE (physics function) until the data is sent; everything else continues
        # json.dumps converts something into a json string
        await asyncio.sleep(1 / fps) # Happens after data is sent, only pauses THIS COROUTINE for 1/fps seconds
        # async functions can only run together with other async functions, if ran together with a sync function then the sync function will block everything

async def main():
    async with websockets.serve(physics, "localhost", 8765): # sets up 
        await asyncio.Future()  # placeholder object that never completes

print("Running")
asyncio.run(main())

print("Program finished")