import pygame
from Player import Player
from Projectiles import Projectile
from Enemies import Enemy
from Collectible import Collectible
from Camera import Camera
from Scoring import Scoring
from Game_Over import GameOver
from Jump import JumpMechanics
import Gun


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Side-Scrolling Game")
    clock = pygame.time.Clock()

    player = Player()
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    all_sprites.add(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    projectile = Projectile(player.rect.right, player.rect.centery)
                    all_sprites.add(projectile)
                    projectiles.add(projectile)

        all_sprites.update()

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
