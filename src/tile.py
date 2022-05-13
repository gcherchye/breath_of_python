"""docstring goes here"""
from __future__ import absolute_import

import pygame


class Tile(pygame.sprite.Sprite):
    """docstring goes here"""

    def __init__(self, pos: int, groups: pygame.sprite.Group) -> None:
        super().__init__(groups)

        self.image = pygame.image.load('../lib/images/dummy/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
