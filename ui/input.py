import pygame


class InputHandler:
    def __init__(self):
        self.enter_pressed = False
        self.direction = (0, 0)

    def poll(self):
        self.enter_pressed = False
        self.direction = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.enter_pressed = True
                elif event.key == pygame.K_UP:
                    self.direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    self.direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    self.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.direction = (1, 0)

    def get_direction(self):
        return self.direction
