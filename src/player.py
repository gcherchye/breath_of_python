"""docstring goes here"""
from __future__ import absolute_import

from typing import List, Tuple

import pygame

from .config import config


class Player(pygame.sprite.Sprite):
    """docstring goes here"""

    def __init__(
            self,
            pos: Tuple[int, int],
            groups: List[pygame.sprite.Group],
            obstacles: pygame.sprite.Group
        ) -> None:
        super().__init__(groups)

        # Image init
        self.image = pygame.image.load('lib/images/dummy/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Player initial attributes
        self.direction = pygame.math.Vector2()
        self.speed = config.player_speed
        self.attacking = False
        self.attack_cooldown = config.player_attack_cooldown

        # Obstacles of the player for which we have to handle collision
        self.obstacles_sprite = obstacles

    def _input(self):
        """Identify the keys pressed by the user and modify the behaviour of the player avatar
        accordingly
        """
        keys = pygame.key.get_pressed()

        # Movements input
        if keys[pygame.K_z]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_q]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # Attack input
        if keys[pygame.K_SPACE]:
            print('attack')

        # Magic input
        if keys[pygame.K_LCTRL]:
            print('magic')

    def _move(self, speed):
        """docstring"""
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self._collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self._collision('vertical')

        self.rect.center = self.hitbox.center

    def _collision(self, direction):
        """docstring"""
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


    def update(self):
        """docstring goes here"""
        self._input()
        self._move(self.speed)
