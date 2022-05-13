"""docstring goes here"""
from __future__ import absolute_import

from typing import List, Tuple

import pygame


class Player(pygame.sprite.Sprite):
    """docstring goes here"""

    def __init__(self, pos: Tuple[int, int], groups: List[pygame.sprite.Group]) -> None:
        super().__init__(groups)

        self.image = pygame.image.load('lib/images/dummy/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5

    def _input(self):
        """docstring goes here"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_z]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_q]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def _move(self, speed):
        """docstring"""
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction * speed

    def update(self):
        """docstring goes here"""
        self._input()
        self._move(self.speed)
