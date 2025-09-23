from constants import Constants

class Square:
    def __init__(self, x: float, y: float, m: float, color: str): # m is in kg
        self.x = x
        self.y = y
        self.m = m
        self.size = Constants.SIZE
        self.color = color
        self.v_x: float = 0.0
        self.v_y: float = 0.0
        self.is_colliding: bool = False
        print("Block Initialized")
        
    def apply_force(self, f_x: float, f_y: float): # Applies an impulse equivalent to Force *  1s / mass
        self.v_x = f_x / self.m
        self.v_y = f_y / self.m

    def step(self, dt):
        self.x += self.v_x * dt
        self.y += self.v_y * dt


    def calculate_collision_time(self, other, dt: float) -> float | None:
        # Relative motion
        vx_rel = self.v_x - other.v_x
        vy_rel = self.v_y - other.v_y

        # Start and end positions (intervals)
        x1_min, x1_max = self.x, self.x + self.size
        x2_min, x2_max = other.x, other.x + other.size
        y1_min, y1_max = self.y, self.y + self.size
        y2_min, y2_max = other.y, other.y + other.size

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


        t_x_enter, t_x_exit = axis_times(x1_min, x1_max, x2_min, x2_max, vx_rel)
        t_y_enter, t_y_exit = axis_times(y1_min, y1_max, y2_min, y2_max, vy_rel)

        # Overall collision interval = intersection of x and y intervals
        t_enter = max(t_x_enter, t_y_enter)
        t_exit = min(t_x_exit, t_y_exit)

        # Valid collision if intervals overlap and within [0, dt]
        if t_enter <= t_exit and 0 <= t_enter <= dt:
            return t_enter
        return None
    
    def calculate_wall_collision_time(self, dt) -> float | None:
        x1_min, x1_max = self.x, self.x + self.size
        y1_min, y1_max = self.y, self.y + self.size
        
        def axis_times(smaller, greater, v_rel):
            if v_rel == 0: # Moving the same speed
                return float("inf") 
            
            return (greater - smaller) / v_rel
        
        if 0 <= axis_times(Constants.CANVAS_X, x1_min, self.v_x) <= dt:
            return axis_times(Constants.CANVAS_X, x1_min, self.v_x)
        if 0 <= axis_times(x1_max, Constants.CANVAS_X + Constants.CANVAS_WIDTH, self.v_x) <= dt:
            return axis_times(x1_max, Constants.CANVAS_X + Constants.CANVAS_WIDTH, self.v_x)
        if 0 <= axis_times(Constants.CANVAS_Y, y1_min, self.v_y) <= dt: 
            return axis_times(Constants.CANVAS_Y, y1_min, self.v_y)
        if 0 <= axis_times(y1_max, Constants.CANVAS_Y + Constants.CANVAS_HEIGHT, self.v_y) <= dt:  
            return axis_times(y1_max, Constants.CANVAS_Y + Constants.CANVAS_HEIGHT, self.v_y)
        return None
    
    def collide_with_block(self, other):

        self.v_x = (self.v_x * (self.m - other.m) + 2 * other.m * other.v_x) / (self.m + other.m)
        self.v_y = (self.v_y * (self.m - other.m) + 2 * other.m * other.v_y) / (self.m + other.m)
        other.v_x = (other.v_x * (other.m - self.m) + 2 * self.m * self.v_x) / (self.m + other.m)
        other.v_y = (other.v_y * (other.m - self.m) + 2 * self.m * self.v_y) / (self.m + other.m)      

    def collide_with_wall(self):
        self.v_x = -self.v_x
        self.v_y = -self.v_y

    def __str__(self):
        return f"Block(mass={self.m}, position=({self.x}, {self.y}), force=({self.f_x}, {self.f_y}))"