import pygame
import random

pygame.mixer.init()
pygame.init()

# Screen dimensions
screen_width = 900
screen_height = 600

# Load eating sound effects
eating_sound = pygame.mixer.Sound("Resources/eating.mp3")
eating_sound.set_volume(0.6)

# Background Image
bgimg = pygame.image.load("Resources/BG.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Snake and food size
snake_size = 20  
food_size = 20  

font = pygame.font.SysFont(None, 55)
game_over_font = pygame.font.SysFont(None, 75)

gamewindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game By Adiraj")

clock = pygame.time.Clock()

def text_screen(text, color, font, y_offset=0):
    screen_text = font.render(text, True, color)
    text_rect = screen_text.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))
    gamewindow.blit(screen_text, text_rect)

def plot_snake(gamewindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gamewindow, color, [x, y, snake_size, snake_size])

def game_loop():
    exit_game = False
    game_over = False

    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    speed = 10

    # Food position
    food_x = random.randint(20, screen_width - food_size)
    food_y = random.randint(20, screen_height - food_size)

    # Snake initialization
    snake_list = []
    snake_length = 1
    score = 0

    # Play background music
    pygame.mixer.music.load("Resources/background.mp3")
    pygame.mixer.music.play(-1)

    while not exit_game:
        if game_over:
            pygame.mixer.music.stop()  
            collision_sound = pygame.mixer.Sound("Resources/Dead.mp3")
            collision_sound.set_volume(0.5)
            if not pygame.mixer.get_busy(): 
                collision_sound.play()

            gamewindow.fill(white)
            text_screen("Game Over!", red, game_over_font)
            text_screen("Press R to Restart or Q to Quit", black, font, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  
                        game_loop()
                    elif event.key == pygame.K_q:  
                        exit_game = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        velocity_x = -speed
                        velocity_y = 0
                    elif event.key == pygame.K_RIGHT:
                        velocity_x = speed
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = -speed
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = speed
                        velocity_x = 0
                    elif event.key == pygame.K_q:
                        exit_game = True
                    elif event.key == pygame.K_o:
                        score += 10
                    elif event.key == pygame.K_p:
                        score -= 10

            
            snake_x += velocity_x
            snake_y += velocity_y

            if snake_x < 0:
                snake_x = screen_width - snake_size
            elif snake_x > screen_width - snake_size:
                snake_x = 0
            if snake_y < 0:
                snake_y = screen_height - snake_size
            elif snake_y > screen_height - snake_size:
                snake_y = 0

            # Food collision check
            if abs(snake_x - food_x) < food_size and abs(snake_y - food_y) < food_size:
                score += 1
                food_x = random.randint(20, screen_width - food_size)
                food_y = random.randint(20, screen_height - food_size)
                snake_length += 5
                eating_sound.play()

            # Update snake body
            head = [snake_x, snake_y]
            snake_list.append(head)

            if len(snake_list) > snake_length:
                snake_list.pop(0)

            if snake_length > 1 and head in snake_list[:-1]:
                game_over = True

            gamewindow.fill(white)
            gamewindow.blit(bgimg, (0, 0))
            text_screen(f"Score: {score * 10}", white, font, -250)
            plot_snake(gamewindow, white, snake_list, snake_size)  
            pygame.draw.rect(gamewindow, red, [food_x, food_y, food_size, food_size])

            pygame.display.update()
            clock.tick(40)

    pygame.quit()

game_loop()