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
        earliest_t = None
        collisions_to_resolve = []  # list of tuples describing collisions
        heapq.heapify(collisions_to_resolve) # (priorty, item) = (time, (type, i, j))

        # block-block collisions
        n = len(blocks)
        for i in range(n):
            for j in range(i + 1, n):
                t = blocks[i].calculate_collision_time(blocks[j], remaining)
                if t is not None and t >= 0.0 - EPS:
                    if earliest_t is None or t < earliest_t - EPS:
                        earliest_t = t
                        collisions_to_resolve = [("bb", i, j, t)]
                    elif abs(t - earliest_t) <= EPS:
                        collisions_to_resolve.append(("bb", i, j, t))

        # block-wall collisions
        for i in range(n):
            t = blocks[i].calculate_wall_collision_time(remaining)
            if t is not None and t >= 0.0 - EPS:
                if earliest_t is None or t < earliest_t - EPS:
                    earliest_t = t
                    collisions_to_resolve = [("bw", i, -1, t)]
                elif abs(t - earliest_t) <= EPS:
                    collisions_to_resolve.append(("bw", i, -1, t))

        if earliest_t is None:
            # no collision in remaining time — advance all and finish
            for b in blocks:
                b.step(remaining)
            remaining = 0.0
            break

        # Advance all objects by earliest_t
        if earliest_t > 0.0:
            for b in blocks:
                b.step(earliest_t)
            remaining -= earliest_t

        # Resolve all collisions that occur at earliest_t (use copies of indices to avoid duplication)
        resolved_pairs = set()
        for kind, i, j, t in collisions_to_resolve:
            if kind == "bb":
                key = (min(i, j), max(i, j))
                if key in resolved_pairs:
                    continue
                # Resolve using elastic formula — ensure you use velocities at collision moment
                blocks[i].collide_with_block(blocks[j])  # note: blocks already moved to collision point
                resolved_pairs.add(key)
                total_collisions += 1
                any_collision = True
            else:  # "bw" block-wall
                if i in resolved_pairs:
                    continue
                blocks[i].collide_with_wall()  # already at collision point
                resolved_pairs.add(i)
                total_collisions += 1
                any_collision = True

        # After resolving collisions at this instant, continue to next iteration to handle remaining time
        # Note: collisions resolution changed velocities; we will recompute times relative to new velocities
        # small safeguard: if too many iterations, break
    if iters >= MAX_ITER:
        # fallback: advance remaining time to avoid locking
        for b in blocks:
            b.step(remaining)
        remaining = 0.0

    return total_collisions, any_collision

                    
async def simulate(websocket): # type: ignore
    blocks = [Rectangle(300, 300, 350, 350, 5000, "blue"), Rectangle(400, 300, 450, 350, 5, "red"), 
              Rectangle(0, 0, 600, 10, 10, "black"), # top
             Rectangle(0, 600, 600, 590, float('inf'), "black"), # bottom
             Rectangle(0, 0, 10, 600, float('inf'), "black"), # left    
             Rectangle(600, 0, 590, 600, float('inf'), "black")] # right

    blocks[0].apply_force(500000, 0)
    blocks[1].apply_force(500, 0)

    


    total_collisions = 0
    while True: # Each loop is one frame
        '''
        collisions = 0
        collision_occured = False
        start_time = time.time()
        collisions, collision_occured = await simulate_collisions(blocks, Constants.dt)
        total_collisions += collisions
        # for i, b in enumerate(blocks):
        #     b.step(Constants.dt - collision_times[i]) 
        '''

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
