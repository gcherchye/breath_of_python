"""docstring goes here"""
from __future__ import absolute_import

from typing import List, Tuple

import pygame

from .config import config


class Tile(pygame.sprite.Sprite):
    """A class representing tiles in the game."""

    def __init__(
            self,
            pos: Tuple[int, int],
            groups: List[pygame.sprite.Group],
            sprite_type,
            surface: pygame.Surface=pygame.Surface((config.tilesize, config.tilesize))
        ) -> None:
        """Initializes the Tile class

        Args:
            pos (Tuple[int, int]): The position of the tile.
            groups (List[pygame.sprite.Group]): List of sprite groups to add the tile to.
            sprite_type: Type of sprite.
            surface (pygame.Surface): Surface to represent the tile (default is a blank surface).
        """
        super().__init__(groups)

        self.sprite_type = sprite_type

        self.image = surface

        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - config.tilesize))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
