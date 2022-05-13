"""Main game file"""
from __future__ import absolute_import

import sys

import pygame

from config import config
from level import Level


class Game:
    """Declaration of a Breath of Python Game"""

    def __init__(self) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()

        self.config = config
        self.screen = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption('Breath of Python')

        self.level = Level()

    def run(self):
        """Run the game"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()

            pygame.display.update()
            self.clock.tick(config.fps)


if __name__ == '__main__':
    game = Game()
    game.run()
