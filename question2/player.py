import pygame
import logging
from character import Character
from projectile import Projectile
from constants import (MOVE_LEFT, MOVE_RIGHT, JUMP, SHOOT, PLAYER_WIDTH, PLAYER_HEIGHT, 
                       MAX_PLAYER_HEALTH, PLAYER_MAX_AMMO, PLAYER_STARTING_AMMO, PLAYER_SPEED, 
                       PLAYER_BULLET_DAMAGE, PLAYER_PROJECTILE_WIDTH, PLAYER_PROJECTILE_HEIGHT,
                       PLAYER_START_LIVES, PLAYER_RESPAWN_INVULNERABILITY_TIME,
                       PLAYER_IDLE_SPRITE_PATH, PLAYER_JUMPING_SPRITE_PATH, 
                       PLAYER_FALLING_SPRITE_PATH, PLAYER_DAMAGED_SPRITE_PATH, 
                       PLAYER_DEAD_SPRITE_PATH)

logging.basicConfig(level=logging.ERROR)

class Player(Character):
    # Inheritance: Player inherits from Character
    def __init__(self, x, y, platform_y):
        try:
            super().__init__(x, y, PLAYER_WIDTH, PLAYER_HEIGHT, platform_y, health=MAX_PLAYER_HEALTH)
            self.load_sprite('idle', PLAYER_IDLE_SPRITE_PATH)
            self.load_sprite('jumping', PLAYER_JUMPING_SPRITE_PATH)
            self.load_sprite('falling', PLAYER_FALLING_SPRITE_PATH)
            self.load_sprite('damaged', PLAYER_DAMAGED_SPRITE_PATH)
            self.load_sprite('dead', PLAYER_DEAD_SPRITE_PATH)
            self.set_sprite('idle')
            self.bullets = pygame.sprite.Group()
            self.shoot_cooldown = 0
            self.ammo = PLAYER_STARTING_AMMO
            self.max_ammo = PLAYER_MAX_AMMO
            self.lives = PLAYER_START_LIVES
            self.invulnerable = False
            self.invulnerable_timer = 0
        except Exception as e:
            logging.error(f"Error initializing Player: {e}")
            raise

    # Polymorphism: Overriding the load_sprite method from Character
    def load_sprite(self, state, path):
        try:
            sprite = pygame.image.load(path).convert_alpha()
            self.sprites[state] = pygame.transform.scale(sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
        except pygame.error as e:
            logging.error(f"Error loading sprite {path}: {e}")
            raise

    # Encapsulation: Method for handling player input
    def handle_input(self):
        try:
            keys = pygame.key.get_pressed()
            self.velocity_x = 0
            if keys[MOVE_LEFT]:
                self.velocity_x = -PLAYER_SPEED
            if keys[MOVE_RIGHT]:
                self.velocity_x = PLAYER_SPEED
            if keys[JUMP]:
                self.jump()
            if keys[SHOOT] and self.shoot_cooldown == 0:
                self.shoot()
                self.shoot_cooldown = 20
        except Exception as e:
            logging.error(f"Error handling player input: {e}")
            raise

    # Encapsulation: Method for player shooting
    def shoot(self):
        try:
            if self.ammo > 0 and self.shoot_cooldown == 0:
                bullet = Projectile(self.rect.centerx, self.rect.centery, 1, PLAYER_BULLET_DAMAGE, 'player', 
                                    width=PLAYER_PROJECTILE_WIDTH, height=PLAYER_PROJECTILE_HEIGHT)
                self.bullets.add(bullet)
                self.ammo -= 1
                self.shoot_cooldown = 20
        except Exception as e:
            logging.error(f"Error shooting bullet: {e}")
            raise

    # Encapsulation: Method for adding ammo
    def add_ammo(self, amount):
        try:
            self.ammo = min(self.ammo + amount, self.max_ammo)
        except Exception as e:
            logging.error(f"Error adding ammo: {e}")
            raise

    # Polymorphism: Overriding the update method from Character
    def update(self):
        try:
            self.handle_input()
            super().update()
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1
            self.bullets.update()
            
            if self.is_taking_damage:
                self.set_sprite('damaged')
            else:
                if self.velocity_y < 0:
                    self.set_sprite('jumping')
                elif self.velocity_y > 0:
                    self.set_sprite('falling')
                elif self.velocity_x == 0 and self.velocity_y == 0:
                    self.set_sprite('idle')

            current_time = pygame.time.get_ticks()
            if self.invulnerable and current_time - self.invulnerable_timer > PLAYER_RESPAWN_INVULNERABILITY_TIME:
                self.invulnerable = False
        except Exception as e:
            logging.error(f"Error updating player: {e}")
            raise

    # Polymorphism: Overriding the draw method from Character
    def draw(self, screen):
        try:
            if self.invulnerable:
                if pygame.time.get_ticks() % 200 < 100:  # Flashing effect
                    super().draw(screen)
            else:
                super().draw(screen)
            self.bullets.draw(screen)
        except Exception as e:
            logging.error(f"Error drawing player: {e}")
            raise

    # Polymorphism: Overriding the take_damage method from Character
    def take_damage(self, amount):
        try:
            if not self.invulnerable:
                super().take_damage(amount)
                if self.health <= 0:
                    self.lives -= 1
                    if self.lives > 0:
                        self.respawn()
                    else:
                        self.set_sprite('dead')
        except Exception as e:
            logging.error(f"Error taking damage: {e}")
            raise

    # Encapsulation: Method for player respawn
    def respawn(self):
        try:
            self.health = MAX_PLAYER_HEALTH
            self.set_sprite('idle')
            self.invulnerable = True
            self.invulnerable_timer = pygame.time.get_ticks()
        except Exception as e:
            logging.error(f"Error respawning player: {e}")
            raise

    # Encapsulation: Method for healing the player
    def heal(self, amount):
        try:
            self.health = min(MAX_PLAYER_HEALTH, self.health + amount)
        except Exception as e:
            logging.error(f"Error healing player: {e}")
            raise

    # Encapsulation: Method for resetting player position
    def reset_position(self, x, y):
        try:
            self.rect.x = x
            self.rect.y = y
            self.velocity_x = 0
            self.velocity_y = 0
        except Exception as e:
            logging.error(f"Error resetting player position: {e}")
            raise
