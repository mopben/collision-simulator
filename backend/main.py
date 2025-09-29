import asyncio
import physics_sim
from rectangle import Rectangle

def initialize_canvas():
    blocks = [Rectangle(300, 300, 900, 900, 5000, "blue"), Rectangle(400, 300, 1000, 900, 5, "red")]
    walls = [Rectangle(0, 0, 600, 10, float('inf'), "black"), # top
             Rectangle(0, 600, 600, 590, float('inf'), "black"), # bottom
             Rectangle(0, 0, 10, 600, float('inf'), "black"), # left
             Rectangle(600, 0, 600, 590, float('inf'), "black")] # right
    blocks[0].apply_force(500000, 0)
    blocks[1].apply_force(500, 0)


asyncio.run(physics_sim.main())
print("Running")
