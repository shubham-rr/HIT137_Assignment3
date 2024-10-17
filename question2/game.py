import pygame
import math
import os
import random
import logging
from constants import (
    FPS, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_BULLET_DAMAGE, ENEMY_WIDTH,
    MAX_ENEMIES, ENEMY_SPAWN_COOLDOWN, COLLECTIBLE_SPAWN_COOLDOWN,
    SCORE_PER_KILL, HEALTH_ITEM_HEAL, MAX_PLAYER_HEALTH,
    PLAYER_START_X, PLAYER_HEIGHT, AMMO_ITEM_AMOUNT,
    ENHANCED_ENEMY_THRESHOLD, BOSS_THRESHOLD, CUSTOM_FONT, GAME_TITLE, STAKE_SCORE_REDUCTION,
    LEVEL_1_COLOR, LEVEL_2_COLOR, LEVEL_3_COLOR,
    LIFE_ICON_PATH, LIFE_ICON_SIZE, LIFE_ICON_SPACING,
    GAME_OVER_COLOR, YOU_WIN_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR,
    PAUSE_MENU_COLOR, PAUSE_TEXT_COLOR
)
from player import Player
from enemy import Enemy, EnhancedEnemy, Boss
from hud import HUD
from collectible import Collectible

logging.basicConfig(level=logging.ERROR)

