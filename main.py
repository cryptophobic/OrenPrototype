import pygame

from engine.grid import Grid
from ui.interaction import Interaction

def main():
    pygame.init()
    grid = Grid(25, 20)
    interaction = Interaction(grid)

    clock = pygame.time.Clock()
    while True:
        interaction.update()
        clock.tick(10)

if __name__ == '__main__':
    main()