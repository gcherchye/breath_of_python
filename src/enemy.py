"""docstring"""
from __future__ import absolute_import
from typing import List

import pygame

from src.config import config
from src.entity import Entity


class Enemy(Entity):
    """docstring"""

    def __init__(self, monster_name: str, pos, groups: List[pygame.sprite.Group]) -> None:
        super().__init__(groups)

        # General setup
        self.sprite_type = 'enemy'

        # Graphics setup
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft = pos)
