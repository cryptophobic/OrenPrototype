import pygame

from deprecated.map.battlefield import battlefield
from deprecated.ui.application import Application

def main():
    pygame.init()
    app = Application(battlefield)
    app.run()


if __name__ == '__main__':
    main()