import pygame
# import os
import logging

logging.basicConfig(level=logging.ERROR)

try:
    # ------------------------- GAME TITLE ------------------------- #
    GAME_TITLE = "Tukkie"

    # ------------------------- GAME SETTINGS ------------------------- #
    FPS = 60
    SCREEN_WIDTH = 1500
    SCREEN_HEIGHT = 700
    CUSTOM_FONT = r"question2\assets\font\8-BIT WONDER.TTF"

    # ------------------------- PLAYER CONTROLS ------------------------- #
    MOVE_LEFT = pygame.K_a
    MOVE_RIGHT = pygame.K_d
    JUMP = pygame.K_w
    SHOOT = pygame.K_e

    # ------------------------- GAME MECHANICS ------------------------- #

    # general game settings
    MAX_ENEMIES = 3
    ENEMY_SPAWN_COOLDOWN = 3000  # 3 seconds in milliseconds
    COLLECTIBLE_SPAWN_COOLDOWN = 5000  # 5 seconds in milliseconds
    SCORE_PER_KILL = 10


    # Bullet Projectile settings
    BULLET_SPEED = 10

    # Player settings
    MAX_PLAYER_HEALTH = 100
    PLAYER_START_X = 100
    PLAYER_HEIGHT = 100
    PLAYER_WIDTH = 100
    PLAYER_SPEED = 5
    # Player ammo settings
    PLAYER_MAX_AMMO = 30
    PLAYER_STARTING_AMMO = 30

    # Player projectile settings
    PLAYER_BULLET_DAMAGE = 15
    PLAYER_PROJECTILE_WIDTH = 60
    PLAYER_PROJECTILE_HEIGHT = 60
    # Player lives settings
    PLAYER_START_LIVES = 3
    PLAYER_RESPAWN_INVULNERABILITY_TIME = 3000  # 3 seconds of invulnerability after respawning

    # Enemy settings
    ENEMY_HEALTH = 15
    ENEMY_MIN_SPEED = 1
    ENEMY_MAX_SPEED = 2
    ENEMY_WIDTH = 80
    ENEMY_HEIGHT = 120

    # Enemy projectile settings
    ENEMY_BULLET_DAMAGE = 5
    ENEMY_PROJECTILE_WIDTH = 50
    ENEMY_PROJECTILE_HEIGHT = 30

    # Enhanced enemy settings
    ENHANCED_ENEMY_HEALTH = 30
    ENHANCED_ENEMY_DAMAGE_MULTIPLIER = 1.5
    # Boss settings
    BOSS_HEALTH = 100
    BOSS_DAMAGE_MULTIPLIER = 2
    BOSS_WIDTH = 150
    BOSS_HEIGHT = 150
    # Boss projectile settings
    BOSS_BULLET_DAMAGE = 15
    BOSS_PROJECTILE_WIDTH = 90
    BOSS_PROJECTILE_HEIGHT = 70

    # Enemy thresholds
    ENHANCED_ENEMY_THRESHOLD = 30
    BOSS_THRESHOLD = 80

    # ------------------------- COLLECTIBLE SETTINGS ------------------------- #
    COLLECTIBLE_SPEED = 2

    # Stake item settings
    STAKE_WIDTH = 60
    STAKE_HEIGHT = 80
    STAKE_SPRITE_PATH = "question2/assets/enemyShrine.png"
    STAKE_SCORE_REDUCTION = 5

    # Ammo item settings
    AMMO_ITEM_AMOUNT = 10
    AMMO_SPRITE_PATH = "question2/assets/playerProjectile.png"
    AMMO_COLLECTIBLE_SIZE = PLAYER_PROJECTILE_WIDTH  

    # Life icon settings
    LIFE_ICON_PATH = "question2/assets/life_icon.png" 
    LIFE_ICON_SIZE = (24, 24)  # Size in pixels (width, height)
    LIFE_ICON_SPACING = 30  # Spacing between icons in pixels

    # Health item settings
    HEALTH_ITEM_HEAL = 25
    HEALTH_ITEM_ICON_PATH = "question2/assets/health_icon.png"
    HEALTH_ITEM_SIZE = (60, 60)

    # ------------------------- SPRITE PATHS ------------------------- #
    # Player sprite paths
    PLAYER_IDLE_SPRITE_PATH = "question2/assets/player_1.png"
    PLAYER_JUMPING_SPRITE_PATH = "question2/assets/player_4.png"
    PLAYER_FALLING_SPRITE_PATH = "question2/assets/player_3.png"
    PLAYER_DAMAGED_SPRITE_PATH = "question2/assets/player_5.png"
    PLAYER_DEAD_SPRITE_PATH = "question2/assets/player_6.png"

    # Enemy sprite paths
    ENEMY_SPRITE_PATH = "question2/assets/enemy.png"
    ENEMY_DEATH_SPRITE_PATH = "question2/assets/enemyDeath.png"
    ENHANCED_ENEMY_SPRITE_PATH = "question2/assets/enemyEnhanced.png"
    ENHANCED_ENEMY_DEATH_SPRITE_PATH = "question2/assets/enemyEnhancedDeath.png"
    BOSS_SPRITE_PATH = "question2/assets/enemyBoss.png"
    BOSS_DEATH_SPRITE_PATH = "question2/assets/enemyBossDeath.png"

    # Projectile sprite paths
    PLAYER_PROJECTILE_SPRITE_PATH = "question2/assets/playerProjectile.png"
    ENEMY_PROJECTILE_SPRITE_PATH = "question2/assets/enemyProjectile.png"
    BOSS_PROJECTILE_SPRITE_PATH = "question2/assets/enemyBossProjectile.png"

    # ------------------------- COLOR CONSTANTS ------------------------- #
    # Color constants
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (100, 100, 100)
    ORANGE = (255, 165, 0)
    BRAT = (138, 206, 206)

    # Game over screen colors
    GAME_OVER_COLOR = RED
    YOU_WIN_COLOR = BRAT
    BUTTON_COLOR = GRAY
    BUTTON_TEXT_COLOR = WHITE

    # Level text colors
    LEVEL_1_COLOR = WHITE
    LEVEL_2_COLOR = ORANGE
    LEVEL_3_COLOR = RED

    # Pause menu colors
    PAUSE_MENU_COLOR = (0, 0, 0)
    PAUSE_TEXT_COLOR = (255, 255, 255)

except Exception as e:
    logging.error(f"Error initializing constants: {e}")
    raise




