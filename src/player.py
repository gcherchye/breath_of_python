"""docstring goes here"""
from __future__ import absolute_import

from typing import List, Tuple

import pygame

from src.config import config
from src.utils.utils import import_image_from_folder


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

        # Loading animation
        self.import_player_assets(config.player_img_path)
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = config.player_animation_speed

        # Player initial attributes
        self.direction = pygame.math.Vector2()
        self.speed = config.player_speed
        self.attacking = False
        self.attack_cooldown = config.player_attack_cooldown
        self.attack_time = None

        # Obstacles of the player for which we have to handle collision
        self.obstacles_sprite = obstacles

    def import_player_assets(self, path:str):
        """Docstring"""
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'up_idle': [],
            'down_idle': [],
            'left_idle': [],
            'right_idle': [],
            'up_attack': [],
            'down_attack': [],
            'left_attack': [],
            'right_attack': [],
        }

        for animation in self.animations:
            self.animations[animation] = import_image_from_folder(path + animation)

    def _input(self):
        """Identify the keys pressed by the user and modify the behaviour of the player avatar
        accordingly
        """
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # Movements input
            if keys[pygame.K_z]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_q]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # Attack input
            if keys[pygame.K_SPACE] or keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

    def _get_status(self):
        """docstring"""
        # Idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not any(old in self.status for old in ['_idle', '_attack']):
                self.status += '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0

            if not '_attack' in self.status:
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
        else:
            if '_attack' in self.status:
                self.status = self.status.replace('_attack', '')


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

    def _cooldowns(self):
        """docstring"""
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def _animate(self):
        """docstring"""
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)




    def update(self):
        """docstring goes here"""
        self._input()
        self._cooldowns()
        self._get_status()
        self._animate()
        self._move(self.speed)
