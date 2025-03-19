import pyxel
from physics import PhysicsModel, Ball
from project_types import Platform

import random
import math
from enum import Enum, auto


class GameState(Enum):
    NOT_STARTED = auto()
    ONGOING = auto()
    ENDED = auto()

class Operation(Enum):
    ADD = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EXPONENTIATE = auto()
    LOG_E = auto()
    ROOT = auto()


class Model(PhysicsModel):
    def __init__(self, fps: int, width: int, height: int):
        super().__init__(fps, width, height)
        self._init_ball()
        self._platforms: dict[int, Platform] = {}
        self._points = 0
        self._state = GameState.NOT_STARTED

        pyxel.init(width, height, fps=fps, title='BONUCHE', quit_key=pyxel.KEY_Q)

    def _init_ball(self):
        self._ball.x = 100
        self._ball.y = 100
        self._ball.v_x = 0
        self._ball.v_y = 0
        self._ball.a_x = 0
        self._ball.a_y = self._gravity

    @property
    def fps(self):
        return self._fps

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height

    @property
    def points(self):
        return self._points
    
    @property
    def game_state(self):
        return self._state
    
    @property
    def platform_list(self):
        return self._platforms

    @property
    def bad_platform_list(self):
        return [(key, platform) for key, platform in self._platforms.items() if platform.type == pyxel.COLOR_RED]

    def spawn_platform(self):
        x, y = self._generate_xy()
        self._platforms[self._id_gen()] = Platform(
            type=random.choice((
                pyxel.COLOR_LIME, 
                pyxel.COLOR_RED, 
                pyxel.COLOR_DARK_BLUE, 
                pyxel.COLOR_YELLOW,
                pyxel.COLOR_ORANGE,
                pyxel.COLOR_PURPLE,)), 
            x=x, 
            y=y)

    def _generate_xy(self) -> tuple[float, float]:
        # current_platforms: list[tuple[float, float]] = [(self._platforms[k].x, self._platforms[k].y) for k in self._platforms]
        # while True:
        #     x1 = random.uniform(0, self._width-50)
        #     y1 = random.uniform(0, self._height-5)
        #     if all(x1 < x2 + 50 and x1 + 50 > x2 and y1 < y2 + 5 and y1 + 5 > y2 for (x2, y2) in current_platforms): return (x1, y1)

        #     break
        x1 = random.uniform(0, self._width-50)
        y1 = random.uniform(0, self._height-5)
        return (x1, y1)
 
    def _id_gen(self):
        while (i := random.randint(0, 32768)) in self._platforms.keys():
            continue

        return i

    def pop_platform(self):
        list_to_remove = self.bad_platform_list
        to_remove = list_to_remove.pop(random.randint(0, len(list_to_remove)-1))

        del self._platforms[to_remove[0]]


    def edit_points(self, o: Operation, p: float):
        match o:
            case Operation.ADD:
                self._points += p

            case Operation.MULTIPLY:
                self._points *= p

            case Operation.DIVIDE:
                self._points //= p

            case Operation.EXPONENTIATE:
                self._points **= p

            case Operation.LOG_E:
                self._points = math.floor(math.log(self._points, p))

            case Operation.ROOT:
                self._points = math.isqrt(self._points)


    #RANDOM AHH FUNCTIONS FOR PLATFORMS
 
    def _high_bounce_y(self):
        self._bounce_y(bounce_factor=-1.4)

    def collision(self):
        for key, platform in self._platforms.items():
            if ((self._ball.bottom >= platform.top >= self._ball.bottom - self._ball.v_y) or (self._ball.top >= platform.bottom >= self._ball.top + self._ball.v_y)) and platform.left < self._ball.x < platform.right:
                col_p = self._platforms.pop(key)
                return col_p

    def flip_y_acceleration(self):
        self._ball.a_y *= -1

    def transpose_acceleration(self):
        self._ball.a_y, self._ball.a_x = self._ball.a_x, self._ball.a_y
        
    def transpose_velocity(self):
        self._ball.v_y, self._ball.v_x = self._ball.v_x, self._ball.v_y

    def stop_ball(self):
        self._ball.v_y = 0
        self._ball.v_x = 0

    def deccelerate_ball(self):
        self._ball.a_y = 0
        self._ball.a_x = 0

    def accelerate_to_gravity(self):
        super().accelerate_to_gravity()

    def platform_bounce(self, platform: Platform):
        match platform.type:
            case pyxel.COLOR_LIME:
                self._high_bounce_y()
                self.accelerate_to_gravity()
                self.edit_points(Operation.ADD, 4)

            case pyxel.COLOR_DARK_BLUE:
                self._bounce_y()
                self.edit_points(Operation.ADD, 2)
            
            case pyxel.COLOR_YELLOW:
                self.flip_y_acceleration()
                self.stop_ball()
                self.edit_points(Operation.ADD, -2)

            case pyxel.COLOR_ORANGE:
                self.transpose_acceleration()
                self.transpose_velocity()
                self.edit_points(Operation.MULTIPLY, -1)

            case pyxel.COLOR_PURPLE:
                self.deccelerate_ball()
                self.edit_points(Operation.EXPONENTIATE, 1.2)

            case pyxel.COLOR_RED:
                self.end_game()

            case _:
                pass



    def start_game(self):
        self._init_ball()
        self._platforms = {}
        self._points = 0
        self._state = GameState.ONGOING

    def end_game(self):
        self._state = GameState.ENDED


