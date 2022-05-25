"""docstring goes here"""
from __future__ import absolute_import

from typing import List, Tuple

import pygame

from .config import config


class Tile(pygame.sprite.Sprite):
    """docstring goes here"""

    def __init__(
            self,
            pos: Tuple[int, int],
            groups: List[pygame.sprite.Group],
            sprite_type,
            surface: pygame.Surface=pygame.Surface((config.tilesize, config.tilesize))
        ) -> None:
        super().__init__(groups)

        self.image = surface

        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - config.tilesize))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
