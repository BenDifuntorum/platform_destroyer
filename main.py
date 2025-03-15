from project import Model, View, Controller

def init(fps: int, width: int, height: int):
    model = Model(fps, width, height)
    view = View(width, height)
    controller = Controller(model, view)

    return controller


def main():
    FPS = 120
    WIDTH = 900
    HEIGHT = 900
    return init(FPS, WIDTH, HEIGHT)



if __name__ == '__main__':
    main()