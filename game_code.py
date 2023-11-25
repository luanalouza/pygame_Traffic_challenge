import pygame
from pygame.locals import *
import time
import random

# Set the size of the window
size = width, height = (500, 500)

# Define road properties
road_w = int(width / 1.4)
roadmark_w = int(width / 50)
green_area_start = width / 2 - road_w / 2
green_area_end = width / 2 + road_w / 2
yellow_line_y = 0
yellow_line_gap = 100
yellow_line_width = 60
yellow_line_speed = 5

# Set the car speed and acceleration
car_speed = 0
car_max_speed = 10
car_acceleration = 0.2
car_deceleration = 0.1

# Initialize pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((size))
pygame.display.set_caption('Road game')
screen.fill((60, 220, 0))

# Load car images and set their initial positions
car = pygame.image.load('images/car_1.png')
car_loc = car.get_rect()
car_loc.center = width / 2 + road_w / 4, height * 0.8

car_2 = pygame.image.load('images/car_2.png')
car2_loc = car_2.get_rect()
car2_loc.center = width / 2 + road_w / 4, -height
car2_speed = 5

car_3 = pygame.image.load('images/car_3.png')
car3_loc = car_3.get_rect()
car3_loc.center = width / 2 - road_w / 4, height
car3_speed = 4

# Load the crash image
crash_image = pygame.image.load('images/crash.png')
crash_rect = crash_image.get_rect()

# Load vegetation image
vegetation_img = pygame.image.load('images/vegetation.png')
vegetation_speed = 3  # Adjust the speed of the vegetation
vegetation_list = []
vegetation_frequency = 250  # Adjust the frequency of vegetation
vegetation_counter = 0

# Set the game clock
clock = pygame.time.Clock()

# Set initial game over state and text
game_over = False
font = pygame.font.Font(None, 36)
game_over_text = font.render('Game Over - Press R to Restart', True, (255, 255, 255))
game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))

# Set the initial score and create the font for the score counter
score = 0
score_font = pygame.font.Font(None, 30)

# Timer variables
start_time = None
penalty_time = 5  # 5 seconds penalty for staying in the middle lane

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if game_over and event.type == KEYDOWN:
            if event.key == K_r:
                game_over = False
                car_loc.center = width / 2 + road_w / 4, height * 0.8
                car2_loc.center = width / 2 + road_w / 4, -height
                car3_loc.center = width / 2 - road_w / 4, height
                score = 0
                vegetation_list = []
                vegetation_counter = 3

    if not game_over:
        keys = pygame.key.get_pressed()

        # Move the player's car if the game is not over
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if car_speed > -car_max_speed:
                car_speed -= car_acceleration
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if car_speed < car_max_speed:
                car_speed += car_acceleration
        else:
            if car_speed > 0:
                car_speed -= car_deceleration
            elif car_speed < 0:
                car_speed += car_deceleration

        car_loc.centerx += car_speed

        # Penalty for staying in the middle lane
        if green_area_start <= car_loc.centerx <= green_area_end - car.get_width():
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time > penalty_time:
                score = max(0, score - 1)  # Reduce the score by 1 if the penalty time is exceeded
                start_time = None
        else:
            start_time = None

        if car_loc.centerx > green_area_end - car.get_width() / 2:
            car_loc.centerx = green_area_end - car.get_width() / 2
        elif car_loc.centerx < green_area_start + car.get_width() / 2:
            car_loc.centerx = green_area_start + car.get_width() / 2

        # Move the enemy cars if the game is not over and update the score
        car2_loc.centery += car2_speed
        if car2_loc.top > height:
            car2_loc.center = width / 2 + road_w / 4, -height
            score += 1

        car3_loc.centery += car3_speed
        if car3_loc.top > height:
            car3_loc.center = width / 2 - road_w / 4, -height
            score += 1

        # Set the game over state and the position of the crash image
        if car_loc.colliderect(car2_loc) or car_loc.colliderect(car3_loc):
            game_over = True
            crash_rect.center = car_loc.center

        # Update the position of the yellow lines
        yellow_line_y += yellow_line_speed
        if yellow_line_y > yellow_line_gap:
            yellow_line_y = 0

        # Move the vegetation
        for vegetation_rect in vegetation_list:
            vegetation_rect.y += vegetation_speed
            if vegetation_rect.y > height:
                vegetation_rect.x = random.choice(
                    [random.randint(0, int(green_area_start) - vegetation_rect.width),
                     random.randint(int(green_area_end), width - vegetation_rect.width)])
                vegetation_rect.y = -vegetation_rect.height

        # Add new vegetation
        vegetation_counter += 0.5

        if vegetation_counter == vegetation_frequency:
            vegetation_counter = 0
            vegetation_rect = vegetation_img.get_rect()
            vegetation_rect.x = random.choice(
                [random.randint(0, int(green_area_start) - vegetation_rect.width),
                 random.randint(int(green_area_end), width - vegetation_rect.width)])
            vegetation_rect.y = -vegetation_rect.height
            vegetation_list.append(vegetation_rect)
            vegetation_counter = 0

    # Fill the screen and draw the road
    screen.fill((60, 220, 0))
    pygame.draw.rect(screen, (50, 50, 50), (width / 2 - road_w / 2, 0, road_w, height))
    pygame.draw.rect(screen, (255, 255, 255), (width / 2 - road_w / 2 + roadmark_w * 2 / 2, 0, roadmark_w, height))
    pygame.draw.rect(screen, (255, 255, 255), (width / 2 + road_w / 2 - roadmark_w * 4 / 2, 0, roadmark_w, height))

    # Draw the sequential yellow lines
    current_line_y = yellow_line_y
    while current_line_y < height:
        yellow_line_rect = pygame.Rect(width / 2 - roadmark_w / 2, current_line_y, roadmark_w, yellow_line_width)
        pygame.draw.rect(screen, (255, 240, 60), yellow_line_rect)
        current_line_y += 2 * yellow_line_gap

    # Display the player's car, enemy cars, vegetation, crash image, game over text, and score counter
    screen.blit(car, car_loc)
    screen.blit(car_2, car2_loc)
    screen.blit(car_3, car3_loc)

    # Draw the vegetation
    for vegetation_rect in vegetation_list:
        screen.blit(vegetation_img, vegetation_rect)

    if game_over:
        screen.blit(crash_image, crash_rect)
        screen.blit(game_over_text, game_over_rect)

    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update the display and set the frame rate
    pygame.display.update()
    clock.tick(60)

# Quit the pygame window
pygame.quit()
