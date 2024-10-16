import pygame, math, os, textwrap
import json # For saving/loading scores
from pygame import mixer
import random
import csv
import button


mixer.init()
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 120
MAX_LEVELS = 4
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False
AUTO_RELOAD_TIME = 120  # Time in frames to auto-reload (2 seconds)

#define player action variables
moving_left = False
moving_right = False
shoot = False


#load music and sounds
#pygame.mixer.music.load('audio/music2.mp3')
#pygame.mixer.music.set_volume(0.3)
#pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.05)

# Placeholder for additional sound effects
reload_fx = pygame.mixer.Sound('audio/shot.wav')
reload_fx.set_volume(0.05)

boss_hit_fx = pygame.mixer.Sound('audio/shot.wav')
boss_hit_fx.set_volume(0.05)

game_over_fx = pygame.mixer.Sound('audio/shot.wav')
game_over_fx.set_volume(0.05)

# bg_level4 = pygame.image.load('asset/img/background/bg_level4.png').convert_alpha()
# bg_level4 = pygame.transform.scale(bg_level4, (SCREEN_WIDTH, SCREEN_HEIGHT))
#load images
#button images
start_img = pygame.image.load('asset/img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('asset/img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('asset/img/restart_btn.png').convert_alpha()
#background
pine1_img = pygame.image.load('asset/img/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('asset/img/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('asset/img/background/mountain.png').convert_alpha()
sky_img = pygame.image.load('asset/img/background/sky_cloud.png').convert_alpha()
#menu background
bg_start_menu = pygame.image.load('asset/img/background/bg_start_menu.png').convert_alpha()
bg_restart = pygame.image.load('asset/img/background/bg_restart.png').convert_alpha()
bg_end = pygame.image.load('asset/img/background/bg_end.png').convert_alpha()

# Background layers for level 2 (4 layers)
bg2_layer1 = pygame.image.load('asset/img/background/bg1_level2.png').convert_alpha()
bg2_layer2 = pygame.image.load('asset/img/background/bg2_level2.png').convert_alpha()
bg2_layer3 = pygame.image.load('asset/img/background/bg3_level2.png').convert_alpha()
bg2_layer4 = pygame.image.load('asset/img/background/bg4_level2.png').convert_alpha()

# Background layers for level 3 (6 layers)
bg3_layer1 = pygame.image.load('asset/img/background/bg1_level3.png').convert_alpha()
bg3_layer2 = pygame.image.load('asset/img/background/bg2_level3.png').convert_alpha()
bg3_layer3 = pygame.image.load('asset/img/background/bg3_level3.png').convert_alpha()
bg3_layer4 = pygame.image.load('asset/img/background/bg4_level3.png').convert_alpha()
bg3_layer5 = pygame.image.load('asset/img/background/bg5_level3.png').convert_alpha()
bg3_layer6 = pygame.image.load('asset/img/background/bg6_level3.png').convert_alpha()

# Background layers for level 4 (3 layers)
bg4_layer1 = pygame.image.load('asset/img/background/bg1_level4.png').convert_alpha()
bg4_layer2 = pygame.image.load('asset/img/background/bg2_level4.png').convert_alpha()
bg4_layer3 = pygame.image.load('asset/img/background/bg3_level4.png').convert_alpha()

# Scale the backgrounds to fit the screen
bg4_layer1 = pygame.transform.scale(bg4_layer1, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg4_layer2 = pygame.transform.scale(bg4_layer2, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg4_layer3 = pygame.transform.scale(bg4_layer3, (SCREEN_WIDTH, SCREEN_HEIGHT))

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'asset/img/tile/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)
#bullet
bullet_img = pygame.image.load('asset/img/icons/bullet.png').convert_alpha()
#Projectile
projectile_img = pygame.image.load('asset/img/icons/projectile.png').convert_alpha()
#grenade
grenade_img = pygame.image.load('asset/img/icons/grenade.png').convert_alpha()
#pick up boxes
health_box_img = pygame.image.load('asset/img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('asset/img/icons/ammo_box.png').convert_alpha()
coin_img = pygame.image.load('asset/img/icons/Coin.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img,
	'Coin'	    : coin_img
}


#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
BLUE = (0, 0, 255)

#define font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_bg():
	screen.fill(BG)
	width = sky_img.get_width()
	for x in range(5):
		screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
		screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_bg_2():
	screen.fill(164, 118, 157)
	width = sky_img.get_width()
	for x in range(5):
		screen.blit(bg3_layer4, ((x * width) - bg_scroll * 0.5, 0))
		screen.blit(bg3_layer3, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - bg3_layer3.get_height() - 300))
		screen.blit(bg3_layer2, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - bg3_layer2.get_height() - 150))
		screen.blit(bg3_layer1, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - bg3_layer1.get_height()))

def draw_bg_3():
	screen.fill(70, 52, 94)
	width = sky_img.get_width()
	for x in range(7):
            screen.blit(bg3_layer1, ((x * width) - bg_scroll * 0.5, 0))
            screen.blit(bg3_layer2, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 500))
            screen.blit(bg3_layer3, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 400))
            screen.blit(bg3_layer4, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height() - 300))
            screen.blit(bg3_layer5, ((x * width) - bg_scroll * 0.9, SCREEN_HEIGHT - bg3_layer2.get_height() - 150))
            screen.blit(bg3_layer6, ((x * width) - bg_scroll * 1, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_bg_4():
    # Draw the background layers in order
    screen.blit(bg4_layer1, (0, 0))  # Layer 1
    screen.blit(bg4_layer2, (0, 0))  # Layer 2
    screen.blit(bg4_layer3, (0, 0))

#function to reset level
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    platform_group.empty()    # For dynamically created platforms (e.g., phase 2 platforms in boss fight)
    boss_group.empty()        # If you have a group to track the boss entity
    projectile_group.empty()  # If the boss shoots projectiles

    # Reset the player's stats if necessary
    player.health = player.max_health
    player.ammo = player.max_ammo
    score_manager.reset_score()

    # Create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data



class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        super().__init__()      # Initialize the Sprite class
        # Sprite
        self.alive = True       # Player's alive status
        self.last_hit_time = 0
        self.char_type = char_type      # Type of character (player/enemy)
        self.speed = speed      # Movement speed of the player
        self.shoot_cooldown = 0
        self.health = 10
        self.max_health = self.health
        self.invincible = False  # Invincibility status
        self.invincible_timer = 0  # Duration of invincibility
        self.flicker_timer = 0  # Timer for controlling the flicker effect
        self.flicker_interval = 6  # How many frames to flicker
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0     # Current action (e.g., idle, run)
        self.update_time = pygame.time.get_ticks()

        #ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0
        self.jump_handler = Jump()

        # Gun variable regarding the player
        self.normal_gun_cooldown = 0  # Cooldown timer for normal gun
        shooting = False  # To keep track if the player is holding down the shoot button

        # Ammo and Reload/ Auto Reload Time
        self.normal_ammo = ammo  # Ammo for the normal gun
        self.reload_time_normal = 180  # Reload time for normal gun (3 seconds)
        self.last_shot_time = 0  # Track time of last shot
        self.auto_reload_timer = 0  # Timer for auto-reloading
        
        # Cooldown and Shooting Interval
        self.normal_gun_shoot_interval = 30  # Interval for normal gun (0.5 seconds)
        self.reload_cooldown_normal = 0  # Cooldown for normal gun reloading
        
        # Scoring system
        self.points = 0  # Player's score
        self.font = pygame.font.SysFont('Futura', 36)  # Set font for score display

        # New attributes for auto-reloading
        self.last_shot_time = 0  # Track time of last shot
        self.auto_reload_timer = 0  # Timer for auto-reloading
        
        # Load images for animations
        self.load_animations(scale)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def load_animations(self, scale):
        """ Load animation frames for the character. """
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'asset/img/animation/{self.char_type}/{animation}'))        # Count frames in the directory
            for i in range(num_of_frames):
                img = pygame.image.load(f'asset/img/animation/{self.char_type}/{animation}/{i}.png').convert_alpha()       # Load image
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))       # Scale image
                temp_list.append(img)   # Append the image to the temporary list
            self.animation_list.append(temp_list)       # Add animation frames to the main list

    def update(self):
        """ Update player state each frame. """
        self.reload()  # Reload ammunition
        self.check_invincibility()  # Check if player is invincible
        self.update_animation()
        self.check_alive()

        # Update cooldowns
        if self.normal_gun_cooldown > 0:
            self.normal_gun_cooldown -= 1

        # Handle aiming and shooting "
        mouse_pos = pygame.mouse.get_pos()  # Get mouse position
        if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
            self.shoot(mouse_pos)  # Shoot towards mouse position    
            self.last_shot_time = pygame.time.get_ticks()  # Update last shot time
            self.auto_reload_timer = 0  # Reset auto reload timer when shooting
        else:
            # Increment the auto-reload timer if not shooting
            self.auto_reload_timer += 1
            
            # Check if 2 seconds have passed (assuming 60 FPS, so 120 frames)
            if self.auto_reload_timer >= AUTO_RELOAD_TIME:
                self.reload()  # Auto-reload if no shooting for 2 seconds

        # Update guns
        self.gun.reload()

    def aim(self, mouse_pos):
        self.gun.update(mouse_pos, self.position)  # Update gun aiming

    def calculate_angle(self, target):
        """ Calculate the angle between the player and the target. """
        dx = target[0] - self.rect.centerx  # Change in x
        dy = target[1] - self.rect.centery  # Change in y
        return math.atan2(dy, dx)  # Returns angle in radians

    def move(self, moving_left, moving_right, platform_rects):
        """ Handle player movement based on input. """
        screen_scroll = 0
        level_complete = False
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed    # Move left
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed     # Move right
            self.flip = False
            self.direction = 1

        # Jump logic 
        if self.jump and not self.in_air:
            self.jump_handler.jump()  # Trigger jump action
            self.jump = False  

        # Apply gravity
        self.jump_handler.apply_gravity()
        self.jump_handler.update(self.rect)

        # Check platform collisions
       # Check for platform collisions, etc.
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0
                self.in_air = False

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # Handle screen scroll if player reaches screen edge
        if self.rect.right > SCREEN_WIDTH - SCROLL_THRESH or self.rect.left < SCROLL_THRESH:
            screen_scroll = -dx  # Update screen_scroll
            
        return screen_scroll, level_complete
    
    def shoot(self, target_pos):
        """ Handle shooting logic. """
        if self.gun.ammo > 0:
            if self.normal_gun_cooldown <= 0 and self.gun.ammo > 0:
                self.create_bullet(target_pos)
                self.gun.shoot(self.rect.center) 
                self.normal_gun_cooldown = self.normal_gun_shoot_interval  # Reset cooldown
                shot_fx.play()
        
    def create_bullet(self, target_pos):
        """ Create a bullet based on the target position and type (normal/blast). """
        angle = self.calculate_angle(target_pos)  # Calculate the angle to shoot
        bullet = Bullet(self.rect.center, angle)  # Create bullet instance
        bullet_group.add(bullet)  # Add bullet to the bullet group

    def reload(self):
        """ Handle reloading logic for both guns. """
        if self.normal_ammo < 10 and self.auto_reload_timer >= AUTO_RELOAD_TIME:  # Only reload if not shooting
            self.normal_ammo += 1  # Reload normal ammo automatically
            if self.normal_ammo > 10:  # Cap ammo at max (10)
                self.normal_ammo = 10
                reload_fx.play()

    def take_damage(self, amount):
        """ Reduce health when taking damage. """
        if not self.invincible:  # Only take damage if not invincible
            self.health -= amount  # Decrease health by damage amount
            self.invincible = True  # Set invincible status
            self.invincible_timer = 180  # Start invincibility timer (3 seconds)
            self.flicker_timer = 0  # Reset flicker timer
            if self.health <= 0:
                self.alive = False  # Mark player as dead if health is 0

    def check_invincibility(self):
        """ Manage invincibility status and timer. """
        if self.invincible:
            self.invincible_timer -= 1  # Decrease invincibility timer
            self.flicker_timer += 1
            if self.invincible_timer <= 0:
                self.invincible = False  # End invincibility
                self.flicker_timer = 0

    def collect_health(self, amount):
        self.score += 50  # Earn 50 points for collecting health
        self.health = min(self.max_health, self.health + amount)  # Cap health at max (10)  # Heal but not exceed max health
       
    
    def add_score(self, points):
        self.score += points  # Add points to score

    def display_score(self, screen):
        score_str = f"{self.score:05d}"
        score_surface = self.font.render(score_str, True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))  # Position score on the top-left
        
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)


    def update_animation(self):
        dx = 0
        dy = 0
        screen_scroll = 0
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

        #check for collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                dy = 0
                #if the ai has hit a wall then make it turn around
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom


        #check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        #check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        #check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0


        #check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def update_action(self, new_action):
		#check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            
    def draw(self):
           # Only draw the player if not invincible or if flicker_timer is even (for flickering effect)
        if not self.invincible or (self.flicker_timer // self.flicker_interval) % 2 == 0:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
class Jump:
    def __init__(self):
        self.vel_y = 0
        self.in_air = True
        self.jump_buffer = False  # To handle jump buffering
        self.coyote_time = 0  # Coyote time counter
        self.coyote_time_limit = 10  # Frames to allow jumping after leaving a platform

    def jump(self):
        if not self.in_air or self.coyote_time > 0:
            self.vel_y = -11  # Jump strength
            self.in_air = True
            self.coyote_time = 0  # Reset coyote time on jump
        else:
            self.jump_buffer = True  # Buffer the jump if not allowed

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > 10:  # Terminal velocity
            self.vel_y = 10

    def update(self, rect):
        rect.y += self.vel_y
        if rect.bottom >= SCREEN_HEIGHT:
            rect.bottom = SCREEN_HEIGHT
            self.in_air = False
            self.vel_y = 0
            self.coyote_time = self.coyote_time_limit  # Start coyote time when landing
        else:
            self.coyote_time -= 1 if self.coyote_time > 0 else 0

        # Handle jump buffering
        if self.jump_buffer and self.coyote_time > 0:
            self.jump()
            self.jump_buffer = False  # Reset buffer after jumping

    def check_collision(self, rect, platform_rects):
        # Check if the player is colliding with a platform
        for platform in platform_rects:
            if rect.colliderect(platform):
                if self.vel_y >= 0:  # Only consider landing if falling
                    rect.bottom = platform.top  # Land on platform
                    self.in_air = False
                    self.vel_y = 0
                    self.coyote_time = self.coyote_time_limit  # Reset coyote time
                else:
                    # If moving up or horizontally, ignore collision
                    rect.y -= self.vel_y
                return


class Bullet(pygame.sprite.Sprite):
    "Projectile"
    def __init__(self, start_pos, angle, speed=10, range=800):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = speed
        self.range = range  # Distance it can travel
        self.distance_travelled = 0
        self.angle = angle  # Angle for movement
        self.damage = 2.5

    def update(self):
        # Move the bullet in the direction of the angle
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)
        self.distance_travelled += self.speed

         # Check for collision with enemies
        for enemy in enemy_group:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(self.damage)
                self.kill()  # Destroy the bullet on impact
        # Check if the bullet has exceeded its range
        if self.distance_travelled > self.range:
            self.kill()  # Remove the bullet if it goes out of range

