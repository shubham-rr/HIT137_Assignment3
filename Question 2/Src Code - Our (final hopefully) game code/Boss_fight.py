import pygame
import math
import random
import button
from Game_Loop import NormalEnemy, MovingPlatform, Water, score_manager, jump_fx, player, shot_fx
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Boss Fight Level')

clock = pygame.time.Clock()
FPS = 60

# define game variables
GRAVITY = 0.75
TILE_SIZE = 40
screen_scroll = 0
level = 1

#define colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# load images
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()

# define font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Boss(NormalEnemy):
    def __init__(self, x, y, speed, health):
        super().__init__(x, y, speed, health)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 4), int(self.image.get_height() * 4)))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.health = health
        self.max_health = health
        self.phase = 1
        self.has_shield = True
        self.shield_angle = 0

    def update(self, player, screen_width):
        """Handles boss behavior, including phase transitions."""
        if self.health <= self.max_health // 2 and self.phase == 1:
            self.enter_phase_two()

        if self.phase == 1:
            self.charge_at_player(player)
        elif self.phase == 2:
            self.move_between_sides(screen_width)
            self.spin_shield()

        super().update_animation()

    def enter_phase_two(self):
        # Transition to phase 2
        self.phase = 2
        self.has_shield = False  # Shield no longer applies, but a new spinning shield mechanic begins

    def charge_at_player(self, player):
        """Boss charges towards the player if on the same platform in phase 1."""
        if self.rect.bottom == player.rect.bottom:
            if player.rect.x < self.rect.x:
                self.direction = -1
            else:
                self.direction = 1
            self.rect.x += self.speed * self.direction

    def move_between_sides(self, screen_width):
        """In phase 2, boss runs between sides of the screen randomly."""
        if random.randint(1, 100) < 2:
            self.direction = -1 if self.rect.x > screen_width / 2 else 1
        self.rect.x += self.speed * self.direction
    
    def spin_shield(self):
        """Spins the shield around the boss during phase 2."""
        self.shield_angle += 5  # Adjust the shield angle each frame
        if self.shield_angle >= 360:
            self.shield_angle -= 360

    def take_damage(self, amount):
        # Handle damage and check if boss is dead
        if not self.has_shield or self.phase == 2:
            self.health -= amount
        if self.health <= 0:
            self.alive = False

    def draw_shield(self, screen):
        # Draw the spinning shield around the boss during phase 2
        if self.phase == 2:
            shield_radius = 50
            shield_x = self.rect.centerx + shield_radius * math.cos(math.radians(self.shield_angle))
            shield_y = self.rect.centery + shield_radius * math.sin(math.radians(self.shield_angle))
            pygame.draw.circle(screen, (0, 0, 255), (int(shield_x), int(shield_y)), 10)  # Blue shield        
    
    def draw_health_bar(self, screen):
        # Draw the health bar above the boss
        bar_length = 150
        bar_height = 10
        fill = (self.health / self.max_health) * bar_length
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.centerx - bar_length // 2, self.rect.top - 20, bar_length, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.centerx - bar_length // 2, self.rect.top - 20, fill, bar_height))
    
    # Function to initialize the boss fight level
def load_boss_level():
    boss = Boss(400, 300)
    moving_platform_left = MovingPlatform(50, 500, 100, 20, 'vertical', 2)
    moving_platform_right = MovingPlatform(650, 500, 100, 20, 'vertical', 2)            
    platform_group = pygame.sprite.Group()
    platform_group.add(moving_platform_left, moving_platform_right)
    return boss, platform_group

# Initialize boss level
boss, platform_group = load_boss_level()

# Create sprite groups
player_group = pygame.sprite.GroupSingle()  # Assuming only one player instance
boss_group = pygame.sprite.GroupSingle(boss)
                                       
def update_boss_level(screen, player, boss, platform_group):
    screen.fill((0, 0, 0))  # Black background
    for platform in platform_group:
        platform.update()

    platform_group.draw(screen)
    boss.update(player, screen.get_width())
    boss.draw(screen)


# game loop
run = True
while run:
    clock.tick(FPS)

    screen.fill((144, 201, 120))  # Fill the screen with a green background

    # update and draw player
    player_group.update()
    player_group.draw(screen)


    # update and draw boss
    boss_group.update()
    boss_group.draw(screen)

     # Update and draw boss
    boss.update(player_group.sprite, SCREEN_WIDTH)
    boss_group.draw(screen)
    boss.draw_health_bar(screen)
    boss.draw_shield(screen)

    # draw boss health bar
    boss.draw()

    # update and draw platforms in phase 2
    if boss.phase == 2:
        platform_group.update()
        platform_group.draw(screen)

    # check for collision between player and boss
    if pygame.sprite.spritecollide(player_group.sprite, boss_group, False):
        draw_text('YOU DIED', font, RED, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        pygame.display.update()
        pygame.time.wait(2000)
        run = False

    # event handler
    for event in pygame.event.get():
    # Quit game
        if event.type == pygame.QUIT:
            run = False

        # Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                run = False

        # Keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_w:
                player.jump = False

        # Handle shooting
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                shoot = True
                if player.alive and player.shoot_cooldown == 0:
                    # Player shoots towards the mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    angle = math.atan2(mouse_pos[1] - player.rect.centery, mouse_pos[0] - player.rect.centerx)
                    player.create_bullet(angle)
                    shot_fx.play()
                    player.shoot_cooldown = 15  # Cooldown to control fire rate

        # Handle mouse button releases
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                shoot = False

    pygame.display.update()

pygame.quit()