import time

class Block:
    def __init__(self, x: float, y: float, f_x: float, f_y: float, m: float): # m is in kg
        self.x = x
        self.y = y
        self.f_x = f_x
        self.f_y = f_y
        self.m = m
        self.v_x = 0
        self.v_y = 0
        print("Initialized")
        
    def apply_force(self, f_x: float, f_y: float):
        self.f_x += f_x
        self.f_y += f_y

    def step(self, dt: int):
        self.x += self.v_x * dt + (self.f_x * dt ** 2) / (2 * self.m)
        self.y += self.v_y * dt + (self.f_y * dt ** 2) / (2 * self.m)

        self.v_x += (self.f_x / self.m) * dt
        self.v_y += (self.f_y / self.m) * dt
    
    def __str__(self):
        return f"Block(mass={self.m}, position=({self.x}, {self.y}), force=({self.f_x}, {self.f_y}))"
        
