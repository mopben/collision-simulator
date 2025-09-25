class Quadrilateral:
    def __init__(self, x: float, y: float, m: float, color: str): # m is in kg
        self.x = x
        self.y = y
        self.m = m
        self.v_x: float = 0.0
        self.v_y: float = 0.0
        self.color = color
        self.is_colliding: bool = False

