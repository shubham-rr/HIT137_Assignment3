import pygame
import button
import csv
import pickle

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

button_list = []
#define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll = 0
scroll_speed = 1
FLOORS = 10  # Number of vertical levels (floors)

# Pagination variables
buttons_per_page = 15
current_page = 0
BUTTON_LIST_MAX_HEIGHT = SCREEN_HEIGHT - 200  # Adjust as needed


#load images
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

total_pages = (len(img_list) - 1) // buttons_per_page + 1

save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()
left_img = pygame.image.load('img/Left Arrow.png').convert_alpha()
right_img = pygame.image.load('img/Right-Arrow-PNG-Image.png').convert_alpha()
left_img = pygame.transform.scale(left_img, (50, 50))  # Resize to 50x50 pixels
right_img = pygame.transform.scale(right_img, (50, 50))  # Resize to 50x50 pixels

def draw_page_number():
	page_text = f"Page: {current_page + 1}/{total_pages}"
	draw_text(page_text, font, WHITE, SCREEN_WIDTH + SIDE_MARGIN - 195, SCREEN_HEIGHT + LOWER_MARGIN - 135)

#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont('Futura', 30)

#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)

#create ground
for tile in range(0, MAX_COLS):
	world_data[ROWS - 1][tile] = 0


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#create function for drawing background
def draw_bg():
	screen.fill(GREEN)
	width = sky_img.get_width()
	for x in range(4):
		screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
		screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

#draw grid
def draw_grid():
	if level in [3, 4]:
        # Vertical lines
		for c in range(MAX_COLS + 1):
			pygame.draw.line(screen, WHITE, (c * TILE_SIZE, 0 - scroll), (c * TILE_SIZE, SCREEN_HEIGHT - scroll))
        # Horizontal lines
		for c in range(ROWS + 1):
			pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE - scroll), (SCREEN_WIDTH, c * TILE_SIZE - scroll))
	else:
        # Vertical lines
		for c in range(MAX_COLS + 1):
			pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
        # Horizontal lines
		for c in range(ROWS + 1):
			pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


#function for drawing the world tiles
def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:  # Ensure tile index is valid
				print(f"Drawing tile {tile} at position ({x}, {y})")
				if level in [3, 4]:
					screen.blit(img_list[tile], (x * TILE_SIZE, y * TILE_SIZE - scroll))
				else:
					screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


#create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
left_button = button.Button(SCREEN_WIDTH + SIDE_MARGIN - 250, SCREEN_HEIGHT + LOWER_MARGIN - 150, left_img, 1)
right_button = button.Button(SCREEN_WIDTH + SIDE_MARGIN - 100, SCREEN_HEIGHT + LOWER_MARGIN - 150, right_img, 1)


def update_button_list():
	# Clear the button list
	global button_list
	button_list.clear()
	button_col = 0
	button_row = 0
	level_img_list = level_images.get(level, [])  # Get the list of images for the current level
	start_index = current_page * buttons_per_page
	end_index = min(start_index + buttons_per_page, len(level_img_list))
	print(f"Updating button list for page {current_page}: start_index={start_index}, end_index={end_index}")
	for i in range(start_index, end_index):
		if i >= len(level_img_list):
			break	# Prevents index error
		img_index = level_img_list[i]
		if img_index < len(img_list): # Check if img_index is valid
			print(f"Adding button for image index {img_index}")
			tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[img_index], 1) 
			button_list.append(tile_button)
			button_col += 1
		if button_col == 3:
			button_row += 1
			button_col = 0
print(f"Button List: {[button.image for button in button_list]}")

level_images = {  # Level 0 has images 0, 1, 2
    1: [0,1,2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,15,16,17,18,19,20 ],  # Level 1 has images 1 to 20
    2: [6, 7, 8],  # Level 2 has images 6, 7, 8
    3: [9, 10, 11],  # Level 3 has images 9, 10, 11
}
MAX_LEVEL = max(level_images.keys())


run = True
while run:

	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()

	draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

	#save and load data
	if save_button.draw(screen):
		#save level data
		with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				writer.writerow(row)
		#alternative pickle method
		#pickle_out = open(f'level{level}_data', 'wb')
		#pickle.dump(world_data, pickle_out)
		#pickle_out.close()
	if load_button.draw(screen):
		#load in level data
		#reset scroll back to the start of the level
		scroll = 0
		with open(f'level{level}_data.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					world_data[x][y] = int(tile)
		#alternative pickle method
		#world_data = []
		#pickle_in = open(f'level{level}_data', 'rb')
		#world_data = pickle.load(pickle_in)
				

	#draw tile panel and tiles
	pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

	# Draw page number
	draw_page_number()

	#choose a tile
	button_count = 0
	for button_count, tile_button in enumerate(button_list):
		if tile_button.draw(screen):
			current_tile = current_page * buttons_per_page + button_count
			print(f"Selected tile index: {current_tile}")
	if 0 <= current_tile < len(img_list):
		page_tile_index = current_tile % buttons_per_page
		if page_tile_index < len(button_list):
			pygame.draw.rect(screen, RED, button_list[page_tile_index].rect, 3)


	#draw left and right buttons
	if left_button.draw(screen) and current_page > 0:
		current_page -= 1
		update_button_list()
		pygame.draw.rect(screen, RED, left_button.rect, 3)
	if right_button.draw(screen) and current_page < total_pages - 1:
		current_page += 1
		update_button_list()
		pygame.draw.rect(screen, RED, right_button.rect, 3)

	#scroll the map
	if level in [3, 4]:
		if scroll_up and scroll > 0:
			scroll -= 5 * scroll_speed
		if scroll_down and scroll < (ROWS * TILE_SIZE) - SCREEN_HEIGHT:
			scroll += 5 * scroll_speed
	else:
		if scroll_left == True and scroll > 0:
			scroll -= 5 * scroll_speed
		if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
			scroll += 5 * scroll_speed

	#add new tiles to the screen
	#get mouse position
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	#check that the coordinates are within the tile area
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#update tile value
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		# keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
				if level > MAX_LEVEL:  # Prevent going above max level
					level = MAX_LEVEL
				update_button_list()
				scroll = 0  # Reset scroll when changing levels
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
				update_button_list()
				scroll = 0  # Reset scroll when changing levels
				
			if level in [3, 4]:
				if event.key == pygame.K_LEFT:
					scroll_up = True  # Left key scrolls up
				if event.key == pygame.K_RIGHT:
					scroll_down = True  # Right key scrolls down
			else:
				if event.key == pygame.K_LEFT:
					scroll_left = True  # Left key scrolls left
				if event.key == pygame.K_RIGHT:
					scroll_right = True  # Right key scrolls right

			if event.key == pygame.K_RSHIFT:
				scroll_speed = 5

		if event.type == pygame.KEYUP:
			if level in [3, 4]:
				if event.key == pygame.K_LEFT:
					scroll_up = False
				if event.key == pygame.K_RIGHT:
					scroll_down = False
			else:
				if event.key == pygame.K_LEFT:
					scroll_left = False
				if event.key == pygame.K_RIGHT:
					scroll_right = False
			if event.key == pygame.K_RSHIFT:
				scroll_speed = 1



	pygame.display.update()

pygame.quit()