class Gun:
    def __init__(self):
        self.angle = 0
        self.ammo = 10  # For normal gun
        self.max_ammo = 10
        self.reload_time = 3000  # 3 seconds reload time
        self.last_shot_time = 0
        self.is_reloading = False
        self.auto_reload_time = 2000  # Auto reload after 2 seconds of inactivity
        self.can_shoot = True
        self.cooldown_time = 500

        # No-reload attributes
        self.no_reload_active = False
        self.no_reload_timer = 0  # Countdown for no-reload period
 
    # # Load SFX placeholders
        # self.shoot_sfx = mixer.Sound('assets/sounds/shoot.wav')  # Placeholder for shooting SFX
        # self.reload_sfx = mixer.Sound('assets/sounds/reload.wav')  # Placeholder for reload SFX

    def update(self, mouse_pos, player_pos):
        rel_x, rel_y = mouse_pos[0] - player_pos[0], mouse_pos[1] - player_pos[1]
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        # Auto reload logic
        if not self.is_reloading and self.ammo < self.max_ammo and pygame.time.get_ticks() - self.last_shot_time > self.auto_reload_time:
            self.ammo += 1
            if self.ammo >= 10:
                self.ammo = 10
           
        # Handle the no-reload timer
        if self.no_reload_active:
            if pygame.time.get_ticks() - self.no_reload_timer >= 10000:  # 10 seconds
                self.no_reload_active = False

          # Handle reloading if out of ammo
        if self.is_reloading and pygame.time.get_ticks() - self.last_shot_time >= self.reload_time:
            self.ammo = self.max_ammo  # Refill ammo
            self.is_reloading = False

        # Handle cooldown between shots
        if not self.is_reloading and not self.can_shoot and pygame.time.get_ticks() - self.last_shot_time > self.cooldown_time:
            self.can_shoot = True

    def shoot(self, player_pos, mouse_pos):
        # Shooting logic: if the gun has ammo and isn't reloading or cooling down
         if self.can_shoot and not self.is_reloading and self.ammo > 0:
            self.ammo -= 1
            self.last_shot_time = pygame.time.get_ticks()
            self.can_shoot = False  # Prevent shooting until cooldown is over

            # Calculate direction and offset bullet start from gun's position (player's position + offset)
            offset_distance = 20  # Gun's offset distance from the player
            bullet_start_x = player_pos[0] + offset_distance * math.cos(self.angle * math.pi / 180)
            bullet_start_y = player_pos[1] + offset_distance * math.sin(self.angle * math.pi / 180)
            bullet_start_pos = (bullet_start_x, bullet_start_y)

            # Calculate angle to shoot towards the mouse
            angle = math.atan2(mouse_pos[1] - bullet_start_y, mouse_pos[0] - bullet_start_x)

            # Create the bullet and add to the bullet group
            bullet = Bullet(bullet_start_pos, angle)
            bullet_group.add(bullet)

            # Start reload if ammo is 0
            if self.ammo == 0:
                self.is_reloading = True
                self.last_shot_time = pygame.time.get_ticks()  
                reload_fx.play()

    def reload(self):
        """Reload the gun after a specified time."""
        if self.is_reloading:
            if pygame.time.get_ticks() - self.last_shot_time >= self.reload_time:
                self.ammo = self.max_ammo
                self.is_reloading = False
                reload_fx.play()

    def activate_no_reload(self):
        """Activate no-reload mode for 10 seconds."""
        self.no_reload_active = True
        self.no_reload_timer = pygame.time.get_ticks()  # Start the 10-second countdown

    def draw(self, screen, player_pos, mouse_pos):
        # Calculate direction vector to the mouse
        rel_x, rel_y = mouse_pos[0] - player_pos[0], mouse_pos[1] - player_pos[1]
        angle = math.atan2(rel_y, rel_x)

        # Offset the visual (square or circle) a little away from the player
        offset_distance = 20  # Distance from player
        offset_x = player_pos[0] + offset_distance * math.cos(angle)
        offset_y = player_pos[1] + offset_distance * math.sin(angle)

        # Draw square for normal gun
        pygame.draw.rect(screen, RED, (offset_x - 10, offset_y - 5, 20, 10))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed, health, detection_range=150):
        super().__init__()
        self.char_type = char_type
        self.speed = speed
        self.health = health
        self.max_health = health
        self.previous_health = health  # Add previous_health attribute
        self.alive = True
        self.direction = 1  # Default direction to the right
        self.detection_range = detection_range
        self.image = pygame.Surface((50, 50))  # Placeholder for enemy image
        self.image.fill((255, 0, 0))  # Red color for placeholder
        self.rect = self.image.get_rect(center=(x, y))
        self.vision = pygame.Rect(0, 0, 150, 20)  # Vision rectangle for AI
        self.idling = False
        self.idling_counter = 0
        self.move_counter = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.animation_list = []  # Add animations if necessary
        self.move_function = self.walk

         # Create a slim health bar for this enemy
        self.health_bar = HealthBar(self.rect.x, self.rect.y - 10, self.health, self.max_health, width=40, height=5)

    def load_animations(self, scale):
        """ Load animation frames for the character. """
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'asset/img/animation/{self.char_type}/{animation}'))        # Count frames in the directory
            for i in range(num_of_frames):
                img = pygame.image.load(f'asset/img/animation/{self.char_type}/{animation}/{i}.png').convert_alpha()       # Load image
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))       # Scale image
                temp_list.append(img)   # Append the image to the temporary list
            self.animation_list.append(temp_list)       # Add animation frames to the main list

    def ai(self, player):
        """AI behavior for the enemy."""
        if self.alive and player.alive:
            if not self.idling and random.randint(1, 200) == 1:
                self.update_action(0)  # Idle action
                self.idling = True
                self.idling_counter = 50

            if self.vision.colliderect(player.rect):
                self.update_action(0)  # Idle action
                self.attack(player)  # Attack the player
            else:
                if not self.idling:
                    self.move()
                    self.update_action(1)  # Run action
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
    
    def update_action(self, new_action):
		#check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def patrol(self):
        """Enemy patrols within its designated area."""
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.patrol_area) > TILE_SIZE:  # Patrol in a small area
            self.direction *= -1

    def attack(self, player):
        if self.char_type == "flying":
            # Flying enemy attacks
            player.take_damage(1)
        elif self.char_type == "normal":
            player.take_damage(1)

    def move(self):
        "General move function to be called by all enemies"
        self.move_function()

    def walk(self):
        "Ground movement behavior for normal enemies."
        self.rect.x += self.speed * self.direction
        # Reverses direction if hitting screen boundaries
        if self.rect.x < 100 or self.rect.x > SCREEN_WIDTH - 100:
            self.direction *= -1    
    
    def fly(self):
        "Flying movement behavior."
        self.rect.x += self.speed * self.direction
        self.rect.y += math.sin(pygame.time.get_ticks() / 1000) * 5  # Smooth vertical flying motion
        # Reverse direction when flying out of bounds
        if self.rect.x < 50 or self.rect.x > SCREEN_WIDTH - 50:
            self.direction *= -1    

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(3)  # Death animation

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def take_damage(self, amount):
        self.previous_health = self.health  # Store current health as previous health
        self.health -= amount
        if self.previous_health > self.health: 
            score_manager.add_points(10 * (self.previous_health - self.health))
            boss_hit_fx()
        global score  # Access the global score variable
        score += 10  # Earn 10 points for each health point deducted
        if self.health <= 0:
            self.check_alive()  # Check if the enemy is dead

    def update(self, player):
        """Update enemy logic."""
        if self.alive:
            self.move_function()  # Call move behavior (either fly or walk)
            self.ai(player)
            self.health_bar.draw(self.health)
        else:
            self.kill()  # Remove from the game if dead

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.direction == -1, False), self.rect)
        if self.alive:
            self.health_bar.draw(screen, self.health, self.rect.centerx - 20, self.rect.y - 10)  # Adjust x, y as needed

