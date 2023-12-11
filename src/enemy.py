"""docstring"""
from __future__ import absolute_import

from typing import List, Tuple

import pygame

from .config import config
from .entity import Entity
from .utils.utils import import_image_from_folder


class Enemy(Entity):
    """docstring"""

    def __init__(self, monster_name: str, pos: Tuple, groups: List[pygame.sprite.Group]) -> None:
        super().__init__(groups)

        # General setup
        self.sprite_type = 'enemy'

        # Graphics setup
        self._import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

    def _import_graphics(self, name: str):
        self.animations = {
            'idle': [],
            'move': [],
            'attack': []
        }
        main_path = f'lib/images/monsters/{name}/'

        for animation in self.animations:
            self.animations[animation] = import_image_from_folder(main_path + animation)
