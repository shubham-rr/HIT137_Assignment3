import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.angle = angle
        self.speed = 10
        self.velocity = pygame.math.Vector2(self.speed * math.cos(math.radians(self.angle)),
                                            -self.speed * math.sin(math.radians(self.angle)))

    def update(self):
        self.rect.move_ip(self.velocity)
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()
