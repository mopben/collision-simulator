from constants import Constants

class Block:
    def __init__(self, x: float, y: float, m: float): # m is in kg
        self.x = x
        self.y = y
        self.m = m
        self.v_x = 0.0
        self.v_y = 0.0
        self.size = Constants.SIZE
        print("Block Initialized")
        
    def apply_force(self, f_x: float, f_y: float): # Applies an impulse equivalent to Force *  1s / mass
        self.v_x = f_x / self.m
        self.v_y = f_y / self.m

    def step(self, dt):
        self.x += self.v_x * dt
        self.y += self.v_y * dt
    
    def will_collide(self, other, dt) -> bool:    
        # Current positions
        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y

        # Next positions
        nx1, ny1 = x1 + self.v_x * dt, y1 + self.v_y * dt
        nx2, ny2 = x2 + other.v_x * dt, y2 + other.v_y * dt

        # Check overlap along x
        if nx1 + self.size < nx2 or nx1 > nx2 + other.size:
            return False

        # Check overlap along y
        if ny1 + self.size < ny2 or ny1 > ny2 + other.size:
            return False

        return True
    
    def will_touch_wall(self, dt) -> bool:
        next_x_min = self.x - self.size + self.v_x * dt
        next_x_max = self.x + self.size + self.v_x * dt
        next_y_min = self.y - self.size + self.v_y * dt
        next_y_max = self.y + self.size + self.v_y * dt

        return (next_x_min <= Constants.CANVAS_X 
            or next_x_max >= Constants.CANVAS_X + Constants.CANVAS_WIDTH
            or next_y_min <= Constants.CANVAS_Y
            or next_y_max >= Constants.CANVAS_Y + Constants.CANVAS_HEIGHT)

    
    def collide_with_block(self, other):
        # Simplified elastic collision equations
        new_v_x1 = (self.v_x * (self.m - other.m) + 2 * other.m * other.v_x) / (self.m + other.m)
        new_v_y1 = (self.v_y * (self.m - other.m) + 2 * other.m * other.v_y) / (self.m + other.m)
        new_v_x2 = (other.v_x * (other.m - self.m) + 2 * self.m * self.v_x) / (self.m + other.m)
        new_v_y2 = (other.v_y * (other.m - self.m) + 2 * self.m * self.v_y) / (self.m + other.m)
        
        self.v_x = new_v_x1
        self.v_y = new_v_y1
        other.v_x = new_v_x2
        other.v_y = new_v_y2

    def collide_with_wall(self):
        self.v_x = -self.v_x
        self.v_y = -self.v_y

    def __str__(self):
        return f"Block(mass={self.m}, position=({self.x}, {self.y}), force=({self.f_x}, {self.f_y}))"