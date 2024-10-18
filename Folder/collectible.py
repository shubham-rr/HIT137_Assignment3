import pygame
import logging
from constants import (HEALTH_ITEM_ICON_PATH, HEALTH_ITEM_SIZE, 
                       STAKE_SPRITE_PATH, STAKE_WIDTH, STAKE_HEIGHT, 
                       AMMO_SPRITE_PATH, AMMO_COLLECTIBLE_SIZE,
                       COLLECTIBLE_SPEED
                       )

logging.basicConfig(level=logging.ERROR)

class Collectible(pygame.sprite.Sprite):
    # Inheritance: Collectible inherits from pygame.sprite.Sprite
    # Encapsulation: Bundling data and methods within a single unit
    def __init__(self, x, y, type):
        try:
            super().__init__()
            self.type = type
            if self.type == 'health':
                self.image = pygame.image.load(HEALTH_ITEM_ICON_PATH).convert_alpha()
                self.image = pygame.transform.scale(self.image, HEALTH_ITEM_SIZE)
            elif self.type == 'ammo':
                self.image = pygame.image.load(AMMO_SPRITE_PATH).convert_alpha()
                self.image = pygame.transform.scale(self.image, (AMMO_COLLECTIBLE_SIZE, AMMO_COLLECTIBLE_SIZE))
            elif self.type == 'stake':
                self.image = pygame.image.load(STAKE_SPRITE_PATH).convert_alpha()
                self.image = pygame.transform.scale(self.image, (STAKE_WIDTH, STAKE_HEIGHT))
            else:
                raise ValueError(f"Invalid collectible type: {type}")
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = COLLECTIBLE_SPEED  # Adjust speed of collectibles
        except Exception as e:
            logging.error(f"Error initializing Collectible: {e}")
            raise

    # Polymorphism: This method can be called on any Sprite object
    def update(self):
        try:
            # Move the collectible downwards
            self.rect.y += self.speed
            # Remove if it goes off-screen
            if self.rect.top > pygame.display.get_surface().get_height():
                self.kill()
        except Exception as e:
            logging.error(f"Error updating Collectible: {e}")
            raise
