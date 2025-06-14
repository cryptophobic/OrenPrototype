import pygame

from deprecated.ui.actors.cursor.actions import Actions
from deprecated.ui.actors.controls import Controls as BaseControls, Action


class Controls(BaseControls):
    def __init__(self, actions: Actions):
        super().__init__(actions)
        self.data[pygame.K_LEFT] = Action(actions.move_left, 150)
        self.data[pygame.K_RIGHT] = Action(actions.move_right, 150)
        self.data[pygame.K_UP] = Action(actions.move_up, 150)
        self.data[pygame.K_DOWN] = Action(actions.move_down, 150)
