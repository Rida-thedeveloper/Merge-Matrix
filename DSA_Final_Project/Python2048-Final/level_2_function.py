import pygame
import random

# Function to run the 2048 game for an 8x8 grid
def run_2048_game2():
    pygame.init()

    # Window dimensions for the 8x8 grid
    tile_size = 80
    padding = 10
    WIDTH = 8 * tile_size + 1 * padding  # Adjust width to account for padding between tiles
    HEIGHT = 8 * tile_size + 150  # Adjust height for extra elements like score and timer
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Merge Matrix')
    timer = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font('PlayfairDisplay-Bold.otf', 24)

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
        'bg':   (0, 128, 128)
    }

    # Game variables initialize
    board_values = [[0 for _ in range(8)] for _ in range(8)]
    game_over = False
    direction = ''
    score = 0

    # High score management
    try:
        with open('high_score_level2', 'r') as file:
            init_high = int(file.readline())
    except FileNotFoundError:
        init_high = 0
        
    high_score = init_high

    # Timer variables
    timer_duration = 20  # 20 seconds timer
    time_left = timer_duration  # Time left for the timer
    start_ticks = pygame.time.get_ticks()  # Starting tick

    # Draw game over and restart text
    def draw_over():
        overlay_width = 400
        overlay_height = 150
        overlay_x = (WIDTH - overlay_width) // 2
        overlay_y = (HEIGHT - overlay_height) // 2
        
        pygame.draw.rect(screen, 'orange', [overlay_x, overlay_y, overlay_width, overlay_height], 0, 10)
        
        # Center the text within the overlay
        game_over_text1 = font.render('Game Over!', True, 'white')
        game_over_text2 = font.render('Press Enter to Restart', True, 'white')
        
        text1_rect = game_over_text1.get_rect(center=(WIDTH // 2, overlay_y + 50))
        text2_rect = game_over_text2.get_rect(center=(WIDTH // 2, overlay_y + 100))
        
        screen.blit(game_over_text1, text1_rect)
        screen.blit(game_over_text2, text2_rect)


    # Take your turn based on direction
    def take_turn(direc, board, current_score):
        merged = [[False for _ in range(8)] for _ in range(8)]
        if direc == 'UP':
            for i in range(8):
                for j in range(8):
                    shift = 0
                    if i > 0:
                        for q in range(i):
                            if board[q][j] == 0:
                                shift += 1
                        if shift > 0:
                            board[i - shift][j] = board[i][j]
                            board[i][j] = 0
                        if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                                and not merged[i - shift - 1][j]:
                            board[i - shift - 1][j] *= 2
                            current_score += board[i - shift - 1][j]
                            board[i - shift][j] = 0
                            merged[i - shift - 1][j] = True

        elif direc == 'DOWN':
            for i in range(7, -1, -1):
                for j in range(8):
                    shift = 0
                    for q in range(i + 1, 8):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i + shift][j] = board[i][j]
                        board[i][j] = 0
                    if i + shift + 1 < 8:
                        if board[i + shift][j] == board[i + shift + 1][j] and not merged[i + shift][j] \
                                and not merged[i + shift + 1][j]:
                            board[i + shift + 1][j] *= 2
                            current_score += board[i + shift + 1][j]
                            board[i + shift][j] = 0
                            merged[i + shift + 1][j] = True

        elif direc == 'LEFT':
            for i in range(8):
                for j in range(8):
                    shift = 0
                    for q in range(j):
                        if board[i][q] == 0:
                            shift += 1
                    if shift > 0:
                        board[i][j - shift] = board[i][j]
                        board[i][j] = 0
                    if j - shift - 1 >= 0:
                        if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                                and not merged[i][j - shift]:
                            board[i][j - shift - 1] *= 2
                            current_score += board[i][j - shift - 1]
                            board[i][j - shift] = 0
                            merged[i][j - shift - 1] = True

        elif direc == 'RIGHT':
            for i in range(8):
                for j in range(7, -1, -1):
                    shift = 0
                    for q in range(j + 1, 8):
                        if board[i][q] == 0:
                            shift += 1
                    if shift > 0:
                        board[i][j + shift] = board[i][j]
                        board[i][j] = 0
                    if j + shift + 1 < 8:
                        if board[i][j + shift] == board[i][j + shift + 1] and not merged[i][j + shift] \
                                and not merged[i][j + shift + 1]:
                            board[i][j + shift + 1] *= 2
                            current_score += board[i][j + shift + 1]
                            board[i][j + shift] = 0
                            merged[i][j + shift + 1] = True
        return board, current_score

    # Spawn in new pieces randomly when turns start
    def new_pieces(board):
        count = 0
        full = False
        while any(0 in row for row in board) and count < 1:
            row = random.randint(0, 7)
            col = random.randint(0, 7)
            if board[row][col] == 0:
                count += 1
                if random.randint(1, 10) == 10:
                    board[row][col] = 4
                else:
                    board[row][col] = 2
        if count < 1:
            full = True
        return board, full

    # Draw background for the board
    def draw_board():
        pygame.draw.rect(screen, colors['bg'], [0, 0, WIDTH, 640], 0, 10)  # Adjusted width
        score_text = font.render(f'Score: {score}', True, 'white')
        high_score_text = font.render(f'High Score: {high_score}', True, 'white')
        timer_text = font.render(f'Time Left: {time_left}', True, 'white')  # Timer text
        screen.blit(score_text, (30, HEIGHT - 130))
        screen.blit(high_score_text, (30, HEIGHT - 100))
        screen.blit(timer_text, (30, HEIGHT - 70))  # Display timer below high score

    def draw_pieces(board):
        for i in range(8):  # Loop over 8 rows
            for j in range(8):  # Loop over 8 columns
                value = board[i][j]
                if value > 8:
                    value_color = colors['light text']
                else:
                    value_color = colors['dark text']
                if value <= 2048:
                    color = colors[value]
                else:
                    color = colors['other']
                pygame.draw.rect(screen, color, [j * tile_size + padding, i * tile_size + padding, tile_size - padding, tile_size - padding], 0, 5)
                if value > 0:
                    value_len = len(str(value))
                    font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j * tile_size + tile_size / 2, i * tile_size + tile_size / 2))
                    screen.blit(value_text, text_rect)
                    pygame.draw.rect(screen, 'black', [j * tile_size + padding, i * tile_size + padding, tile_size - padding, tile_size - padding], 5, 5)

    # Game loop
    run = True
    new_board, full = new_pieces(board_values)

    while run:
        timer.tick(fps)
        screen.fill( (0, 128, 128))
        draw_board()
        draw_pieces(board_values)

        # Timer countdown logic only when the game is not over
        if not game_over:
            seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000  # Seconds passed
            time_left = max(0, timer_duration - seconds_passed)  # Calculate time left
            if time_left <= 0:
                game_over = True  # Set game over when time runs out

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
                        board_values, score = take_turn(direction, board_values, score)  # Pass and receive score
                        new_board, full = new_pieces(board_values)
                        if full:
                            game_over = True
                        spawn_new = True
                elif event.key == pygame.K_RETURN:
                    # Restart game logic
                    board_values = [[0 for _ in range(8)] for _ in range(8)]
                    score = 0
                    game_over = False
                    time_left = timer_duration  # Reset timer
                    start_ticks = pygame.time.get_ticks()  # Reset starting ticks
                    new_pieces(board_values)

        if game_over:
            draw_over()
            # Check if the score is greater than the high score
            if score > high_score:
                high_score = score  # Update high score
                # Write the new high score to the file
                with open('high_score_level2', 'w') as file:
                    file.write(str(high_score))

        # Check if score exceeds 2048
        if score > 2048:
            # Render the exceed score message here
            score_exceed_msg = font.render('You have exceeded 2048!', True, 'red')
            screen.blit(score_exceed_msg, (70, 600))  # Adjusted position for the message

        pygame.display.flip()

    pygame.quit()


