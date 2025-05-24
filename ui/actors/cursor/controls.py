import pygame

from ui.actors.cursor.cursor import Cursor
from ui.actors.controls import Controls as BaseControls, Action


class Controls(BaseControls):
    def __init__(self, actor: Cursor):
        super().__init__(actor)
        self.data[pygame.K_LEFT] = Action(actor.actions.move_left, 150)
        self.data[pygame.K_RIGHT] = Action(actor.actions.move_right, 150)
        self.data[pygame.K_UP] = Action(actor.actions.move_up, 150)
        self.data[pygame.K_DOWN] = Action(actor.actions.move_down, 150)
