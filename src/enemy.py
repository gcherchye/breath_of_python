"""docstring"""
from __future__ import absolute_import

from typing import List, Tuple

import pygame

from .config import config
from .entity import Entity
from .utils.utils import import_image_from_folder


class Enemy(Entity):
    """docstring"""

    def __init__(
            self,
            monster_name: str,
            pos: Tuple[int, int],
            groups: List[pygame.sprite.Group],
            obstacles: pygame.sprite.Group
        ) -> None:
        super().__init__(groups)

        # General setup
        self.sprite_type = 'enemy'

        # Graphics setup
        self._import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # Movements
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacles_sprite = obstacles

        # Stats
        self.monster_name = monster_name
        monster_info =  config.monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

    def _import_graphics(self, name: str):
        self.animations = {
            'idle': [],
            'move': [],
            'attack': []
        }
        main_path = f'lib/images/monsters/{name}/'

        for animation in self.animations:
            self.animations[animation] = import_image_from_folder(main_path + animation)

    def _get_status(self, player):
        distance, _ = self._get_player_distance_direction(player)

        if distance <= self.attack_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def _get_player_distance_direction(self, player) -> Tuple[float, pygame.math.Vector2]:
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return distance, direction

    def action(self, player):
        if self.status == 'attack':
            print('attack')
        elif self.status == 'move':
            _, self.direction = self._get_player_distance_direction(player)
        else:
            self.direction = pygame.math.Vector2()
    
    def animate(self):
        

    def update(self) -> None:
        self._move(self.speed)

    def enemy_update(self, player):
        self._get_status(player)
        self.action(player)