class Game:
    # Encapsulation: Bundling game data and methods within a single unit
    def __init__(self):
        try:
            pygame.init()
            self.clock = pygame.time.Clock()
            
            # Create game window
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption(GAME_TITLE)
            
            # Load images
            self.bg = self.load_image("bg.png")
            self.platform = self.load_image("platform.png")
            
            self.bg_width = self.bg.get_width()
            self.bg_rect = self.bg.get_rect()
            
            # Define game variables
            self.scroll = 0
            self.tiles = math.ceil(SCREEN_WIDTH / self.bg_width) + 1
            
            # Platform positioning
            self.platform_height = 80
            self.platform_y = SCREEN_HEIGHT - self.platform_height
            
            # Initialize fonts
            self.font_small = pygame.font.Font(CUSTOM_FONT, 24)
            self.font_medium = pygame.font.Font(CUSTOM_FONT, 36)
            self.font_large = pygame.font.Font(CUSTOM_FONT, 74)
            
            self.game_state = "MENU"
            
            # call reset_game after fonts are initialized
            self.reset_game()
            
            self.level = 1  # Initialize level to 1
            self.max_level_reached = 1  # Keep track of the highest level reached

            self.life_icon = pygame.image.load(LIFE_ICON_PATH)
            self.life_icon = pygame.transform.scale(self.life_icon, LIFE_ICON_SIZE)

            self.paused = False
        except Exception as e:
            logging.error(f"Error initializing Game: {e}")
            raise

    # Encapsulation: Method for resetting game state
    def reset_game(self):
        try:
            # Create player
            player_y = self.platform_y - PLAYER_HEIGHT
            self.player = Player(PLAYER_START_X, player_y, self.platform_y)
            
            # Create enemies
            self.enemies = pygame.sprite.Group()
            self.max_enemies = MAX_ENEMIES
            self.last_spawn_time = 0
            self.spawn_cooldown = ENEMY_SPAWN_COOLDOWN
            
            # Create HUD with custom font
            self.hud = HUD(self.font_small)
            
            self.game_over = False
            self.running = True
            
            self.collectibles = pygame.sprite.Group()
            self.last_collectible_spawn = 0
            self.collectible_spawn_cooldown = COLLECTIBLE_SPAWN_COOLDOWN

            self.score = 0

            # Initialize boss-related attributes
            self.boss_spawned = False
            self.boss_defeated = False

            self.level = 1  # Reset level to 1
            self.max_level_reached = 1  # Reset max_level_reached to 1
            self.boss_spawned = False  # Reset boss_spawned flag
            self.boss_defeated = False  # Reset boss_defeated flag
        except Exception as e:
            logging.error(f"Error resetting game: {e}")
            raise

    # Abstraction: Method for loading images
    def load_image(self, filename):
        """Load an image from the assets folder."""
        try:
            return pygame.image.load(os.path.join("question2", "assets", filename)).convert_alpha()
        except pygame.error as e:
            logging.error(f"Error loading image {filename}: {e}")
            raise

    # Encapsulation: Method for handling events
    def handle_events(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.paused:
                        self.handle_pause_menu_click(event.pos)
                    elif self.game_state == "MENU":
                        self.handle_menu_click(event.pos)
                    elif self.game_state in ["INSTRUCTIONS", "CREDITS"]:
                        button_width, button_height = 280, 40
                        button_y = 530
                        back_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, button_y, button_width, button_height)
                        if back_button.collidepoint(event.pos):
                            self.game_state = "MENU"
                    elif self.game_state == "PLAYING" and self.game_over:
                        button_width = 350  # need to make sure this matches the width in the draw method
                        restart_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT * 2 // 3 - 60, button_width, 40)
                        menu_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT * 2 // 3, button_width, 40)
                        if restart_button.collidepoint(event.pos):
                            self.reset_game()
                            self.game_over = False
                            self.game_state = "PLAYING"
                        elif menu_button.collidepoint(event.pos):
                            self.game_state = "MENU"
                            self.reset_game()
        except Exception as e:
            logging.error(f"Error handling events: {e}")
            raise

    # Encapsulation: Method for handling menu clicks
    def handle_menu_click(self, pos):
        try:
            button_width, button_height = 280, 40
            button_y_positions = [220, 280, 340, 400]
            
            for i, y in enumerate(button_y_positions):
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, y, button_width, button_height)
                if button_rect.collidepoint(pos):
                    if i == 0:  # Start Game
                        self.game_state = "PLAYING"
                        self.reset_game()
                    elif i == 1:  # Instructions
                        self.game_state = "INSTRUCTIONS"
                    elif i == 2:  # Credits
                        self.game_state = "CREDITS"
                    elif i == 3:  # Exit
                        self.running = False
                    break
        except Exception as e:
            logging.error(f"Error handling menu click: {e}")
            raise

    # Encapsulation: Method for handling pause menu clicks
    def handle_pause_menu_click(self, pos):
        try:
            button_width, button_height = 280, 40
            button_y_positions = [220, 280, 340]
            
            for i, y in enumerate(button_y_positions):
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, y, button_width, button_height)
                if button_rect.collidepoint(pos):
                    if i == 0:  # Resume
                        self.paused = False
                    elif i == 1:  # Restart
                        self.reset_game()
                        self.paused = False
                    elif i == 2:  # Quit to Menu
                        self.game_state = "MENU"
                        self.paused = False
                        self.reset_game()
                    break
        except Exception as e:
            logging.error(f"Error handling pause menu click: {e}")
            raise

    # Encapsulation: Methods for drawing different game states
    def draw_menu(self):
        try:
            self.screen.fill((0, 0, 0))
            title = self.font_large.render(GAME_TITLE, True, (255, 255, 255))
            start_text = self.font_small.render("Start Game", True, (255, 255, 255))
            instructions_text = self.font_small.render("Instructions", True, (255, 255, 255))
            credits_text = self.font_small.render("Credits", True, (255, 255, 255))
            exit_text = self.font_small.render("Exit", True, (255, 255, 255))

            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            
            button_width, button_height = 280, 40
            button_y_positions = [220, 280, 340, 400]
            
            for i, (text, y) in enumerate(zip([start_text, instructions_text, credits_text, exit_text], button_y_positions)):
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, y, button_width, button_height)
                pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
                self.screen.blit(text, (button_rect.centerx - text.get_width() // 2, button_rect.centery - text.get_height() // 2))
        except Exception as e:
            logging.error(f"Error drawing menu: {e}")
            raise

    def draw_instructions(self):
        try:
            self.screen.fill((0, 0, 0))
            title = self.font_large.render("Instructions", True, (255, 255, 255))
            instruction1 = self.font_small.render("Use WASD to move", True, (255, 255, 255))
            instruction2 = self.font_small.render("Press E to shoot", True, (255, 255, 255))
            instruction3 = self.font_small.render("Collect items to regain health and ammo", True, (255, 255, 255))
            instruction4 = self.font_small.render("Crucifix bones will decrease your score", True, (255, 255, 255))
            back_text = self.font_small.render("Back", True, (255, 255, 255))

            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            
            self.screen.blit(instruction1, (SCREEN_WIDTH // 2 - instruction1.get_width() // 2, 230))
            self.screen.blit(instruction2, (SCREEN_WIDTH // 2 - instruction2.get_width() // 2, 280))
            self.screen.blit(instruction3, (SCREEN_WIDTH // 2 - instruction3.get_width() // 2, 330))
            self.screen.blit(instruction4, (SCREEN_WIDTH // 2 - instruction4.get_width() // 2, 380))

            button_width, button_height = 280, 40
            button_y = 530
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
            self.screen.blit(back_text, (button_rect.centerx - back_text.get_width() // 2, button_rect.centery - back_text.get_height() // 2))
        except Exception as e:
            logging.error(f"Error drawing instructions: {e}")
            raise
    
    def draw_credits(self):
        try:
            self.screen.fill((0, 0, 0))
            title = self.font_large.render("Credits", True, (255, 255, 255))
            credit1 = self.font_small.render("Made by Group 7 CAS 133", True, (255, 255, 255))
            credit2 = self.font_small.render("Shubham Maharjan [ Code Art Design ]", True, (255, 255, 255))
            credit3 = self.font_small.render("Huong Thao Trinh ( Lea ) [ Code Design ]", True, (255, 255, 255))
            credit4 = self.font_small.render("Phuc Tran ( Owen ) [ Code ]", True, (255, 255, 255))
            credit5 = self.font_small.render("Muhammad Ahmad [ Code ]", True, (255, 255, 255))
            credit6 = self.font_small.render(" ", True, (255, 255, 255))
            back_text = self.font_small.render("Back", True, (255, 255, 255))

            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            
            self.screen.blit(credit1, (SCREEN_WIDTH // 2 - credit1.get_width() // 2, 230))
            self.screen.blit(credit2, (SCREEN_WIDTH // 2 - credit2.get_width() // 2, 280))
            self.screen.blit(credit3, (SCREEN_WIDTH // 2 - credit3.get_width() // 2, 330))
            self.screen.blit(credit4, (SCREEN_WIDTH // 2 - credit4.get_width() // 2, 380))
            self.screen.blit(credit5, (SCREEN_WIDTH // 2 - credit5.get_width() // 2, 430))
            self.screen.blit(credit6, (SCREEN_WIDTH // 2 - credit6.get_width() // 2, 480))

            button_width, button_height = 280, 40
            button_y = 530
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, button_y, button_width, button_height)
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect)
            self.screen.blit(back_text, (button_rect.centerx - back_text.get_width() // 2, button_rect.centery - back_text.get_height() // 2))
        except Exception as e:
            logging.error(f"Error drawing credits: {e}")
            raise

    # Encapsulation: Method for spawning collectibles
    def spawn_collectible(self):
        try:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_collectible_spawn > self.collectible_spawn_cooldown:
                # Spawn collectibles only on the left side of the screen
                x = random.randint(50, SCREEN_WIDTH // 2 - 50)  # 50 pixels padding from left and center
                y = 0  # Spawn at the top of the screen
                collectible_type = random.choice(['health', 'ammo', 'stake'])
                collectible = Collectible(x, y, collectible_type)
                self.collectibles.add(collectible)
                self.last_collectible_spawn = current_time
        except Exception as e:
            logging.error(f"Error spawning collectible: {e}")
            raise

    # Encapsulation: Method for spawning enemies
    def spawn_enemies(self):
        try:
            current_time = pygame.time.get_ticks()
            screen_center = SCREEN_WIDTH // 2
            if not self.boss_spawned and self.score >= BOSS_THRESHOLD:
                x = random.randint(screen_center, SCREEN_WIDTH - ENEMY_WIDTH)
                y = self.platform_y - 60
                boss = Boss(x, y, self.platform_y)
                self.enemies.add(boss)
                self.boss_spawned = True
            elif len(self.enemies) < self.max_enemies and current_time - self.last_spawn_time > self.spawn_cooldown and not self.boss_spawned:
                x = random.randint(screen_center, SCREEN_WIDTH - ENEMY_WIDTH)
                y = self.platform_y - 60
                if self.score >= ENHANCED_ENEMY_THRESHOLD:
                    enemy = EnhancedEnemy(x, y, self.platform_y)
                else:
                    enemy = Enemy(x, y, self.platform_y)
                self.enemies.add(enemy)
                self.last_spawn_time = current_time
        except Exception as e:
            logging.error(f"Error spawning enemies: {e}")
            raise

    # Encapsulation: Method for handling collisions
    def handle_collisions(self):
        try:
            # Player bullets hitting enemies
            for enemy in self.enemies:
                hits = pygame.sprite.spritecollide(enemy, self.player.bullets, True)
                for hit in hits:
                    enemy.take_damage(PLAYER_BULLET_DAMAGE)
                    if not enemy.is_alive():
                        self.enemies.remove(enemy)
                        if isinstance(enemy, Boss):
                            self.boss_defeated = True
                            self.game_over = True
                        else:
                            self.score += SCORE_PER_KILL
        
            # Enemy bullets hitting player
            for enemy in self.enemies:
                hits = pygame.sprite.spritecollide(self.player, enemy.bullets, True)
                for hit in hits:
                    self.player.take_damage(hit.damage)
                    if self.player.lives <= 0:
                        self.game_over = True

            # Player collecting items
            collected = pygame.sprite.spritecollide(self.player, self.collectibles, True)
            for item in collected:
                if item.type == 'health':
                    self.player.health = min(self.player.health + HEALTH_ITEM_HEAL, MAX_PLAYER_HEALTH)
                elif item.type == 'ammo':
                    self.player.add_ammo(AMMO_ITEM_AMOUNT)
                elif item.type == 'stake':
                    self.score = max(0, self.score - STAKE_SCORE_REDUCTION)  # to ensure score doesn't go below 0
        except Exception as e:
            logging.error(f"Error handling collisions: {e}")
            raise

    # Encapsulation: Method for updating game state
    def update(self):
        try:
            if not self.game_over and not self.paused:
                # Scroll the background
                self.scroll -= 5
                # Reset the scroll position when it exceeds the width of the background
                if abs(self.scroll) > self.bg_width:
                    self.scroll = 0
                self.player.update()
                self.enemies.update()
                self.collectibles.update()
                self.handle_collisions()
                self.spawn_enemies()
                self.spawn_collectible()
                
                # Update level based on enemy type
                if self.boss_spawned:
                    self.level = 3
                elif any(isinstance(enemy, EnhancedEnemy) for enemy in self.enemies):
                    self.level = max(2, self.level)
                
                # Update max_level_reached
                self.max_level_reached = max(self.max_level_reached, self.level)
                
                # Ensure level never decreases
                self.level = self.max_level_reached
                
                # Update enemy sprites based on health
                for enemy in self.enemies:
                    if enemy.health <= 0:
                        enemy.set_sprite('death')
                    else:
                        enemy.set_sprite('normal')
                
                if self.player.lives <= 0:
                    self.game_over = True
                elif self.player.health <= 0:
                    # Respawn the player
                    player_y = self.platform_y - PLAYER_HEIGHT
                    self.player.reset_position(PLAYER_START_X, player_y)
                    self.player.respawn()
            elif self.boss_defeated:
                # The game is over, but we're waiting for the player to choose to return to the menu
                pass
            else:
                # Game over, but not because of boss defeat
                pass
        except Exception as e:
            logging.error(f"Error updating game state: {e}")
            raise

    # Encapsulation: Method for drawing game elements
    def draw(self):
        try:
            # Draw scrolling background
            for i in range(0, self.tiles):
                self.screen.blit(self.bg, (i * self.bg_width + self.scroll, 0))
                self.bg_rect.x = i * self.bg_width + self.scroll
            
            # Draw platform
            platform_width = SCREEN_WIDTH
            scaled_platform = pygame.transform.scale(self.platform, (platform_width, self.platform_height))
            self.screen.blit(scaled_platform, (0, self.platform_y))
            
            # Draw player and enemies
            self.player.draw(self.screen)
            self.enemies.draw(self.screen)
            for enemy in self.enemies:
                enemy.bullets.draw(self.screen)
            
            # Draw collectibles
            self.collectibles.draw(self.screen)
            
            # Draw HUD
            self.hud.draw(self.screen, self.player, self.score)
            
            # Draw level indicator with color based on level
            if self.level == 1:
                level_color = LEVEL_1_COLOR
            elif self.level == 2:
                level_color = LEVEL_2_COLOR
            else:
                level_color = LEVEL_3_COLOR

            level_text = self.font_medium.render(f"LEVEL {self.level}", True, level_color)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 30))  # 30 pixels from the top
            self.screen.blit(level_text, level_rect)
            
            # Boss text below Level 3
            if self.level == 3:
                boss_text = self.font_medium.render("BOSS", True, LEVEL_3_COLOR)
                boss_rect = boss_text.get_rect(center=(SCREEN_WIDTH // 2, 70))
                self.screen.blit(boss_text, boss_rect)
            
            # Draw lives
            life_icon_width, life_icon_height = LIFE_ICON_SIZE
            life_icon_spacing = LIFE_ICON_SPACING
            ammo_text_height = 30  # Approximate height of the ammo text
            vertical_spacing = 40  # Increased spacing below ammo text
            
            # Add "LIVES" text
            lives_text = self.font_small.render("LIVES", True, (255, 255, 255))
            lives_text_pos = (10, 10 + ammo_text_height + vertical_spacing)
            self.screen.blit(lives_text, lives_text_pos)
            
            # Draw life icons
            for i in range(self.player.lives):
                x_position = 10 + lives_text.get_width() + 10 + i * (life_icon_width + life_icon_spacing)
                y_position = lives_text_pos[1] + (lives_text.get_height() - life_icon_height) // 2 + 2  # 2 pixels more down
                self.screen.blit(self.life_icon, (x_position, y_position))
            
            if self.game_over:
                game_over_text = self.font_large.render("You Win" if self.boss_defeated else "GAME OVER", True, YOU_WIN_COLOR if self.boss_defeated else GAME_OVER_COLOR)
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3 - game_over_text.get_height() // 2))
                
                score_color = YOU_WIN_COLOR if self.boss_defeated else GAME_OVER_COLOR
                score_text = self.font_medium.render(f"FINAL SCORE {self.score}", True, score_color)
                self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
                
                # Add "Restart" button
                restart_text = self.font_small.render("RESTART", True, BUTTON_TEXT_COLOR)
                button_width = 350
                restart_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT * 2 // 3 - 60, button_width, 40)
                pygame.draw.rect(self.screen, BUTTON_COLOR, restart_button)
                self.screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, restart_button.centery - restart_text.get_height() // 2))

                # Add "Return to Menu" button
                menu_text = self.font_small.render("RETURN TO MENU", True, BUTTON_TEXT_COLOR)
                menu_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT * 2 // 3, button_width, 40)
                pygame.draw.rect(self.screen, BUTTON_COLOR, menu_button)
                self.screen.blit(menu_text, (menu_button.centerx - menu_text.get_width() // 2, menu_button.centery - menu_text.get_height() // 2))
            
            if self.paused:
                self.draw_pause_menu()

            pygame.display.update()
        except Exception as e:
            logging.error(f"Error drawing game elements: {e}")
            raise

    # Encapsulation: Method for drawing pause menu
    def draw_pause_menu(self):
        try:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(PAUSE_MENU_COLOR)
            self.screen.blit(overlay, (0, 0))

            title = self.font_large.render("PAUSED", True, PAUSE_TEXT_COLOR)
            resume_text = self.font_small.render("Resume", True, PAUSE_TEXT_COLOR)
            restart_text = self.font_small.render("Restart", True, PAUSE_TEXT_COLOR)
            quit_text = self.font_small.render("Quit to Menu", True, PAUSE_TEXT_COLOR)

            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            
            button_width, button_height = 280, 40
            button_y_positions = [220, 280, 340]
            
            for i, (text, y) in enumerate(zip([resume_text, restart_text, quit_text], button_y_positions)):
                button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, y, button_width, button_height)
                pygame.draw.rect(self.screen, BUTTON_COLOR, button_rect)
                self.screen.blit(text, (button_rect.centerx - text.get_width() // 2, button_rect.centery - text.get_height() // 2))
        except Exception as e:
            logging.error(f"Error drawing pause menu: {e}")
            raise

    # Encapsulation: Main game loop method
    def run(self):
        try:
            while self.running:
                self.clock.tick(FPS)
                self.handle_events()

                if self.game_state == "MENU":
                    self.draw_menu()
                elif self.game_state == "INSTRUCTIONS":
                    self.draw_instructions()
                elif self.game_state == "CREDITS":
                    self.draw_credits()
                elif self.game_state == "PLAYING":
                    self.update()
                    self.draw()

                pygame.display.update()

            pygame.quit()
        except Exception as e:
            logging.error(f"Error in game loop: {e}")
            pygame.quit()