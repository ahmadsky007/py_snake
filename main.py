import pygame, sys, time, random

game_speed = 10

window_width = 800
window_height = 600

init_errors = pygame.init()
if init_errors[1] > 0:
    print(f'[!] Encountered {init_errors[1]} errors during initialization, exiting...')
    sys.exit(-1)
else:
    print('[+] Game initialized successfully')

pygame.display.set_caption('Py_Snale')
game_surface = pygame.display.set_mode((window_width, window_height))


dark = pygame.Color(10, 10, 10)
light_gray = pygame.Color(200, 200, 200)
orange = pygame.Color(255, 165, 0)
purple = pygame.Color(128, 0, 128)
cyan = pygame.Color(0, 255, 255)


game_clock = pygame.time.Clock()


snake_position = [200, 60]
snake_segments = [[200, 60], [190, 60], [180, 60]]


food_position = [random.randrange(1, (window_width//20)) * 20, random.randrange(1, (window_height//20)) * 20]
food_present = True

move_direction = 'RIGHT'
next_direction = move_direction


current_score = 0


def end_game():
    font = pygame.font.SysFont('verdana', 90)
    end_surface = font.render('GAME OVER', True, orange)
    end_rect = end_surface.get_rect()
    end_rect.midtop = (window_width/2, window_height/4)
    game_surface.fill(dark)
    game_surface.blit(end_surface, end_rect)
    display_score(0, cyan, 'arial', 20)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()


def display_score(position, color, font_type, size):
    score_font = pygame.font.SysFont(font_type, size)
    score_surface = score_font.render('Score: ' + str(current_score), True, color)
    score_rect = score_surface.get_rect()
    if position == 1:
        score_rect.midtop = (window_width/10, 20)
    else:
        score_rect.midtop = (window_width/2, window_height/1.2)
    game_surface.blit(score_surface, score_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                next_direction = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                next_direction = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                next_direction = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                next_direction = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))


    if next_direction == 'UP' and not move_direction == 'DOWN':
        move_direction = 'UP'
    if next_direction == 'DOWN' and not move_direction == 'UP':
        move_direction = 'DOWN'
    if next_direction == 'LEFT' and not move_direction == 'RIGHT':
        move_direction = 'LEFT'
    if next_direction == 'RIGHT' and not move_direction == 'LEFT':
        move_direction = 'RIGHT'


    if move_direction == 'UP':
        snake_position[1] -= 20
    if move_direction == 'DOWN':
        snake_position[1] += 20
    if move_direction == 'LEFT':
        snake_position[0] -= 20
    if move_direction == 'RIGHT':
        snake_position[0] += 20


    snake_segments.insert(0, list(snake_position))
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        current_score += 1
        food_present = False
    else:
        snake_segments.pop()


    if not food_present:
        food_position = [random.randrange(1, (window_width//20)) * 20, random.randrange(1, (window_height//20)) * 20]
    food_present = True


    game_surface.fill(dark)
    for pos in snake_segments:
        pygame.draw.rect(game_surface, orange, pygame.Rect(pos[0], pos[1], 20, 20))

    pygame.draw.rect(game_surface, light_gray, pygame.Rect(food_position[0], food_position[1], 20, 20))


    if snake_position[0] < 0 or snake_position[0] > window_width-20 or snake_position[1] < 0 or snake_position[1] > window_height-20:
        end_game()
    for block in snake_segments[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            end_game()

    display_score(1, cyan, 'arial', 20)
    pygame.display.update()
    game_clock.tick(game_speed)
