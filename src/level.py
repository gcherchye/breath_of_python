"""Level management class"""
from __future__ import absolute_import

import pygame


class Level:
    """Level management class"""

    def __init__(self) -> None:
        # Get the game display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

    def run(self) -> None:
        """Update and draw the game"""
        pass
