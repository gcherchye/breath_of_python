"""docstring"""
from __future__ import absolute_import

from typing import Callable ,List, Tuple

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
            obstacles: pygame.sprite.Group,
            damage: Callable
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

        # Player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = monster_info['cooldown']
        self.damage_player = damage

        # Invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = monster_info['invincibility_duration']

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

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
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
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            _, self.direction = self._get_player_distance_direction(player)
        else:
            self.direction = pygame.math.Vector2()

    def _animate(self) -> None:
        """Animates the enemy based on its current status

        This method updates the enemy's image to the next frame in the corresponding animation
        sequence, considering the animation speed and status. It handles frame looping and
        manages the attack status.
        """

        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.status]):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # Flicker if hit
        if not self.vulnerable:
            alpha = self._wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def _cooldowns(self) -> None:
        """Manages cooldowns for the enemy

        This method checks and updates the cooldown status for attacks and invincibility. It
        ensures that the enemy can attack again after a specified cooldown period and becomes
        vulnerable again after a certain invincibility duration.
        """
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def _check_death(self) -> None:
        """Check if the enemy is dead according to his current health"""
        if self.health <= 0:
            self.kill()

    def _hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def get_damage(self, player: Player, attack_type: str) -> None:
        """Applies damage to the enemy based on the type of attack

        This method reduces the enemy's health when it receives damage from a player's attack,
        considering the attack type and the enemy's vulnerability status. It updates the hit
        time and sets the enemy to be invulnerable for a specified duration.

        Args:
            player(Player): The player object
            attack_type (str): The type of attack, 'weapon' for physical attacks, or 'magic' for
                magical attacks
        """
        if self.vulnerable:
            self.direction = self._get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                pass  # Magic damage
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def update(self) -> None:
        """Updates the sprite's movement, animation, cooldowns, and checks for death"""
        self._hit_reaction()
        self._move(self.speed)
        self._animate()
        self._cooldowns()
        self._check_death()

    def enemy_update(self, player: Player) -> None:
        """Updates the enemy sprite's status, actions, and interactions with the player

        Args:
            player (Player): The player object
        """
        self._get_status(player)
        self._action(player)
