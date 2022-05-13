"""Level management class"""
from __future__ import absolute_import

import pygame

from config import config
from player import Player
from tile import Tile


class Level:
    """Level management class"""

    def __init__(self) -> None:
        # Get the game display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # Config
        self.config = config

        # Vars
        self._create_map()

    def _create_map(self):
        for row_index, row in enumerate(config.world_map):
            for col_index, col in enumerate(row):
                x_pos = col_index * config.tilesize
                y_pos = row_index * config.tilesize

                if col == 'x':
                    Tile((x_pos, y_pos), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    Player((x_pos, y_pos), [self.visible_sprites])

    def run(self) -> None:
        """Update and draw the game"""
        self.visible_sprites.draw(self.display_surface)