class FlyingEnemy(Enemy):
    def __init__(self, x, y, speed=3, health=5):
        super().__init__()
        self.move_function = self.fly
        self.char_type = 'flying_enemy'
        self.speed = speed
        self.health = health
        self.max_health = health
        self.direction = 1  # Start moving to the right
        self.alive = True
        self.attack_mode = False  # Whether the enemy is currently attacking
        self.start_pos = (x, y)  # The original patrol position (to return after attacking)
        self.target_reached = False  # Tracks if it has returned to patrol after attacking
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: Idle, 1: Flying, 2: Death
        self.update_time = pygame.time.get_ticks()

        self.load_animations(1.5)  # Load flying animations with scaling factor
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        self.move_counter = 0  # Used for patrolling

    def load_animations(self, scale):
        animation_types = ['Fly', 'Attack', 'Hit']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'asset/img/animation/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'asset/img/enemies/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

    def take_damage(self, amount):
        """Override take_damage to trigger the GetHit animation."""
        self.health -= amount
        if self.health <= 0:
            self.alive = False  # Enemy dies
            self.update_action(2)  # Trigger the 'GetHit' animation for death
        else:
            self.update_action(2)  # Trigger the 'GetHit' animation when damaged
            self.hit_time = pygame.time.get_ticks()  # Record the time the enemy got hit

    def update(self, player):
            """Update the flying enemy state each frame."""
            if self.alive:
                # If enemy is hit, switch back to patrol/attack after the GetHit animation finishes
                if self.action == 2 and pygame.time.get_ticks() - self.hit_time > 300:  # Play 'GetHit' for 300 ms
                    self.update_action(0 if not self.vision.colliderect(player.rect) else 1)  # Resume patrol or attack
                else:
                    self.ai(player)  # Handle AI behavior (patrolling, attacking, etc.)
                
                self.update_animation()  # Handle animations based on current action
            else:
                self.update_action(2)  # Trigger the 'GetHit' animation if the enemy is dead
    
    def fly(self):
        """Custom flying behavior."""
        if not self.attack_mode:
            self.rect.x += self.speed * self.direction
            if self.rect.x < 50 or self.rect.x > SCREEN_WIDTH - 50:
                self.direction *= -1  # Reverse direction at screen edges

    def ai(self, player):
        """Handle AI behavior: attack the player and return to patrol after."""
        if self.alive and player.alive:
            if self.attack_mode:
                self.fly_towards_player(player)
            elif self.target_reached:
                # When attack finishes, return to patrol position
                self.fly_back_to_position()
            elif self.vision.colliderect(player.rect):
                # If the player is detected in the vision, start attack
                self.update_action(1)  # Attack action
                self.attack_mode = True  # Enable attack mode
            else:
                self.fly()  # Patrol when not attacking or returning to position

    def fly_towards_player(self, player):
        # Calculate the distance from the starting position
        distance_from_start = abs(self.rect.x - self.start_pos[0]) + abs(self.rect.y - self.start_pos[1])

        if distance_from_start > self.detection_range:
            # If too far from start, return to patrol
            self.target_reached = True
            self.attack_mode = False
            self.update_action(0)  # Return to patrol state
        else:
            # Charge towards the player's position
            if player.rect.x > self.rect.x:
                self.direction = 1
            else:
                self.direction = -1
            self.rect.x += self.speed * self.direction
            self.rect.y += self.speed * (-1 if player.rect.y < self.rect.y else 1)  # Charge vertically

            # Check if enemy reaches player's x-coordinate
            if abs(self.rect.x - player.rect.x) < 5:  # Tolerance for "hitting" the player
                self.attack(player)
                self.target_reached = True  # Mark target as reached (whether hit or missed)

    def fly_back_to_position(self):
        """Return to the original patrol position after attacking."""
        # Move back to the starting patrol position
        if abs(self.rect.x - self.start_pos[0]) > 5 or abs(self.rect.y - self.start_pos[1]) > 5:
            if self.rect.x < self.start_pos[0]:
                self.direction = 1
            else:
                self.direction = -1
            self.rect.x += self.speed * self.direction
            self.rect.y += self.speed * (1 if self.rect.y < self.start_pos[1] else -1)
        else:
            # Once back to the original position, resume patrol
            self.target_reached = False
            self.attack_mode = False
            self.update_action(0)  # Switch back to patrol action

    def update_animation(self):
            """Update the flying enemy animation frame."""
            self.image = self.animation_list[self.action][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > 100:  # Adjust the frame rate
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 2:  # GetHit animation plays once
                    self.frame_index = len(self.animation_list[self.action]) - 1  # Freeze on last frame
                else:
                    self.frame_index = 0  # Loop animation for Patrol and Attack

    def update_action(self, new_action):
        """Change the current action and reset animation frame."""
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def attack(self, player):
        player.take_damage(1)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
     

class NormalEnemy(Enemy):
    def __init__(self, x, y, speed=2, health=4):
        super().__init__('enemy', x, y, speed, health)

    def move(self):
        if not self.idling:
            self.rect.x += self.direction * self.speed
            if self.rect.x < 100 or self.rect.x > SCREEN_WIDTH - 100:  # Example boundaries
                self.direction *= -1

    def attack(self, player):
        player.take_damage(1)
    
class Scoring:
    def __init__(self):
        self.score = 0
        self.checkpoint_score = 0  # This will store the score at the start of each level
        self.font = pygame.font.SysFont('Comic Sans MS', 36)  # Set font for score display

    def add_points(self, points):
        """Add points to the score."""
        self.score += points

    def save_checkpoint_score(self):
        """Save the current score as the checkpoint (when starting a new level)."""
        self.checkpoint_score = self.score

    def reset_to_checkpoint(self):
        """Reset the score to the last saved checkpoint (when the player dies but restarts the current level)."""
        self.score = self.checkpoint_score

    def reset_score(self):
        """Reset the score to zero."""
        self.score = 0
        self.checkpoint_score = 0

    def display_score(self, screen):
        """Display the current score on the screen."""
        score_str = f"{self.score:06d}"  # Format score to 6 digits with leading zeros
        score_surface = self.font.render(score_str, True, (255, 255, 255))  # White color
        screen.blit(score_surface, (10, 10))  # Position score on the screen

    def save_score(self, filename):
        """Save the current score to a file."""
        with open(filename, 'w') as f:
            json.dump({'score': self.score}, f)

    def load_score(self, filename):
        """Load the score from a file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.score = data.get('score', 0)
        except FileNotFoundError:
            self.score = 0  # If file doesn't exist, start with 0

score_manager = Scoring()


class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, direction, speed, center_x=None, center_y=None, radius=100):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = direction
        self.speed = speed
        self.angle = 0  # For circular motion

        # If center_x or center_y is not provided, use the platform's initial position as the center
        self.center_x = center_x if center_x is not None else x
        self.center_y = center_y if center_y is not None else y
        self.radius = radius  # Radius of the circular movement

    def update(self):
        if self.direction == 'horizontal':
            self.rect.x += self.speed
            if self.rect.x > 800 or self.rect.x < 0:  # Change direction on screen edges
                self.speed = -self.speed
        elif self.direction == 'vertical':
            self.rect.y += self.speed
            if self.rect.y > 600 or self.rect.y < 0:
                self.speed = -self.speed
        elif self.direction == 'circular':
            self.angle += self.speed  # Increase the angle over time to create circular movement
            if self.angle >= 360:
                self.angle = 0  # Reset angle to avoid overflow
            
            # Calculate new position based on the circular path around center_x, center_y
            self.rect.x = self.center_x + self.radius * math.cos(math.radians(self.angle)) - self.rect.width // 2
            self.rect.y = self.center_y + self.radius * math.sin(math.radians(self.angle)) - self.rect.height // 2

    def reset(self):
        """Reset the platform to its original position."""
        self.angle = 0  # Reset angle for circular motion
        self.rect.x = self.center_x - self.radius  # Reset position based on initial radius
        self.rect.y = self.center_y

class ScreenFade():
	def __init__(self, direction, colour, speed):
		self.direction = direction
		self.colour = colour
		self.speed = speed
		self.fade_counter = 0
		self.player = None  # Player will be assigned later

	def set_player(self, player):
		self.player = player

	def fade(self):
		fade_complete = False
		self.fade_counter += self.speed
		if self.direction == 1:# whole screen fade
			pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
			pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
			pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
		if self.direction == 2: # Circle wipe based on player's location
			# Get the player's center position for the circle's center
			player_center = self.player.rect.center
            # Draw the circle, growing in radius each frame
			pygame.draw.circle(screen, self.colour, player_center, self.fade_counter)

		if self.direction == 1 and self.fade_counter >= SCREEN_WIDTH:
			fade_complete = True
		elif self.direction == 2 and self.fade_counter >= max(SCREEN_WIDTH, SCREEN_HEIGHT):
			fade_complete = True  # Complete the circle wipe when it fills the screen

		return fade_complete
     
def draw_crosshair(screen, player_pos, mouse_pos):
    outer_circle_color = GREEN  # Green for outer circle
    inner_circle_color = RED  # Red for inner circle (aim indicator)

    # Define circle sizes
    outer_circle_radius = 50  # Outer circle radius around the player
    inner_circle_radius = 70  # Inner circle radius (aim indicator)

    # Draw the outer circle fixed around the player
    pygame.draw.circle(screen, outer_circle_color, player_pos, outer_circle_radius, 2)  # Green outer circle

    # Draw the inner circle on the mouse position (aim indicator)
    pygame.draw.circle(screen, inner_circle_color, mouse_pos, inner_circle_radius)  # Red circle follows mouse

def display_ammo(screen, normal_ammo, blast_ammo):
		font = pygame.font.SysFont('Montserrat', 30)
		ammo_text = font.render(f'Ammo: {normal_ammo}/{blast_ammo}', True, (255, 255, 255))
		screen.blit(ammo_text, (10, 50))

class HealthBar():
    def __init__(self, x, y, health, max_health, width=40, height=5):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        self.width = width  # Add width for flexibility
        self.height = height  # Add height for flexibility

    def draw(self, health):
        #update with new health
        self.health = health
        #calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


    def display_health(screen, health):
        font = pygame.font.SysFont('Futura', 30)
        health_text = font.render(f'Health: {health}', True, (255, 255, 255))
        screen.blit(health_text, (10, 10))

	
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, collectible_type="default"):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        
        img = pygame.image.load('img/icons/Coin.png').convert_alpha()  # Load your collectible images here
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.images.append(img)

        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        self.collected = False
        self.collectible_type = collectible_type  # Example collectible type, in case you have multiple types (e.g., health, score)

    def update(self, player):
        """ Update collectible status and check for collision with player. """
        # Move collectible with screen scroll if applicable
        self.rect.x += screen_scroll

        # Check if the player collides with the collectible
        if pygame.sprite.collide_rect(self, player):
            self.collect(player)
            shot_fx.play()  # Placeholder for item collection sound

    def collect(self, player):
        """ Handle the logic when the player collects the item. """
        global score_manager
        if self.collectible_type == "score":
            score_manager.add_points(50)  # Award 50 points for collecting
        elif self.collectible_type == "health":
            player.collect_health(10)  # Heal the player
            score_manager.add_points(50)  # Optionally award points for health collectibles

        # Mark the collectible as collected and remove from the game
        self.collected = True
        self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += screen_scroll  # Make sure walls move with the screen scroll

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])

        # Iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)

                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10 or tile in range(95,99):
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  # Create player
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:  # Create enemies
                        enemy = NormalEnemy(x * TILE_SIZE, y * TILE_SIZE, 1.65, 15)
                        enemy_group.add(enemy)
                    elif tile == 17:  # Create ammo box
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile in range(11, 15) or tile in range(40, 46):  # Create coin box
                        item_box = ItemBox('Coin', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:  # Create health box
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20 or 116:  # Create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 78 or 115:  # Horizontal moving platform
                        platform = MovingPlatform(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE * 2, TILE_SIZE // 2, 'horizontal', 2)
                        platform_group.add(platform)
                    elif tile == 113 or 112:  # Vertical moving platform
                        platform = MovingPlatform(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE * 2, TILE_SIZE // 2, 'vertical', 2)
                        platform_group.add(platform)
                    elif tile == 24:  # Circular moving platform
                        platform = MovingPlatform(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE * 2, TILE_SIZE // 2, 'circular', 2, center_x=(x+1)* TILE_SIZE, center_y=(y+1)* TILE_SIZE, radius=2 * TILE_SIZE)
                        platform_group.add(platform)
                    elif tile == 30:  # Create wall
                        wall = Wall(img, x * TILE_SIZE, y * TILE_SIZE)
                        wall_group.add(wall)    
                    elif tile == 105:  # Create boss
                        boss = Boss(x * TILE_SIZE, y * TILE_SIZE, 3, 50)  
                        boss_group.add(boss)
                    elif tile == 101:  # Create flying enemy
                        flying_enemy = FlyingEnemy(x * TILE_SIZE, y * TILE_SIZE, speed=1.5, health=10)  
                        enemy_group.add(flying_enemy)    

        return player, health_bar, platform_group, wall_group, boss_group



    def draw(self):
        for tile in self.obstacle_list:
            tile_rect = tile[1].copy()  # Copy the tile's rect to avoid modifying the original rect
            tile_rect.x += screen_scroll  # Apply screen scroll only for drawing purposes
            screen.blit(tile[0], tile_rect)  # Draw the tile at the updated position


class Decoration(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        # Scroll
        self.rect.x += screen_scroll
        # Check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            # Check what kind of box it was
            if self.item_type == 'Health':
                player.health += 5
                score_manager.add_points(50)  # Add points
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.gun.activate_no_reload()  # Activate 10s of no reload
                score_manager.add_points(25)  # Give 25 points
            elif self.item_type == 'Coin':
                score_manager.add_points(50)
            
            # Delete the item box
            self.kill()



#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

#create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
collectible_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()

#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
player, health_bar, platform_group, wall_group, boss_group = world.process_data(world_data)

moving_platform_horizontal = MovingPlatform(x=100, y=300, width=100, height=20, direction='horizontal', speed=2)
moving_platform_vertical = MovingPlatform(x=300, y=200, width=100, height=20, direction='vertical', speed=2)
moving_platform_circular = MovingPlatform(x=400, y=300, width=20, height=20, direction='circular', speed=2)
platforms_group = pygame.sprite.Group(moving_platform_horizontal, moving_platform_vertical, moving_platform_circular)


class Boss(NormalEnemy):
    def __init__(self, x, y, speed=3, health=30):
        super().__init__(x, y, speed, health)
        self.image = pygame.image.load('asset/img/icons/boss.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE * 4, TILE_SIZE * 4))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.health = health
        self.max_health = health
        self.health_bar = None  # Remove the health bar from the enemy display

        # Animation attributes
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # The current action (e.g., 0 for move)
        self.update_time = pygame.time.get_ticks()
        # Load the boss animations
        self.load_animations()

        #Variable for phase 1
        self.phase = 1   # Boss phases to change behavior
        self.charging_speed = 0  # Track the current speed when charging
        self.max_charging_speed = 8  # Max speed while charging
        self.acceleration = 0.2  # Acceleration rate while charging
        self.deceleration = 0.3  # Deceleration rate when the player is behind
        self.charging = False  # Flag to check if the boss is currently charging
        
        #Variable for phase 2
        self.has_shield = False
        self.shield_angle = 0
        self.projectile_timer = 0  # Timer to control shooting projectiles
        self.platform = None  # To reference the moving platform in phase 2
        self.shield_radius = 50  # Distance from the boss to the shield
        self.projectile_group = pygame.sprite.Group()

        # Platform teleporting attributes for phase 2
        self.current_platform = None
        self.platform_switch_timer = 0

    def draw_health_bar_on_top(self, screen):
        """Draw the boss health bar at the top of the screen."""
        bar_length = 300
        bar_height = 20
        fill = (self.health / self.max_health) * bar_length

        # Background for health bar
        pygame.draw.rect(screen, (0, 0, 0), (screen.get_width() // 2 - bar_length // 2, 20, bar_length, bar_height))
        # Health bar (filled part)
        pygame.draw.rect(screen, BLUE, (screen.get_width() // 2 - bar_length // 2, 20, bar_length, bar_height))
        pygame.draw.rect(screen, RED, (screen.get_width() // 2 - bar_length // 2, 20, fill, bar_height))

    def load_animations(self):
        """Load the boss animation frames into animation_list"""
        animation_types = ['Move']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'asset/img/animation/boss/{animation}'))  # Assuming your frames are stored in a folder
            for i in range(num_of_frames):
                img = pygame.image.load(f'asset/img/animation/boss/{animation}/{i}.png').convert_alpha()
                temp_list.append(img)
            self.animation_list.append(temp_list)

        # Set the initial image for the boss from the first frame of the move animation
        self.image = self.animation_list[self.action][self.frame_index]

    def update_animation(self):
        """Update the boss animation frame based on the current action."""
        # Update image to the next frame
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > 100:  # Adjust frame rate (100 ms per frame)
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # Loop the animation
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update(self, player, platform):
        """Handles boss behavior, including phase transitions."""
        if self.health <= self.max_health // 2 and self.phase == 1:
            self.enter_phase_two(platform)

        if self.phase == 1:
            self.charge_at_player(player)
        elif self.phase == 2:
            self.switch_platform_if_needed(platform_group)
            self.stand_on_platform()
            self.spin_shield()
            self.shoot_projectiles_from_shield()

        # Update animations
        self.update_animation()

        super().update(player)

    def enter_phase_two(self, platform_group):
        """Transition to phase 2: Boss moves to the platform and activates a shield."""
        self.phase = 2
        self.has_shield = True  # Activate shield in phase 2

        # The boss starts on one of the two moving platforms
        moving_platforms = [platform for platform in platform_group if isinstance(platform, MovingPlatform)]
        if moving_platforms:
            self.current_platform = random.choice(moving_platforms)
            self.rect.centerx = self.current_platform.rect.centerx
            self.rect.bottom = self.current_platform.rect.top
            self.platform_switch_timer = pygame.time.get_ticks()  # Start the timer for platform switching

    def stand_on_platform(self):
        """Boss stays on the moving platform in phase 2."""
        if self.phase == 2 and self.current_platform:
            # Make sure the boss moves with the current platform horizontally
            self.rect.x = self.current_platform.rect.x
            self.rect.bottom = self.current_platform.rect.top

            # Detect platform collision with walls and reverse direction if needed
            if pygame.sprite.spritecollide(self.current_platform, wall_group, False):
                self.current_platform.speed = -self.current_platform.speed  # Reverse platform direction on collision
        
    def switch_platform_if_needed(self, platform_group):
        """Switch the boss's position between the two platforms after 5 seconds."""
        # If the boss has been on the current platform for 5 seconds, teleport to the other platform
        if pygame.time.get_ticks() - self.platform_switch_timer > 6000:  # 5 seconds
            moving_platforms = [platform for platform in platform_group if isinstance(platform, MovingPlatform)]
            if moving_platforms:
                other_platforms = [p for p in moving_platforms if p != self.current_platform]
                if other_platforms:
                    new_platform = random.choice(other_platforms)
                    self.rect.centerx = new_platform.rect.centerx
                    self.rect.bottom = new_platform.rect.top
                    self.current_platform = new_platform
                    self.platform_switch_timer = pygame.time.get_ticks()  # Reset the timer

    def charge_at_player(self, player, platform_group):
        """Boss gradually charges towards the player with increasing speed in phase 1."""
        # Determine direction based on the player's position
        # Boss will only charge if the player is on the same platform or ground
        player_on_ground = player.rect.bottom >= SCREEN_HEIGHT - TILE_SIZE

        if player_on_same_platform or player_on_ground:
            # Determine direction based on the player's position
            if player.rect.x < self.rect.x:
                self.direction = -1  # Move left
            else:
                self.direction = 1  # Move right
        
        player_on_same_platform = False
        for platform in platform_group:
            if platform.rect.colliderect(player.rect) and platform.rect.colliderect(self.rect):
                player_on_same_platform = True
        # Check if the player is in front of the boss
        player_in_front = (player.rect.x < self.rect.x and self.direction == -1) or \
                          (player.rect.x > self.rect.x and self.direction == 1)
        
        # If the player is in front, accelerate towards them
        if player_in_front:
            self.charging = True
            if self.charging_speed < self.max_charging_speed:
                self.charging_speed += self.acceleration  # Gradually increase speed

            # Move towards the player
            self.rect.x += self.charging_speed * self.direction
        else:
            # If the player is behind the boss, decelerate or stop
            self.charging = False
            if self.charging_speed > 0:
                self.charging_speed -= self.deceleration  # Gradually slow down
            else:
                self.charging_speed = 0  # Stop when speed reaches 0

        # Check for collisions with walls
        wall_hit_list = pygame.sprite.spritecollide(self, wall_group, False)
        if wall_hit_list:
            self.charging_speed = 0  # Stop the boss if it hits a wall
    
    def spin_shield(self):
        """Spins the shield around the boss during phase 2."""
        self.shield_angle += 5  # Adjust the shield angle each frame
        if self.shield_angle >= 360:
            self.shield_angle -= 360

    def shoot_projectiles_from_shield(self):
        """Shoots projectiles from the shield at the current shield angle."""
        self.shield_projectile_timer += 1
        if self.shield_projectile_timer > 30:  # Shoot every half a second (30 frames at 60 FPS)
            self.shield_projectile_timer = 0
            num_projectiles = random.randint(2, 8)  # Shoot between 3 to 6 projectiles

            for _ in range(num_projectiles):
                self.create_shield_projectile()

        # Update and draw projectiles
        self.projectile_group.update()


    def create_shield_projectile(self):
        """Create a projectile shot from the shield's current position."""
        shield_radius = 50
        # Calculate projectile's starting point based on shield's current angle
        projectile_x = self.rect.centerx + shield_radius * math.cos(math.radians(self.shield_angle))
        projectile_y = self.rect.centery + shield_radius * math.sin(math.radians(self.shield_angle))
        angle = math.radians(self.shield_angle)  # The projectile will travel along this angle
        projectile = Projectile(projectile_x, projectile_y, angle)  # Create projectile at shield's position
        self.projectile_group.add(projectile)

    def take_damage(self, amount):
        # Handle damage only if the shield is not active or the boss is in a vulnerable state in phase 2
        if self.phase == 1:
            # In phase 1, the boss can only be damaged if it has no shield
            if not self.has_shield:
                self.health -= amount
            
        elif self.phase == 2:
            # In phase 2, even if the shield is active, you could add conditions for when the shield doesn't block damage
            if not self.has_shield:  # Shield is down
                self.health -= amount
                
            elif self.shield_is_vulnerable():  # Optional condition to make shield occasionally vulnerable
                self.health -= amount
                
        # Check if the boss is dead after taking damage
        if self.health <= 0:
            self.alive = False
        

    def draw_shield(self, screen):
        # Draw the spinning shield around the boss during phase 2
        if self.phase == 2 and self.has_shield:
            shield_radius = 0
            arc_angle_start = self.shield_angle  # Starting angle of the arc
            arc_angle_end = self.shield_angle + 60  # 1/6 of the circle (60 degrees)
       
        # Calculate the arc's points
        shield_center = (self.rect.centerx, self.rect.centery)
        # Draw the arc's border, without filling
        pygame.draw.arc(
            screen,
            BLUE,  
            pygame.Rect(
                shield_center[0] - shield_radius,
                shield_center[1] - shield_radius,
                shield_radius * 2,
                shield_radius * 2
            ),
            math.radians(arc_angle_start),  # Convert start angle to radians
            math.radians(arc_angle_end),  # Convert end angle to radians
            5  # Thickness of the arc's border
        )

    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_health_bar_on_top(screen)

def load_boss_level():
    "Initialize the boss fight level"
    boss = Boss(x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - TILE_SIZE * 4, speed=3, health=30)
    
    # Create the ground (floor tiles) that cover the width of the screen
    ground_tiles = []
    for i in range(0, SCREEN_WIDTH // TILE_SIZE):
        ground_tile = Wall(img_list[31], i * TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE)  # Assuming tile ID 30 is the ground tile
        ground_tiles.append(ground_tile)
        wall_group.add(ground_tile)

    # Create walls on both sides (left and right)
    left_wall = Wall(img_list[30], 0, SCREEN_HEIGHT - TILE_SIZE * 10)
    right_wall = Wall(img_list[30], SCREEN_WIDTH - TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE * 10)
    wall_group.add(left_wall)
    wall_group.add(right_wall)
    
    # Create two stationary platforms in phase 1
    platform_group = pygame.sprite.Group()
    platform1 = Wall(img_list[30], SCREEN_WIDTH // 4 - TILE_SIZE * 2, SCREEN_HEIGHT - TILE_SIZE * 6, TILE_SIZE * 4, TILE_SIZE)  # Left platform
    platform2 = Wall(img_list[30], SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - TILE_SIZE * 6, TILE_SIZE * 4, TILE_SIZE)  # Right platform
    platform_group.add(platform1)
    platform_group.add(platform2)

    return boss, platform_group, wall_group

    

def enter_boss_phase_two(boss, platform_group):
    # Add two vertical platforms on both sides
    moving_platform_left = MovingPlatform(50, SCREEN_HEIGHT - TILE_SIZE * 4, TILE_SIZE * 6, TILE_SIZE * 2, 'vertical', 2)
    moving_platform_right = MovingPlatform(SCREEN_WIDTH - 150, SCREEN_HEIGHT - TILE_SIZE * 4, TILE_SIZE * 6, TILE_SIZE * 2, 'vertical', 2)
    platform_group.add(moving_platform_left)
    platform_group.add(moving_platform_right)
    
    boss.enter_phase_two(platform_group)
    # Activate phase 2 mechanics for the boss
    boss.phase = 2    
    
class Projectile(pygame.sprite.Sprite):
    "Projectile for boss at phase 2"
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = projectile_img
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.angle = angle  # Set the projectile's angle of movement
        
    def update(self):
        """Move the projectile in the direction of its angle."""
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)

        # Destroy the projectile if it goes off the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Initialize boss level
boss, platform_group = load_boss_level()
                                 
def update_boss_level(screen, player, boss, platform_group):
    draw_bg_4()  # Draw the background starting from (0, 0)

    # Draw the ground and walls
    wall_group.draw(screen)

    # Phase 2: Platforms appear
    if boss.phase == 2:
        platform_group.update()
        platform_group.draw(screen)

        # Handle boss shield and projectile logic in phase 2
        boss.spin_shield()  # If spinning shield is part of phase 2
        boss.shoot_projectiles_from_shield()
        boss.projectile_group.update()
        boss.projectile_group.draw(screen)

    # Update and draw boss
    boss.update(player)
    boss.draw(screen)
    boss.draw_health_bar_on_top(screen)
    
    # If the boss enters phase 2, trigger platform spawning
    if boss.health <= boss.max_health // 2 and boss.phase == 1:
        enter_boss_phase_two(boss, platform_group)

    boss.draw_shield(screen)

       
# Create a function to display the end screen after defeating the boss
def display_end_screen(screen, score_manager):
    # Fill the screen with a black background
    screen.blit(bg_end, (0, 0))  # Draw the congrats background

    # Create and display the "Congratulations" message
    font = pygame.font.SysFont('Futura', 60)
    small_font = pygame.font.SysFont('Futura', 40)
    congrats_text = font.render('Congratulations!', True, (255, 255, 255))
    congrats_x = SCREEN_WIDTH // 2 - congrats_text.get_width() // 2
    congrats_y = SCREEN_HEIGHT // 2 - 150
    screen.blit(congrats_text, (congrats_x, congrats_y))

    # Display the final score
    score_font = pygame.font.SysFont('Futura', 40)
    score_text = score_font.render(f'Final Score: {score_manager.score}', True, (255, 255, 255))
    score_x = SCREEN_WIDTH // 2 - score_text.get_width() // 2
    score_y = congrats_y + 80  # Positioned below the "Congratulations" text
    screen.blit(score_text, (score_x, score_y))

    # Display the "Thank You for Playing" message
    thank_you_text = small_font.render('Thank you for playing!', True, (255, 255, 255))
    thank_you_x = SCREEN_WIDTH // 2 - thank_you_text.get_width() // 2
    thank_you_y = score_y + 60  # Positioned below the final score
    screen.blit(thank_you_text, (thank_you_x, thank_you_y))

    # Create buttons for restarting or exiting the game
    restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, restart_img, 1)
    exit_button = button.Button(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 100, exit_img, 1)

    # Draw the buttons on the screen
    if restart_button.draw(screen):
        return 'restart'
    if exit_button.draw(screen):
        return 'exit'
    
    return 'continue'

class ScrollingText:
    def __init__(self, text_list, font, text_color, x, start_y, scroll_speed, screen_width):
        """
        Initialize the ScrollingText object.

        Parameters:
        - text_list: List of strings representing the credits.
        - font: Pygame font object.
        - text_color: Color of the text.
        - x: X position of the text.
        - start_y: Starting Y position of the text.
        - scroll_speed: Speed at which the text scrolls.
        - screen_width: Screen width for wrapping the text.
        """
        self.text_list = text_list
        self.font = font
        self.text_color = text_color
        self.x = x
        self.start_y = start_y
        self.scroll_speed = scroll_speed
        self.screen_width = screen_width

        # Prepare wrapped text list to handle line wrapping
        self.wrapped_text = self.prepare_wrapped_text()
        self.current_y = self.start_y  # Current Y position for scrolling

    def prepare_wrapped_text(self):
        """Wrap each line of text to fit within the screen width."""
        wrapped_lines = []
        for line in self.text_list:
            wrapped_lines.extend(self.wrap_text(line))
        return wrapped_lines

    def wrap_text(self, text):
        """Wrap a single line of text based on the screen width."""
        words = text.split(' ')
        wrapped_lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            line_width = self.font.size(' '.join(current_line))[0]  # Calculate width
            if line_width > self.screen_width - 20:  # Subtract some margin for padding
                current_line.pop()  # Remove last word that exceeded the width
                wrapped_lines.append(' '.join(current_line))
                current_line = [word]  # Start a new line with the current word

        # Add remaining words as the last line
        wrapped_lines.append(' '.join(current_line))
        return wrapped_lines

    def update(self):
        """Update the scrolling text's Y position."""
        self.current_y -= self.scroll_speed

        # Reset the text position when it scrolls off-screen
        if self.current_y < -len(self.wrapped_text) * (self.font.get_height() + 5):
            self.current_y = self.start_y

    def draw(self, screen):
        """Draw the scrolling text on the screen."""
        y_offset = self.current_y
        for line in self.wrapped_text:
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.x, y_offset))
            y_offset += self.font.get_height() + 5  # Add space between lines
    
