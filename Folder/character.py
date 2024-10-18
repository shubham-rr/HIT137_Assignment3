import pygame
import logging

logging.basicConfig(level=logging.ERROR)

class Character(pygame.sprite.Sprite):
    # Encapsulation: Bundling data and methods within a single unit
    def __init__(self, x, y, width, height, platform_y, health):
        try:
            super().__init__()  # Inheritance: Character inherits from pygame.sprite.Sprite
            self.sprites = {}  # Dictionary to store different sprite images
            self.current_sprite = 'idle'  # Default sprite state
            self.image = pygame.Surface([width, height])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.velocity_x = 0
            self.velocity_y = 0
            self.is_jumping = False
            self.jump_power = 15
            self.gravity = 0.8
            self.platform_y = platform_y
            self.health = health
            self.max_health = health
            self.is_taking_damage = False
            self.damage_timer = 0
            self.damage_duration = 30  # Show damage sprite for 30 frames (0.5 seconds at 60 FPS)
        except Exception as e:
            logging.error(f"Error initializing Character: {e}")
            raise

    # Abstraction: Defining a common interface for loading sprites
    def load_sprite(self, state, path):
        try:
            self.sprites[state] = pygame.image.load(path).convert_alpha()
            self.sprites[state] = pygame.transform.scale(self.sprites[state], (self.rect.width, self.rect.height))
        except pygame.error as e:
            logging.error(f"Error loading sprite {path}: {e}")
            raise

    # Abstraction: Defining a common interface for setting sprites
    def set_sprite(self, state):
        if state in self.sprites:
            self.current_sprite = state
            self.image = self.sprites[state]

    # Encapsulation: Method operating on the object's data
    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    # Encapsulation: Method implementing character-specific logic
    def apply_gravity(self):
        if self.is_jumping or self.rect.bottom < self.platform_y:
            self.velocity_y += self.gravity
            if self.velocity_y > 10:  # Terminal velocity
                self.velocity_y = 10
            if self.velocity_y > 0:
                self.set_sprite('falling')
        
        # Check if character has landed on the platform
        if self.rect.bottom >= self.platform_y:
            self.rect.bottom = self.platform_y
            self.is_jumping = False
            self.velocity_y = 0
            self.set_sprite('idle')

    # Encapsulation: Method implementing character-specific logic
    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_power
            self.set_sprite('jumping')

    # Polymorphism: This method can be overridden in subclasses
    def update(self):
        self.move()
        self.apply_gravity()
        if self.is_taking_damage:
            self.damage_timer -= 1
            if self.damage_timer <= 0:
                self.is_taking_damage = False
                self.set_sprite('idle')
        elif self.velocity_x == 0 and self.velocity_y == 0:
            self.set_sprite('idle')

    # Polymorphism: This method can be overridden in subclasses
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # Encapsulation: Method operating on the object's data
    def take_damage(self, amount):
        self.health -= amount
        self.is_taking_damage = True
        self.damage_timer = self.damage_duration
        self.set_sprite('damaged')
        if self.health <= 0:
            self.set_sprite('dead')
            self.kill()  # Remove the sprite from all groups

    # Encapsulation: Method providing information about the object's state
    def is_alive(self):
        return self.health > 0
