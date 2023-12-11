"""docstring"""
from __future__ import absolute_import
from typing import List

import pygame

from src.entity import Entity


class Enemy(Entity):
    """docstring"""

    def __init__(self, groups: List[pygame.sprite.Group]) -> None:
        super().__init__(groups)
