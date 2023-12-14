"""docstring"""
from __future__ import absolute_import

from typing import List, Tuple

import pygame

from .config import config
from .entity import Entity
from .player import Player
from .utils.utils import import_image_from_folder


class Enemy(Entity):
    """Class representing an enemy entity"""

    def __init__(
            self,
            monster_name: str,
            pos: Tuple[int, int],
            groups: List[pygame.sprite.Group],
            obstacles: pygame.sprite.Group
        ) -> None:
        """Intitialise an Enemy object

        Args:
            monster_name (str): The name of the monster, refering to the config
            pos (Tuple[int, int]): The initial position (x, y) of the enemy
            groups (List[pygame.sprite.Group]): List of the sprite groups the enemy belongs to
            obstacles (pygame.sprite.Group): Sprite groupe containing obstacles the enemy can
                collide to
        """
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

    def _import_graphics(self, name: str) -> None:
        """Import graphics for the different enemy animations

        Args:
            name (str): The name of the enemy
        """
        self.animations = {
            'idle': [],
            'move': [],
            'attack': []
        }
        main_path = f'lib/images/monsters/{name}/'

        for animation in self.animations:
            self.animations[animation] = import_image_from_folder(main_path + animation)

    def _get_status(self, player: Player) -> None:
        """Determine the status of the enemy based on player distance

        Args:
            player (Player): The player object
        """
        distance, _ = self._get_player_distance_direction(player)

        if distance <= self.attack_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def _get_player_distance_direction(self, player: Player) -> Tuple[float, pygame.math.Vector2]:
        """Calculate the distance and direction to the player

        Args:
            player (Player): The player object

        Returns:
            Tuple[float, pygame.math.Vector2]: Distance to the player and the direction as a vector
        """
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return distance, direction

    def _action(self, player: Player) -> None:
        """Perform an action based on the enemy current status

        Args:
            player (Player): The player object
        """
        if self.status == 'attack':
            print('attack')
        elif self.status == 'move':
            _, self.direction = self._get_player_distance_direction(player)
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        pass


    def update(self) -> None:
        self._move(self.speed)

    def enemy_update(self, player: Player) -> None:
        self._get_status(player)
        self._action(player)
