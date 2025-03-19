from physics_types import Ball, Surface

class PhysicsModel:
    def __init__(self, fps: int, width: int, height: int):
        self._gravity = 4200 / fps**2
        self._ball = Ball(
            x=0, 
            y=0, 
            v_x=0, 
            v_y=0, 
            a_x=0, 
            a_y=0,
            radius=5, 
            )
        self._width = width
        self._height = height
        self._fps = fps

    @property
    def ball(self):
        return self._ball

    @property
    def closest_surface(self) -> Surface:
        dist = self.ball_dist_from_next_surface
        
        if dist == self._ball.left-0:
            return Surface.LEFT

        elif dist == self._width-self._ball.right:
            return Surface.RIGHT

        elif dist == self._ball.top-0:
            return Surface.TOP

        else:
            assert dist == self._height-self._ball.bottom
            return Surface.BOTTOM

    @property
    def ball_dist_from_next_surface(self):
        return min(
            self._ball.left-0, 
            self._width-self._ball.right, 
            self._ball.top-0, 
            self._height-self._ball.bottom)

    @property
    def speed_change_x(self):
        return self._speed_function()
    


    def _adjust(self):
        match self.closest_surface:
            case Surface.LEFT:
                self._ball.x = self._ball.radius

            case Surface.RIGHT:
                self._ball.x = self._width - self._ball.radius

            case Surface.TOP:
                self._ball.y = self._ball.radius

            case Surface.BOTTOM:
                self._ball.y = self._height - self._ball.radius

    def height_update(self):
        self._accelerate_x()
        self._accelerate_y()
        self._move_x()
        self._move_y()

    def _move_x(self):
        self._ball.x += self._ball.v_x

    def _move_y(self):
        self._ball.y += self._ball.v_y

    def _bounce_x(self, bounce_factor: float = -1):
        self._ball.v_x *= bounce_factor

    def _bounce_y(self, bounce_factor: float = -0.987):
        self._ball.v_y *= bounce_factor
        self._ball.v_x *= 0.993

    def _accelerate_x(self):
        self._ball.v_x += self._ball.a_x
    
    def _accelerate_y(self):
        self._ball.v_y += self._ball.a_y

    def _speed_function(self):
        speed = self._ball.v_x
        if speed >= 500:
            return 1  
        return 15 * (1 / 15 + speed)

    def accelerate_to_gravity(self):
        self._ball.a_y = self._gravity

    def bounce(self):
        if self.closest_surface in (Surface.TOP, Surface.BOTTOM):
            self._bounce_y()
        else:
            assert self.closest_surface in (Surface.LEFT, Surface.RIGHT)
            self._bounce_x()
        if self.ball_dist_from_next_surface < 0.1:
            self._adjust()


    def jump(self):
        self._ball.v_y = -1500/self._fps

    def push_right(self):
        if self._ball.v_x >= 540/self._fps:
            self._ball.v_x += 0
        else:
            self._ball.v_x += 35/self._fps

    def push_left(self):
        if self._ball.v_x <= -540/self._fps:
            self._ball.v_x += 0
        else:
            self._ball.v_x -= 35/self._fps