import pygame

from map.battlefield import battlefield
from ui.application import Application

def main():
    pygame.init()
    app = Application(battlefield)
    app.run()


if __name__ == '__main__':
    main()