class View:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
    
    def sample_bounce(self, circle: Ball, platform_list: dict[int, Platform]):
        pyxel.cls(col=pyxel.COLOR_BLACK)
        pyxel.circ(x=circle.x, y=circle.y, r=circle.radius, col=pyxel.COLOR_WHITE)

        for platform in platform_list.values():
            pyxel.rect(x=platform.x, y=platform.y, w=platform.width, h=platform.height, col=platform.type)

    def print_points(self, points: float):
        pyxel.text(x=self._width/10, y=self._height/10, s=f'Points: {points}', col=pyxel.COLOR_WHITE)


    def unstarted_screen(self, key: int):
        pyxel.cls(col=pyxel.COLOR_BLACK)
        pyxel.text(x=self._width/2, y=self._height/2, s=f'PRESS {key} TO START', col=pyxel.COLOR_WHITE)

    def ended_screen(self, points: float, key_restart: int, key_quit: int):
        pyxel.cls(col=pyxel.COLOR_RED)
        pyxel.text(x=self._width/2, y=self._height/2, s=f'YOU GOT {points} POINTS!', col=pyxel.COLOR_WHITE)
        pyxel.text(x=self._width/2, y=self._height/2 + 5, s=f'PRESS {key_restart} TO RESTART', col=pyxel.COLOR_WHITE)
        pyxel.text(x=self._width/2, y=self._height/2, s=f'PRESS {key_quit} TO QUIT', col=pyxel.COLOR_WHITE)



class Controller:
    def __init__(self, model: Model, view: View):
        self._view = view
        self._model = model


        pyxel.run(self.update, self.draw)

    def update(self):
        if self._model.ball_dist_from_next_surface < 0:
            self._model.bounce()
        
        second_per_plat: float = 4

        chance = random.uniform(0, second_per_plat * self._model.fps)
        if math.floor(chance) == 0: self._model.spawn_platform()

        if len(self._model.bad_platform_list) > 12:
            if math.floor(chance) == second_per_plat: 
                self._model.pop_platform()

        self._model.height_update()
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            self._model.jump()

        if pyxel.btnp(pyxel.KEY_Q):
            self._model.end_game()

        if pyxel.btn(pyxel.KEY_D):
            self._model.push_right()

        if pyxel.btn(pyxel.KEY_A):
            self._model.push_left()


        if self._model.ball.v_y != 0:
            if col_p := self._model.collision():
                self._model.platform_bounce(col_p)

        if self._model.game_state == GameState.NOT_STARTED:
            if pyxel.btn(pyxel.KEY_G):
                self._model.start_game()

        if self._model.game_state == GameState.ENDED:
            if pyxel.btn(pyxel.KEY_R):
                self._model.start_game()

            elif pyxel.btn(pyxel.KEY_Q):
                quit()
        # print(self._model.ball.a_y, self._model.ball.a_x)




    def draw(self):
        match self._model.game_state:
            case GameState.ONGOING:
                self._view.sample_bounce(self._model.ball, self._model.platform_list)
                self._view.print_points(self._model.points)
            
            case GameState.NOT_STARTED:
                self._view.unstarted_screen(pyxel.KEY_G)

            case GameState.ENDED:
                self._view.ended_screen(self._model.points, pyxel.KEY_R, pyxel.KEY_Q)

