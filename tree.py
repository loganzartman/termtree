from termpixels.app import App
from termpixels.screen import Color 
import random 
from math import cos, sin, atan2, sqrt, pi
from copy import copy

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_dir(direction, length=1):
        return Vector(cos(direction), sin(direction)) * length

    def angle(self):
        return atan2(self.y, self.x)
    
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def __add__(self, other):
        try:
            return Vector(self.x + other.x , self.y + other.y)
        except AttributeError:
            return Vector(self.x + other, self.y + other)

    def __iadd__(self, other):
        try:
            self.x += other.x
            self.y += other.y
        except AttributeError:
            self.x += other
            self.y += other
        return self
    
    def __mul__(self, other):
        try:
            return Vector(self.x * other.x , self.y * other.y)
        except AttributeError:
            return Vector(self.x * other, self.y * other)

    def __imul__(self, other):
        try:
            self.x *= other.x
            self.y *= other.y
        except AttributeError:
            self.x *= other
            self.y *= other
        return self

def branch_char(direction):
    angle = direction.angle()
    f = (angle / pi) % 1 # opposite directions have same line
    chars = list("─╲│╱")
    return chars[int(f * len(chars))]

class Branch:
    def __init__(self, pos, direction, age, thickness=1):
        self.pos = copy(pos)
        self.direction = copy(direction)
        self.age = age
        self.thickness = thickness
    
    def update(self):
        self.age += 1
        self.thickness -= 0.001
        self.pos += self.direction
        if self.thickness < 0:
            return ()
        if random.random() < self.age / 50:
            offset = random.uniform(-0.4, 0.4)
            left = Branch(self.pos, Vector.from_dir(self.direction.angle() + offset), self.age, self.thickness * 0.5)
            right = Branch(self.pos, Vector.from_dir(self.direction.angle() - offset), self.age, self.thickness * 0.5)
            return (left, right)
        return (self,)
        
    def draw(self, screen):
        col = Color(127,100,0) * (self.thickness ** 0.25) + Color(20,180,0) * (1 - self.thickness ** 0.25)
        screen.print(branch_char(self.direction), round(self.pos.x), round(self.pos.y), fg=col, bg=Color(0,0,0))

class TreeApp(App):
    def __init__(self):
        super().__init__()
        pos0 = Vector(self.screen.w / 2, self.screen.h - 1)
        dir0 = Vector(0, -1)
        self.branches = [Branch(pos0, dir0, 10)]
    
    def on_frame(self):
        next_branches = []
        for branch in self.branches:
            branch.draw(self.screen)
            next_branches += branch.update()
        self.branches = next_branches
        self.screen.update()

TreeApp().start()

