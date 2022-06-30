"""Weapon class"""
from __future__ import absolute_import

import pygame

from .config import config


class Weapon(pygame.sprite.Sprite):
    """Docstring here"""

    def __init__(self, player, *groups) -> None:
        super().__init__(*groups)

        direction = player.status.split('_')[0]

        # Graphics
        self.image = pygame.Surface((40, 40))

        # Placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + \
                config.weapon_horizon_offset)
        if direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft+ \
                config.weapon_horizon_offset)
        if direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + \
                config.weapon_vertical_offset)
        if direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + \
                config.weapon_vertical_offset)
