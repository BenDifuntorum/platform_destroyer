from typing import Protocol
from dataclasses import dataclass
from enum import Enum, auto


class UpdateHandler(Protocol):
    def update(self):
        ...


class DrawHandler(Protocol):
    def draw(self):
        ...


class Rectangle:
    def __init__(self, x: float, y: float, width: float, height: float):
        # print('lol')
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width


class Platform(Rectangle):
    def __init__(self, type: int, x: float, y: float):
        super().__init__(x, y, 100, 5)
        self.type = type

@dataclass
class Circle:
    x: float
    y: float
    radius: float

    @property
    def top(self):
        return self.y - self.radius

    @property
    def bottom(self):
        return self.y + self.radius

    @property
    def left(self):
        return self.x - self.radius

    @property
    def right(self):
        return self.x + self.radius

@dataclass
class Ball(Circle):
    v_x: float
    v_y: float
    a_x: float
    a_y: float




class Surface(Enum):
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()



class PipePairInfo(Protocol):
    @property
    def top_pipe(self) -> Rectangle:
        ...

    @property
    def bottom_pipe(self) -> Rectangle:
        ...


class BirdInfo(Protocol):
    @property
    def x(self) -> float:
        ...

    @property
    def y(self) -> float:
        ...

    @property
    def radius(self) -> float:
        ...





