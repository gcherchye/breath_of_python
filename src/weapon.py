"""Contains the Weapon class for game weaponry"""
from __future__ import absolute_import

import pygame

from .config import config


class Weapon(pygame.sprite.Sprite):
    """A class representing a weapon for the game sprites.

    Attributes:
        image (pygame.Surface): The image representing the weapon.
        rect (pygame.Rect): The rectangular area occupied by the weapon on the screen.

    Args:
        player (Player): The player object associated with the weapon.
        *groups: Variable-length argument list of pygame Groups to which the weapon belongs.
    """

    def __init__(self, player, *groups) -> None:
        """Initialize the Weapon object.

        Loads the image for the weapon and sets its initial placement based on the player's direction.

        Args:
            player (Player): The player object associated with the weapon.
            *groups: Variable-length argument list of pygame Groups to which the weapon belongs.
        """
        super().__init__(*groups)

        direction = player.status.split('_')[0]

        # Graphics
        weapon_path = f'lib/images//weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(weapon_path).convert_alpha()

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
