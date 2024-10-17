import pygame
import logging
from constants import (BULLET_SPEED, SCREEN_WIDTH,
                       PLAYER_PROJECTILE_SPRITE_PATH, ENEMY_PROJECTILE_SPRITE_PATH, BOSS_PROJECTILE_SPRITE_PATH)

logging.basicConfig(level=logging.ERROR)

class Projectile(pygame.sprite.Sprite):
    # Inheritance: Projectile inherits from pygame.sprite.Sprite
    # Encapsulation: Bundling projectile data and methods within a single unit
    def __init__(self, x, y, direction, damage, projectile_type, width=20, height=20):
        try:
            super().__init__()
            self.direction = direction
            self.speed = BULLET_SPEED
            self.damage = damage

            if projectile_type == 'player':
                self.image = pygame.image.load(PLAYER_PROJECTILE_SPRITE_PATH).convert_alpha()
            elif projectile_type == 'enemy':
                self.image = pygame.image.load(ENEMY_PROJECTILE_SPRITE_PATH).convert_alpha()
            elif projectile_type == 'boss':
                self.image = pygame.image.load(BOSS_PROJECTILE_SPRITE_PATH).convert_alpha()
            else:
                raise ValueError("Invalid projectile type")

            self.image = pygame.transform.scale(self.image, (width, height))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
        except Exception as e:
            logging.error(f"Error initializing Projectile: {e}")
            raise

    # Polymorphism: This method can be called on any Sprite object
    def update(self):
        try:
            self.rect.x += self.speed * self.direction
        except Exception as e:
            logging.error(f"Error updating Projectile: {e}")
            raise

    # Encapsulation: Method for checking if projectile is off screen
    def is_off_screen(self):
        try:
            return self.rect.right < 0 or self.rect.left > SCREEN_WIDTH
        except Exception as e:
            logging.error(f"Error checking if Projectile is off screen: {e}")
            raise
