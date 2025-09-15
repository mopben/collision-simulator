from block import Block
from constants import Constants
import asyncio
import time
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

async def physics(websocket): # type: ignore
    blocks = [Block(100, 300, 1000), Block(300, 300, 1)]

    blocks[0].apply_force(100000, 0)
    blocks[1].apply_force(100, 0)

    collisions = 0

    while True: # Each loop is one frame
        start_time = time.time()

        collision_occured = False

        for i, b in enumerate(blocks):
            substeps = min(10000, max(1, int(max(b.v_x, b.v_y)))) # Scale frames simulated based on block speed to prevent clipping
            dt_sub = Constants.dt / substeps

            for _ in range(substeps):
                b.step(dt_sub) 
            
                if b.will_touch_wall(Constants.dt): # May need to deal with problem when block collides with wall and another block simultaneously
                    blocks[i].collide_with_wall()
                    collision_occured = True
                    
                for j in range(i + 1, len(blocks)):
                    if  b.will_collide(blocks[j], Constants.dt):
                        b.collide_with_block(blocks[j])
                        collision_occured = True

        if collision_occured:
            collisions += 1

        state = {
            "blocks": [{"x": b.x, "y": b.y} for b in blocks],
            "collisionOccured": collision_occured,
            "totalCollisions": collisions
            } 
        
        await websocket.send(json.dumps(state)) 
        await asyncio.sleep(Constants.dt - (time.time() - start_time))

async def main():
    async with websockets.serve(physics, "localhost", 8765): # sets up 
        await asyncio.Future()  # placeholder object that never completes

print("Running")
asyncio.run(main())

print("Program finished")