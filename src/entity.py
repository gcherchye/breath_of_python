"""Docstring"""
from __future__ import absolute_import

from typing import List

from math import sin

import pygame

from src.config import config


class Entity(pygame.sprite.Sprite):
    """Docstring"""

    def __init__(self, groups: List[pygame.sprite.Group]) -> None:
        super().__init__(groups)

        self.frame_index =config.frame_index
        self.animation_speed = config.animation_speed
        self.direction = pygame.math.Vector2()

    def _move(self, speed: int) -> None:
        """Moves the player's hitbox based on the specified speed and direction

        Calculates the movement based on the player's current direction vector and applies the
        movement to the hitbox. It checks for collisions in both horizontal and vertical directions
        and adjusts the hitbox position accordingly.

        Args:
            speed (int): The speed at which the player moves.
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self._collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self._collision('vertical')

        self.rect.center = self.hitbox.center

    def _collision(self, direction: str) -> None:
        """Handles collision detection and response for the player's hitbox

        Checks for collisions in the specified direction (horizontal or vertical) with obstacles
        represented by sprites in the obstacles_sprite group. Adjusts the player's hitbox position
        based on the detected collisions to prevent overlapping with obstacles.

        Args:
            direction (str): The direction in which collision detection is performed ('horizontal'
            or 'vertical').
        """
        if direction == 'horizontal':
            for sprite in self.obstacles_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x >= 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x <= 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacles_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y >= 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y <= 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def _wave_value(self) -> int:
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        return 0
