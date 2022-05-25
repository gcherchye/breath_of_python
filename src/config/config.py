"""Config file for the game"""
from __future__ import absolute_import

from dataclasses import dataclass


@dataclass
class Configuration:
    """Global configuration class"""
    # Screen config
    width = 1280
    height = 720
    tilesize = 64

    # Time config
    fps = 60

    # Player config
    player_speed = 5
    player_attack_cooldown = 400
