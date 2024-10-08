
import pygame
import math

class Gun:
    def __init__(self, gun_type):
        self.gun_type = gun_type
        self.angle = 0
        self.recoil = pygame.math.Vector2(0, 0)
        if gun_type == "pistol":
            self.recoil = pygame.math.Vector2(5, 0)
        elif gun_type == "rifle":
            self.recoil = pygame.math.Vector2(10, 0)

    def update(self, mouse_pos, player_pos):
        rel_x, rel_y = mouse_pos[0] - player_pos[0], mouse_pos[1] - player_pos[1]
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

    def shoot(self, player_pos):
        # Implement shooting logic here
        pass

    def draw(self, screen):
        # Implement drawing logic here
        pass
