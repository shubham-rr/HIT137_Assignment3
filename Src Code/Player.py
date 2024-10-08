# player.py
import pygame
from Jump import JumpMechanics
import Gun

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 300
        self.speed = 5
        self.on_ground = False
        self.jump_count = 0
        self.max_jumps = 2
        self.jump_mechanics = JumpMechanics()
        self.guns = [Gun("pistol"), Gun("rifle")]
        self.current_gun = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Jump logic with coyote time and jump buffering
        if keys[pygame.K_SPACE]:
            self.jump_mechanics.jump_buffer_timer = self.jump_mechanics.jump_buffer_time
        else:
            self.jump_mechanics.jump_buffer_timer -= 1 / 60

        if (self.on_ground or self.jump_mechanics.coyote_timer > 0) and self.jump_mechanics.jump_buffer_timer > 0:
            if self.jump_mechanics.jump_hold_time < self.jump_mechanics.max_jump_hold_time:
                self.jump_mechanics.velocity_y = self.jump_mechanics.jump_speed
                self.jump_mechanics.jump_hold_time += 1
                if self.on_ground:
                    self.jump_count = 1
                else:
                    self.jump_count += 1
            self.jump_mechanics.jump_buffer_timer = 0

        # Apply gravity and increase falling speed
        self.jump_mechanics.apply_gravity()
        self.jump_mechanics.increase_falling_speed()
        self.jump_mechanics.cap_falling_speed()

        self.rect.y += self.jump_mechanics.velocity_y

        # Check if on ground
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.jump_mechanics.velocity_y = 0
            self.on_ground = True
            self.jump_mechanics.reset_jump_timers()
            self.jump_count = 0
        else:
            self.on_ground = False
            self.jump_mechanics.coyote_timer -= 1 / 60

        # Wall jump logic (optional)
        if self.rect.left <= 0 or self.rect.right >= 800:
            if keys[pygame.K_SPACE]:
                self.jump_mechanics.velocity_y = self.jump_mechanics.jump_speed
                self.jump_count = 1


import pygame
from pygame import mixer
import os
import random
import csv
import button

# Initialize mixer and pygame
mixer.init()
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Create display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False

# Define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False
aim_angle = 0

# Load music and sounds
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.05)
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.05)

# Load images
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

# Load tile images into a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# Load other images
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()

# Dictionary for item boxes
item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img
}

# Define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)

# Define font
font = pygame.font.SysFont('Futura', 30)

# Function to draw text on the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function to draw the background
def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

# Function to reset the level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # Create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data

# Soldier class
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = {'normal': 10, 'blast': 2}
        self.start_ammo = self.ammo.copy()
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.last_shot_time = pygame.time.get_ticks()
        self.reload_time = {'normal': 3000, 'blast': 5000}
        self.auto_reload_time = 2000
        self.last_reload_time = pygame.time.get_ticks()
        # AI specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0
        
        # Load all images for the player
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # Reset temporary list of images
            temp_list = []
            # Count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()
        self.reload_ammo()
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # Reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # Assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # Check for collision
        for tile in world.obstacle_list:
            # Check collision in the x direction
            if tile.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                # If the AI has hit a wall then make it turn around
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            # Check for collision in the y direction
            if tile.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile.bottom - self.rect.top
                # Check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile.top - self.rect.bottom

        # Check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        # Check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # Update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and
        # Update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        return screen_scroll, level_complete

    def shoot(self, gun_type):
        # Check if enough time has passed since the last shot
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.reload_time[gun_type]:
            if self.ammo[gun_type] > 0:
                self.ammo[gun_type] -= 1
                self.shoot_cooldown = 20
                self.last_shot_time = current_time
                # Create bullet instance
                bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size * self.direction), self.rect.centery, self.direction, gun_type)
                bullet_group.add(bullet)
                # Play gun sound
                shot_fx.play()
            else:
                # Reload if out of ammo
                self.reload_ammo(gun_type)

    def reload_ammo(self, gun_type=None):
        current_time = pygame.time.get_ticks()
        if gun_type:
            if current_time - self.last_shot_time > self.reload_time[gun_type]:
                self.ammo[gun_type] = self.start_ammo[gun_type]
        else:
            if current_time - self.last_reload_time > self.auto_reload_time:
                self.ammo['normal'] = self.start_ammo['normal']
                self.ammo['blast'] = self.start_ammo['blast']
                self.last_reload_time = current_time

    def update_animation(self):
        # Update animation
        ANIMATION_COOLDOWN = 100
        # Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # If the animation has run out, reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(3)  # 3: death

    def update_action(self, new_action):
        # Check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, gun_type):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img if gun_type == 'normal' else grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # Move bullet
        self.rect.x += (self.direction * self.speed)
        # Check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # Check for collision with level
        for tile in world.obstacle_list:
            if tile.colliderect(self.rect):
                self.kill()


# Create groups
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# Main game loop
run = True
while run:
    clock.tick(FPS)

    draw_bg()

    # Update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
