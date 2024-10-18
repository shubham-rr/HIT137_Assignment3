import pygame
import random
import logging
from character import Character
from projectile import Projectile
from constants import (
    ENEMY_BULLET_DAMAGE, ENEMY_MIN_SPEED, ENEMY_MAX_SPEED, ENEMY_WIDTH, ENEMY_HEIGHT, 
    BOSS_WIDTH, BOSS_HEIGHT, BOSS_BULLET_DAMAGE, ENEMY_PROJECTILE_WIDTH, ENEMY_PROJECTILE_HEIGHT,
    BOSS_PROJECTILE_WIDTH, BOSS_PROJECTILE_HEIGHT,
    ENEMY_SPRITE_PATH, ENEMY_DEATH_SPRITE_PATH, ENHANCED_ENEMY_SPRITE_PATH,
    ENHANCED_ENEMY_DEATH_SPRITE_PATH, BOSS_SPRITE_PATH, BOSS_DEATH_SPRITE_PATH,
    ENEMY_HEALTH, ENHANCED_ENEMY_HEALTH, BOSS_HEALTH
)

logging.basicConfig(level=logging.ERROR)

class Enemy(Character):
    # Inheritance: Enemy inherits from Character
    def __init__(self, x, y, platform_y):
        try:
            super().__init__(x, y, ENEMY_WIDTH, ENEMY_HEIGHT, platform_y, health=ENEMY_HEALTH)
            self.load_sprite('normal', ENEMY_SPRITE_PATH)
            self.load_sprite('death', ENEMY_DEATH_SPRITE_PATH)
            self.set_sprite('normal')
            self.speed = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
            self.bullets = pygame.sprite.Group()
            self.shoot_cooldown = random.randint(60, 120)  # Random cooldown
            self.direction = -1  # Start moving left
            self.screen_center = pygame.display.get_surface().get_width() // 2
        except Exception as e:
            logging.error(f"Error initializing Enemy: {e}")
            raise

    # Method overriding: Customizing the load_sprite method for Enemy
    def load_sprite(self, state, path):
        try:
            sprite = pygame.image.load(path).convert_alpha()
            self.sprites[state] = pygame.transform.scale(sprite, (self.rect.width, self.rect.height))
        except pygame.error as e:
            logging.error(f"Error loading sprite {path}: {e}")
            raise

    # Polymorphism: Overriding the move method from Character
    def move(self):
        # Change direction if at screen edge or center
        if self.rect.right > pygame.display.get_surface().get_width():
            self.direction = -1
        elif self.rect.left < self.screen_center:
            self.direction = 1

        self.velocity_x = self.speed * self.direction
        super().move()

    # Encapsulation: Method specific to Enemy behavior
    def shoot(self):
        try:
            bullet = Projectile(self.rect.centerx, self.rect.centery, -1, ENEMY_BULLET_DAMAGE, 'enemy', 
                                width=ENEMY_PROJECTILE_WIDTH, height=ENEMY_PROJECTILE_HEIGHT)
            self.bullets.add(bullet)
        except Exception as e:
            logging.error(f"Error shooting bullet: {e}")
            raise

    # Polymorphism: Overriding the update method from Character
    def update(self):
        try:
            self.move()
            super().update()
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1
            else:
                self.shoot()
                self.shoot_cooldown = random.randint(60, 120)
            self.bullets.update()

            # Remove bullets that go off-screen
            for bullet in self.bullets:
                if bullet.rect.right < 0:
                    self.bullets.remove(bullet)
        except Exception as e:
            logging.error(f"Error updating Enemy: {e}")
            raise

    # Polymorphism: Overriding the draw method from Character
    def draw(self, screen):
        try:
            super().draw(screen)
            self.bullets.draw(screen)
        except Exception as e:
            logging.error(f"Error drawing Enemy: {e}")
            raise

class EnhancedEnemy(Enemy):
    # Inheritance: EnhancedEnemy inherits from Enemy
    def __init__(self, x, y, platform_y):
        try:
            super().__init__(x, y, platform_y)
            self.load_sprite('normal', ENHANCED_ENEMY_SPRITE_PATH)
            self.load_sprite('death', ENHANCED_ENEMY_DEATH_SPRITE_PATH)
            self.set_sprite('normal')
            self.speed = random.randint(ENEMY_MIN_SPEED + 1, ENEMY_MAX_SPEED + 1)  # Slightly faster
            self.health = ENHANCED_ENEMY_HEALTH
        except Exception as e:
            logging.error(f"Error initializing EnhancedEnemy: {e}")
            raise

    # Polymorphism: Overriding the shoot method from Enemy
    def shoot(self):
        try:
            bullet = Projectile(self.rect.centerx, self.rect.centery, -1, ENEMY_BULLET_DAMAGE, 'enemy', 
                                width=ENEMY_PROJECTILE_WIDTH, height=ENEMY_PROJECTILE_HEIGHT)
            self.bullets.add(bullet)
        except Exception as e:
            logging.error(f"Error shooting bullet: {e}")
            raise

class Boss(Enemy):
    # Inheritance: Boss inherits from Enemy
    def __init__(self, x, y, platform_y):
        try:
            super().__init__(x, y, platform_y)
            self.rect = pygame.Rect(x, y, BOSS_WIDTH, BOSS_HEIGHT)
            self.load_sprite('normal', BOSS_SPRITE_PATH)
            self.load_sprite('death', BOSS_DEATH_SPRITE_PATH)
            self.set_sprite('normal')
            self.speed = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)  # Same speed range as regular enemies
            self.health = BOSS_HEALTH 
        except Exception as e:
            logging.error(f"Error initializing Boss: {e}")
            raise

    # Polymorphism: Overriding the shoot method from Enemy
    def shoot(self):
        try:
            bullet = Projectile(self.rect.centerx, self.rect.centery, -1, BOSS_BULLET_DAMAGE, 'boss', 
                                width=BOSS_PROJECTILE_WIDTH, height=BOSS_PROJECTILE_HEIGHT)
            self.bullets.add(bullet)
        except Exception as e:
            logging.error(f"Error shooting bullet: {e}")
            raise

    # Polymorphism: Overriding the update method from Enemy
    def update(self):
        try:
            super().update()
        except Exception as e:
            logging.error(f"Error updating Boss: {e}")
            raise
