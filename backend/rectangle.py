from constants import Constants

class Rectangle():
    def __init__(self, x: float, y: float, x2: float, y2: float, m: float, color: str): # m is in kg
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.m = m
        self.color = color
        self.v_x: float = 0.0
        self.v_y: float = 0.0
        self.is_colliding: bool = False
        self.size = Constants.SIZE
        self.color = color

        print("Block Initialized")
        
    def apply_force(self, f_x: float, f_y: float): # Applies an impulse equivalent to Force *  1s / mass
        self.v_x = f_x / self.m
        self.v_y = f_y / self.m

    def step(self, dt):
        self.x += self.v_x * dt
        self.y += self.v_y * dt
        self.x2 += self.v_x * dt
        self.y2 += self.v_y * dt

    def calculate_collision_time(self, other, dt: float) -> float | None:
        # Relative motion
        vx_rel = self.v_x - other.v_x
        vy_rel = self.v_y - other.v_y

        def axis_times(min1, max1, min2, max2, v_rel):
            if v_rel == 0: # Moving the same speed
                if max1 < min2 or max2 < min1: 
                    return float("inf"), float("-inf")  # never collide
                else:
                    return float("-inf"), float("inf")  # always overlapping
            t_enter = (min2 - max1) / v_rel # time they start touching
            t_exit  = (max2 - min1) / v_rel 
            if t_enter > t_exit:
                t_enter, t_exit = t_exit, t_enter
            return t_enter, t_exit


        t_x_enter, t_x_exit = axis_times(self.x, self.x2, other.x, other.x2, vx_rel)
        t_y_enter, t_y_exit = axis_times(self.y, self.y2, other.y, other.y2, vy_rel)

        # Overall collision interval = intersection of x and y intervals
        t_enter = max(t_x_enter, t_y_enter)
        t_exit = min(t_x_exit, t_y_exit)

        # Valid collision if intervals overlap and within [0, dt]
        if t_enter <= t_exit and 0 <= t_enter <= dt:
            return t_enter
        return None

    def collide_with_block(self, other):
        if other.m == float('inf'): # collision including a wall
            self.v_x = - self.v_x
            self.v_y = - self.v_y
        else:        
            u1x, u2x = self.v_x, other.v_x # temp versions 
            u1y, u2y = self.v_y, other.v_y

            self.v_x = (u1x * (self.m - other.m) + 2 * other.m * u2x) / (self.m + other.m)
            other.v_x = (u2x * (other.m - self.m) + 2 * self.m * u1x) / (self.m + other.m)

            self.v_y = (u1y * (self.m - other.m) + 2 * other.m * u2y) / (self.m + other.m)
            other.v_y = (u2y * (other.m - self.m) + 2 * self.m * u1y) / (self.m + other.m)


    def __str__(self):
        return f"Block(mass={self.m}, position=({self.x}, {self.y}), velocity=({self.v_x}, {self.v_y}))"
    
    def __repr__(self):
        return self.__str__()
