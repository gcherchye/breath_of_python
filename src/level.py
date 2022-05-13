"""Level management class"""
from __future__ import absolute_import

import pygame


class Level:
    """Level management class"""

    def __init__(self) -> None:
        # Sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

    def run(self) -> None:
        """Update and draw the game"""
        pass