# Example list of credits
credits_text = [
    "Game developed by Your Name",
    "Artwork by Artist Name",
    "Music by Composer Name",
    "Special thanks to all the playtesters",
]

font = pygame.font.SysFont('Times New Roman', 30)
scrolling_credits = ScrollingText(credits_text, font, WHITE, 10, (SCREEN_HEIGHT // 3) - 30, 1, SCREEN_WIDTH)


running = True
while running:
    mouse_pos = pygame.mouse.get_pos()  # Update mouse position
    "Event"
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            running = False
            
        #keyboard presses
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
                running = False

        #keyboard button released
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

        # Handle mouse button releases
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                shoot = False
    
    
    # --- Game State Management ---
    if start_game == False:
        # Handle start menu
        screen.blit(bg_start_menu, (0, 0))
        # Add buttons to the start menu
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            running = False
        # Add credits at the bottom left
        # Wrap text if needed (if you want each line to fit within a certain width)
        # Update and draw the scrolling credits
        scrolling_credits.update()  # Update the Y position
        scrolling_credits.draw(screen)  # Draw the text

    else:
        # --- LEVEL-SPECIFIC BACKGROUND DRAWING ---
        if level == 3:
            draw_bg_3()  # Call the background drawing function for level 3
        if level == 2:
            draw_bg_2()
        else:
            draw_bg()  # Default background for other levels
        decoration_group.update()
        decoration_group.draw(screen)
        world.draw()   

        platform_rects = [platform.rect for platform in platforms_group]

        # Update player movement (with platform collision check)
        screen_scroll = player.move(moving_left, moving_right, platform_rects)
    
        # Update game elements
        platforms_group.update(player)  # Pass player to check for breaking or interactions
        platforms_group.draw(screen)

        # Collision Handling
        for bullet in bullet_group:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, False)
            if hit_enemies:
                for enemy in hit_enemies:
                    if isinstance(enemy, FlyingEnemy):  # Only applies to flying enemies
                        enemy.take_damage(1)
                    bullet.kill()

        # When player collects health
        for collectible in collectible_group:
            collectible.update(player)  # Update each collectible
            if pygame.sprite.collide_rect(player, collectible):
                collectible.collect(player)  # Add points for collecting health
        
        # Update and draw player actions
        player.update()
        player.draw()

        # Enemy AI and interactions
        for enemy in enemy_group:
            enemy.ai(player)
            enemy.update(player)
            enemy.draw(screen)
        # Score for hitting enemies
            if enemy.previous_health > enemy.health:
                score_manager.add_points(10 * (enemy.previous_health - enemy.health))

        # Update the gun (to handle reloading and cooldown)
        player.gun.update(mouse_pos, player.rect.center)
        
        # Shooting logic (if the player is shooting)
        if shoot and player.gun.can_shoot:
            player.shoot(mouse_pos)  # Shoot at the mouse position
            shot_fx.play()
            # Display the score on the screen during the game loop  

    
        # Update and draw various groups (bullets, grenades, etc.)
        bullet_group.update()
        grenade_group.update()
        item_box_group.update()
        water_group.update()
        exit_group.update()
        boss_group.update(player)
        enemy_group.update(player)
        
        
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        item_box_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)
        collectible_group.draw(screen)
        boss_group.draw(screen)
        enemy_group.draw(screen)

        # Intro sequence 
        if start_intro:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # Player interactions and movement logic
        if player.alive:
            # Shooting bullets
            if shoot and player.shoot_cooldown == 0:
                angle = math.atan2(mouse_pos[1] - player.rect.centery, mouse_pos[0] - player.rect.centerx)
                player.create_bullet(angle)
                shot_fx.play()
                player.shoot_cooldown = 15  # Cooldown to control fire rate
            elif player.shoot_cooldown > 0:
                player.shoot_cooldown -= 1


            # Handle player movement
            if player.in_air:
                player.update_action(2)  # Jumping
            elif moving_left or moving_right:
                player.update_action(1)  # Running
            else:
                player.update_action(0)  # Idle

            # Move player and handle screen scroll
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll

            # Level completion handling
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()

                if level <= MAX_LEVELS:
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
                elif level == 4:  # Load Boss Level
                    boss, platform_group = load_boss_level()
                    world_data = reset_level()  # Empty the current world and create a boss fight environment
                    world = World()  # Initialize an empty world for this level
                    player, health_bar = world.process_data(world_data)
                    boss.update(player, platform_group)
        # --- Player Death Handling ---
        else:
            screen_scroll = 0
            if death_fade.fade():
                if level == 4:  # Boss level case
                    if restart_button.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro = True
                        boss, platform_group, wall_group = load_boss_level()  # Restart the boss fight
                        player.reset_player()  # Reset player state (health, ammo, etc.)
                        score_manager.reset_to_checkpoint()  # Reset score to the checkpoint for this level
                    if exit_button.draw(screen):
                        running = False
            else:
                # Normal game over logic (for non-boss levels)
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
                if exit_button.draw(screen):
                    running = False
        
        # --- Boss Fight Logic ---
        if level == 4:
            draw_bg_4()
            world.draw()

            boss.update(player, platform_group)  # Update boss logic with player and platforms
            boss.draw_health_bar_on_top(screen)
            screen.blit(boss.image, boss.rect)
            boss.draw_shield(screen)  # Draw the shield in phase 2

            

            # Update the boss logic and draw shield, health bar, etc.
            if boss.alive:
                if boss.phase == 2:
                    platform_group.update()
                    platform_group.draw(screen)
                    boss.stand_on_platform()

                # Update boss logic and draw shield, health bar, etc.    
                boss.update(player, platform_group)  # Update boss with player and platform group
                boss.draw_health_bar(screen)
                screen.blit(boss.image, boss.rect)
                boss.draw_shield(screen)  # Draw the spinning shield around boss

                # Update and draw boss projectiles
                boss.projectile_group.update()
                boss.projectile_group.draw(screen)

            
                if pygame.sprite.spritecollide(player, boss.projectile_group, True):  # True to remove projectile on hit
                    player.take_damage(3) 
            else:
                # Boss is dead, handle victory or transition to end screen
                while True:
                    result = display_end_screen(screen, score_manager)
                    game_over_fx.play()
                    if result == 'restart':
                        boss.alive = True
                        level = 1
                        score_manager.reset_score()
                        start_intro = True
                        bg_scroll = 0
                        world_data = reset_level()

                        with open(f'level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)

                        world = World()
                        player, health_bar = world.process_data(world_data)
                        break

                    if result == 'exit':
                        running = False
                        break

            # Collision Handling: Bullets with the boss
            for bullet in bullet_group:
                if pygame.sprite.collide_rect(bullet, boss):
                    if boss.has_shield and boss.phase == 1:
                        boss_hit_fx.play()
                        # Shield blocks damage in phase 1
                        if isinstance(bullet, Bullet) and not bullet.normal:  # Blast gun removes the shield
                            boss.has_shield = False
                        bullet.kill()
                    else:
                        boss.take_damage(1)
                        score_manager.add_points(10)  # Add points for hitting the boss
                        bullet.kill()

        # --- HUD Elements ---
        health_bar.draw(player.health)
        score_manager.display_score(screen)
        HealthBar.display_health(screen, player.health)
        display_ammo(screen, player.gun.ammo, player.gun.ammo)
        

        # Draw crosshair
        draw_crosshair(screen, player.rect.center, pygame.mouse.get_pos())
     
    clock.tick(60)               
    pygame.display.flip()
    
pygame.quit()
