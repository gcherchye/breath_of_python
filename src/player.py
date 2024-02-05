"""docstring goes here"""
from __future__ import absolute_import

from typing import Callable, List, Tuple

import pygame

from src.entity import Entity
from src.config import config
from src.utils.utils import import_image_from_folder


class Player(Entity):
    """A class representing the player in the game."""

    def __init__(
            self,
            pos: Tuple[int, int],
            groups: List[pygame.sprite.Group],
            obstacles: pygame.sprite.Group,
            create_attack: Callable,
            destroy_attack: Callable,
            create_magic: Callable
        ) -> None:
        """Initializes the Player class.

        Args:
            pos (Tuple[int, int]): The initial position of the player.
            groups (List[pygame.sprite.Group]): List of sprite groups to add the player to.
            obstacles (pygame.sprite.Group): Sprite group representing obstacles.
            create_attack (Callable): Function to create an attack.
            destroy_attack (Callable): Function to destroy an attack.
        """
        super().__init__(groups)

        # Image init
        self.image = pygame.image.load('lib/images/dummy/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Loading animation
        self.import_player_assets(config.player_img_path)
        self.status = 'down'

        # Player initial attributes
        self.attacking = False
        self.attack_cooldown = config.player_attack_cooldown
        self.attack_time = None

        # Weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(config.weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = config.switch_duration_cooldown

        # Magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(config.magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # Stats
        self.stats = config.player_stats
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

        # Obstacles of the player for which we have to handle collision
        self.obstacles_sprite = obstacles

        # Damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invincibility_duration = self.stats['invincibility_duration']

    def import_player_assets(self, path: str) -> None:
        """Imports player assets for animations

        Args:
            path (str): Path to the folder containing player animation assets.
        """
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

    def _input(self) -> None:
        """Handle user input to control player actions

        Detects and processes key presses by the user to manipulate the player's avatar behavior.

        Reads the keyboard input to determine movement and attack actions:
        - 'Z' or 'S' keys control vertical movement (up/down).
        - 'D' or 'Q' keys control horizontal movement (right/left).
        - 'SPACE' triggers an attack action, initiating the attack sequence.
        - 'A' triggers weapon switching if available, cycling through different weapons.
        - 'LCTRL' triggers a special attack action.

        The method updates the player's direction, status, and triggers relevant actions based
        on the keys pressed. It manages movement, attacking, weapon switching, and special
        attacks according to the assigned keys.
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
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            if keys[pygame.K_a] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(config.weapon_data) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(config.weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(config.magic_data.keys())[self.magic_index]
                strenght = list(config.magic_data.values())[self.magic_index]['strenght'] + \
                        self.stats['magic']
                cost = list(config.magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strenght, cost)

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(config.magic_data) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(config.magic_data.keys())[self.magic_index]

    def _get_status(self) -> None:
        """Determines the current status of the player"""
        # Idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not any(old in self.status for old in ['_idle', '_attack']):
                self.status += '_idle'

        # Attacking
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

    def _cooldowns(self) -> None:
        """Manages cooldowns for attacks and weapon switching.

        This method checks cooldowns for the player's attacks and weapon switching.

        If the player is currently attacking, it checks whether enough time has passed since the
        last attack. If the attack cooldown has been reached, it resets the attacking status and
        destroys the attack.

        Additionally, it monitors the cooldown for switching weapons. If the player is currently
        unable to switch weapons (due to a recent switch), it checks whether enough time has elapsed
        to enable weapon switching again.
        """
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= \
                    self.attack_cooldown + config.weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.vulnerable = True

    def _animate(self) -> None:
        """Manages sprite animation based on current status.

        This method handles sprite animation by cycling through frames according to the current
        status of the sprite. It retrieves the appropriate animation based on the current status,
        increments the frame index by the animation speed, resets the index if it exceeds the number
        of frames in the animation, and updates the sprite's image and position accordingly.
        """
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # Flicker if hit
        if not self.vulnerable:
            alpha = self._wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)


    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = config.weapon_data[self.weapon]['damage']

        return base_damage + weapon_damage

    def update(self) -> None:
        """Updates the player's actions and status."""
        self._input()
        self._cooldowns()
        self._get_status()
        self._animate()
        self._move(self.speed)
