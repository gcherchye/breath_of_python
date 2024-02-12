"""slip de bain"""
from __future__ import absolute_import

from typing import List

import pygame

from src.config import config
from src.utils.utils import import_image_from_folder


class AnimationPlayer:
    def __init__(self) -> None:
        self.frames = {
            # Magic
            'flame': import_image_from_folder('lib/images/particles/flame/frames'),
            'aura': import_image_from_folder('lib/images/particles/aura/'),
            'heal': import_image_from_folder('lib/images/particles/heal/frames'),

            # Attacks
            'claw': import_image_from_folder('lib/images/particles/claw/'),
            'splash': import_image_from_folder('lib/images/particles/splash/'),
            'sparkle': import_image_from_folder('lib/images/particles/sparkle/'),
            'leaf_attack': import_image_from_folder('lib/images/particles/leaf_attack/'),
            'thunder': import_image_from_folder('lib/images/particles/thunder/'),

            # Monster deaths
            'squid': import_image_from_folder('lib/images/particles/smoke_orange/'),
            'raccoon': import_image_from_folder('lib/images/particles/raccoon/'),
            'spirit': import_image_from_folder('lib/images/particles/nova/'),
            'bamboo': import_image_from_folder('lib/images/particles/bamboo/'),

            # Leaf
            'leaf': (
                import_image_from_folder('lib/image/particles/leaf1'),
                import_image_from_folder('lib/image/particles/leaf2'),
                import_image_from_folder('lib/image/particles/leaf3'),
                import_image_from_folder('lib/image/particles/leaf4'),
                import_image_from_folder('lib/image/particles/leaf5'),
                import_image_from_folder('lib/image/particles/leaf6'),
                self.reflect_images(import_image_from_folder('lib/image/particles/leaf1')),
                self.reflect_images(import_image_from_folder('lib/image/particles/leaf2')),
                self.reflect_images(import_image_from_folder('lib/image/particles/leaf3')),
                self.reflect_images(import_image_from_folder('lib/image/particles/leaf4')),
                self.reflect_images(import_image_from_folder('lib/image/particles/leaf5')),
                self.reflect_images(import_image_from_folder('lib/image/particles/leaf6')),
            )
        }

    def reflect_images(self, frames: List[pygame.Surface]) -> List[pygame.Surface]:
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)

        return new_frames

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, animation_frames, groups) -> None:
        super().__init__(groups)

        self.animation_speed = config.animation_speed
        self.frame_index = config.frame_index
        self.frames = animation_frames

        self.image = self.image.get_rect[self.frame_index]

        def _animate(self):
            self.frame_index += self.animation_speed
            if self.frame >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[int(self.frame_index)]

        def update(self):
            self._animate()
