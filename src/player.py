"""docstring goes here"""
from __future__ import absolute_import

from typing import Callable, List, Tuple

import pygame

from src.config import config
from src.utils.utils import import_image_from_folder


class Player(pygame.sprite.Sprite):
    """A class representing the player in the game."""

    def __init__(
            self,
            pos: Tuple[int, int],
            groups: List[pygame.sprite.Group],
            obstacles: pygame.sprite.Group,
            create_attack: Callable,
            destroy_attack: Callable
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
        self.frame_index = 0
        self.animation_speed = config.player_animation_speed

        # Player initial attributes
        self.direction = pygame.math.Vector2()
        self.speed = config.player_speed
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
        self.weapon_switch_cooldown = config.weapon_switch_cooldown

        # Obstacles of the player for which we have to handle collision
        self.obstacles_sprite = obstacles

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
                print('magic')

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
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
                self.can_switch_weapon = True

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


    def update(self) -> None:
        """Updates the player's actions and status."""
        self._input()
        self._cooldowns()
        self._get_status()
        self._animate()
        self._move(self.speed)
