import pygame
import random

# Function to run the 2048 game with a 16x16 grid
def run_2048_game3():
    pygame.init()

    # Initial setup for a larger grid
    TILE_SIZE = 35  # Smaller tiles for a 16x16 grid
    GRID_SIZE = 16
    WIDTH = TILE_SIZE * GRID_SIZE + 40  # Adjusted width for grid and padding
    HEIGHT = WIDTH + 150  # Adjusted height for score, high score, and timer display
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Merge Matrix')
    timer = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font('PlayfairDisplay-Bold.otf', 18)  # Smaller font for tiles

    # 2048 game color library
    colors = {
        0: (204, 192, 179),
        2: (77, 205, 128),
        4: (170, 190, 210),
        8: (242, 177, 121),
        16: (255, 102, 0),
        32: (246, 124, 95),
        64: (246, 94, 59),
        128: (237, 207, 114),
        256: (237, 204, 97),
        512: (237, 200, 80),
        1024: (237, 197, 63),
        2048: (237, 194, 46),
        'light text': (249, 246, 242),
        'dark text': (119, 110, 101),
        'other': (0, 0, 0),
        'bg': (106, 90, 205)
    }

    # Game variables
    board_values = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    game_over = False
    direction = ''
    score = 0
    
    # High score management
    try:
        with open('high_score_level3', 'r') as file:
            init_high = int(file.readline())
    except FileNotFoundError:
        init_high = 0
        
    high_score = init_high

    # Timer variables
    timer_duration = 15  # 15 seconds timer
    time_left = timer_duration
    start_ticks = pygame.time.get_ticks()

    def draw_over():
        # Calculate dimensions and position for the overlay rectangle
        rect_width = 300
        rect_height = 100
        rect_x = (WIDTH - rect_width) // 2
        rect_y = (HEIGHT - rect_height) // 2

        # Draw the overlay rectangle
        pygame.draw.rect(screen, 'black', [rect_x, rect_y, rect_width, rect_height], 0, 10)

        # Render the text
        game_over_text1 = font.render('Game Over!', True, 'white')
        game_over_text2 = font.render('Press Enter to Restart', True, 'white')

        # Calculate positions for centering the text
        text1_rect = game_over_text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 15))
        text2_rect = game_over_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 15))

        # Blit the text onto the screen
        screen.blit(game_over_text1, text1_rect)
        screen.blit(game_over_text2, text2_rect)


    # Move and merge tiles for each direction
    def take_turn(direc, board, current_score):
        merged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        if direc == 'UP':
            for j in range(GRID_SIZE):
                for i in range(1, GRID_SIZE):
                    if board[i][j] != 0:
                        row = i
                        while row > 0 and board[row - 1][j] == 0:
                            board[row - 1][j], board[row][j] = board[row][j], 0
                            row -= 1
                        if row > 0 and board[row - 1][j] == board[row][j] and not merged[row - 1][j]:
                            board[row - 1][j] *= 2
                            current_score += board[row - 1][j]
                            board[row][j] = 0
                            merged[row - 1][j] = True

        elif direc == 'DOWN':
            for j in range(GRID_SIZE):
                for i in range(GRID_SIZE - 2, -1, -1):
                    if board[i][j] != 0:
                        row = i
                        while row < GRID_SIZE - 1 and board[row + 1][j] == 0:
                            board[row + 1][j], board[row][j] = board[row][j], 0
                            row += 1
                        if row < GRID_SIZE - 1 and board[row + 1][j] == board[row][j] and not merged[row + 1][j]:
                            board[row + 1][j] *= 2
                            current_score += board[row + 1][j]
                            board[row][j] = 0
                            merged[row + 1][j] = True

        elif direc == 'LEFT':
            for i in range(GRID_SIZE):
                for j in range(1, GRID_SIZE):
                    if board[i][j] != 0:
                        col = j
                        while col > 0 and board[i][col - 1] == 0:
                            board[i][col - 1], board[i][col] = board[i][col], 0
                            col -= 1
                        if col > 0 and board[i][col - 1] == board[i][col] and not merged[i][col - 1]:
                            board[i][col - 1] *= 2
                            current_score += board[i][col - 1]
                            board[i][col] = 0
                            merged[i][col - 1] = True

        elif direc == 'RIGHT':
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE - 2, -1, -1):
                    if board[i][j] != 0:
                        col = j
                        while col < GRID_SIZE - 1 and board[i][col + 1] == 0:
                            board[i][col + 1], board[i][col] = board[i][col], 0
                            col += 1
                        if col < GRID_SIZE - 1 and board[i][col + 1] == board[i][col] and not merged[i][col + 1]:
                            board[i][col + 1] *= 2
                            current_score += board[i][col + 1]
                            board[i][col] = 0
                            merged[i][col + 1] = True

        return board, current_score

    # Spawn in new pieces
    def new_pieces(board):
        count = 0
        full = False
        while any(0 in row for row in board) and count < 1:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            if board[row][col] == 0:
                count += 1
                board[row][col] = 4 if random.randint(1, 10) == 10 else 2
        if count < 1:
            full = True
        return board, full

    # Draw the board with smaller tiles
    def draw_board():
        pygame.draw.rect(screen, colors['bg'], [0, 0, WIDTH, WIDTH], 0, 10)
        score_text = font.render(f'Score: {score}', True, 'white')
        high_score_text = font.render(f'High Score: {high_score}', True, 'white')
        timer_text = font.render(f'Time Left: {time_left}', True, 'white')
        screen.blit(score_text, (20, WIDTH + 10))  # Left-aligned
        screen.blit(high_score_text, (20, WIDTH + 50))  # Left-aligned
        screen.blit(timer_text, (20, WIDTH + 90))  # Left-aligned

    # Draw tiles for 16x16 grid
    def draw_pieces(board):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = board[i][j]
                value_color = colors['light text'] if value > 8 else colors['dark text']
                color = colors.get(value, colors['other'])
                pygame.draw.rect(screen, color, [j * TILE_SIZE + 20, i * TILE_SIZE + 20, TILE_SIZE - 5, TILE_SIZE - 5], 0, 5)
                if value > 0:
                    value_len = len(str(value))
                    tile_font = pygame.font.Font('freesansbold.ttf', 36 - (2 * value_len))
                    value_text = tile_font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2 + 20, i * TILE_SIZE + TILE_SIZE // 2 + 20))
                    screen.blit(value_text, text_rect)

    # Game loop
    run = True
    new_board, full = new_pieces(board_values)

    while run:
        timer.tick(fps)
        screen.fill((106, 90, 205))
        draw_board()
        draw_pieces(board_values)

        # Timer countdown logic only when the game is not over
        if not game_over:
            seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
            time_left = max(0, timer_duration - seconds_passed)
            if time_left <= 0:
                game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        direction = 'UP'
                    elif event.key == pygame.K_DOWN:
                        direction = 'DOWN'
                    elif event.key == pygame.K_LEFT:
                        direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        direction = 'RIGHT'
                    if direction:
                        board_values, score = take_turn(direction, board_values, score)
                        new_board, full = new_pieces(board_values)
                        if full:
                            game_over = True
                        direction = ''
                elif event.key == pygame.K_RETURN:
                    # Restart game logic
                    board_values = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                    score = 0
                    game_over = False
                    time_left = timer_duration
                    start_ticks = pygame.time.get_ticks()
                    new_pieces(board_values)

        if game_over:
            draw_over()
            if score > high_score:
                high_score = score
                with open('high_score_level3', 'w') as file:
                    file.write(str(high_score))

        pygame.display.flip()

    pygame.quit()
