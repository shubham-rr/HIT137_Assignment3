import pygame
import logging
from constants import SCREEN_WIDTH, MAX_PLAYER_HEALTH

logging.basicConfig(level=logging.ERROR)

class HUD:
    # Encapsulation: Bundling HUD data and methods within a single unit
    def __init__(self, font):
        try:
            self.font = font
        except Exception as e:
            logging.error(f"Error initializing HUD: {e}")
            raise

    # Encapsulation: Method for drawing HUD elements
    def draw(self, screen, player, score):
        try:
            # Health bar
            health_percentage = player.health / MAX_PLAYER_HEALTH
            pygame.draw.rect(screen, (255, 0, 0), (10, 10, 200, 20))
            pygame.draw.rect(screen, (0, 255, 0), (10, 10, 200 * health_percentage, 20))
            
            # Ammo count
            ammo_text = self.font.render(f"Ammo {player.ammo}", True, (255, 255, 255))
            screen.blit(ammo_text, (10, 40))
            
            # Score
            score_text = self.font.render(f"Score {score}", True, (255, 255, 255))
            screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))
        except Exception as e:
            logging.error(f"Error drawing HUD: {e}")
            raise
