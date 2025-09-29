from rectangle import Rectangle
from constants import Constants
import asyncio
import time
import websockets
import json
import time
import heapq

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

'''
Alters velocity based on collision & teleports blocks to collision point
Doesn't work if one block may collide with multiple blocks or block + wall in one frame (only in very high speeds)
Returns float[] of collision times or none if no collision within frame & collisions
'''
import math
from typing import List, Tuple

EPS = 1e-9
MAX_ITER = 50  # safety cap to avoid pathological infinite loops

async def simulate_collisions(blocks: List[Rectangle], dt: float):
    """
    Processes collisions for the whole frame of duration dt.
    Returns (collision_counts, any_collision_happened_bool).
    This advances blocks in-place through the entire dt.
    """

    remaining = dt
    total_collisions = 0
    any_collision = False
    iters = 0

    while remaining > EPS and iters < MAX_ITER:
        iters += 1

        # Find earliest collision in (0, remaining]
        collisions_to_resolve : List[tuple[int, int, int]] = []  # list of tuples describing collisions
        heapq.heapify(collisions_to_resolve) # (priorty, item) = (time, (type, i, j))

        # block-block collisions
        n = len(blocks)
        for i in range(n):
            for j in range(i + 1, n):
                t = blocks[i].calculate_collision_time(blocks[j], remaining)
                if t is not None and t >= 0.0 - EPS:
                    heapq.heappush(collisions_to_resolve, (t, i, j))


        if len(collisions_to_resolve) == 0:
            # No collisions in remaining time
            for b in blocks:
                b.step(remaining)
            remaining = 0.0
            break

        # Advance all objects by earliest_t
        if collisions_to_resolve[0][0] > 0.0: # collisions_to_resolve[0][0] is the earliest collision time
            print("Collisions to resolve:", collisions_to_resolve)
            for b in blocks:
                b.step(collisions_to_resolve[0][0])
            remaining -= collisions_to_resolve[0][0]
        
        for i in range(2):
            print(blocks[i].color, blocks[i])

        last_t = collisions_to_resolve[0][0]
        for collisions in collisions_to_resolve: 
            t, i, j, = collisions
            if t != last_t:
                break
            blocks[i].collide_with_block(blocks[j])
            total_collisions += 1
            any_collision = True
            last_t = t
        print("After: ")
        for i in range(2):
            print(blocks[i].color, blocks[i])

        print()
            



    if iters >= MAX_ITER: # To prevent an infinite loop
        for b in blocks:
            b.step(remaining)
        remaining = 0.0

    return total_collisions, any_collision

                    
async def simulate(websocket): # type: ignore
    blocks = [Rectangle(300, 300, 350, 350, 5000, "blue"), Rectangle(400, 300, 450, 350, 5, "red"), 
              Rectangle(0, 0, 600, 10, float('inf'), "black"), # top
             Rectangle(0, 600, 600, 590, float('inf'), "black"), # bottom
             Rectangle(0, 0, 10, 600, float('inf'), "black"), # left    
             Rectangle(600, 0, 590, 600, float('inf'), "black")] # right

    blocks[0].apply_force(500000, 0)
    blocks[1].apply_force(500, 0)

    total_collisions = 0
    while True: # Each loop is one frame
        collisions = 0
        collision_occured = False
        start_time = time.time()
        collisions, collision_occured = await simulate_collisions(blocks, Constants.dt)
        total_collisions += collisions
        # for i, b in enumerate(blocks):
        #     b.step(Constants.dt - collision_times[i]) 

        collision_occured = False
        state = {
            "blocks": [{"x": b.x, "x2": b.x2, "y": b.y, "y2": b.y2, "color": b.color, "v_x": b.v_x, "isColliding": b.is_colliding} for b in blocks],
            "collisionOccured": collision_occured,
            "totalCollisions": total_collisions   
            } 
        
        await websocket.send(json.dumps(state)) 
        await asyncio.sleep(Constants.dt - (time.time() - start_time))

async def main():
    async with websockets.serve(simulate, "localhost", 8765): 
        await asyncio.Future()  
