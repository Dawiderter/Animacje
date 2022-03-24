import pygame
import model

#Podstawowe rozmiary
BALL_RADIUS = 40
TRACK_LENGTH_IN_PX = 350
MAX_ROWS_BEFORE_SCROLLING = 5

MARGIN = 10
CONTOURS_WIDTH = 3
SCROLL_DELTA = 10

#Stałe modelu
DEFAULT_VEL = model.DEFAULT_VEL
ERROR_STEP = model.ERROR_STEP
MAX_ERROR = model.MAX_ERROR
RANDOMNESS_FACTOR = model.RANDOMNESS_FACTOR

DEFAULT_COL = (128, 128, 200)
DEFAULT_NUM = model.DEFAULT_NUM

#Informacje o komórkach
ROWS = DEFAULT_NUM + 1

CELLS_VEL = model.CELLS_VEL
CELLS = model.CELLS

CELL_COLOR_STEP = 200//CELLS
CELLS_COL = [(DEFAULT_COL[0] - i*CELL_COLOR_STEP, DEFAULT_COL[1] + i*CELL_COLOR_STEP, DEFAULT_COL[2]) for i in range(-DEFAULT_NUM,CELLS-DEFAULT_NUM)]

#Wyliczone rozmiary
CELL_HEIGHT = 2*BALL_RADIUS + 2*MARGIN
CELL_WIDTH = 2*BALL_RADIUS + TRACK_LENGTH_IN_PX + 2*MARGIN

TEXT_SIZE = CELL_HEIGHT // 6
TITLE = TEXT_SIZE + 2*MARGIN
TEXT_SPACE = TEXT_SIZE * 7 + 2*MARGIN

CELL_WIDTH_TEXT = CELL_WIDTH + 2*MARGIN + TEXT_SPACE

TRUE_HEIGHT = TITLE + (CELL_HEIGHT + 2*MARGIN) * min(CELLS, ROWS)
HEIGHT = min(TRUE_HEIGHT, TITLE + int((CELL_HEIGHT + 2*MARGIN)*(MAX_ROWS_BEFORE_SCROLLING+0.5)))
WIDTH = (CELL_WIDTH_TEXT + 2*MARGIN) * (CELLS // ROWS + 1)

#Fizyczne wielkości
TRACK_LENGTH = model.TRACK_LENGTH
PX_TO_M_FACTOR = TRACK_LENGTH_IN_PX / TRACK_LENGTH
TIMESTEP = 0.01
AUTO_RUN_STEP = 1.0 / 60.0

#Kolory
UI_COLOR = (50, 50, 50)
BALL_COLOR = (0, 0, 255)
RIGHT_COLOR = (42,255,0)
LEFT_COLOR = (255,42,0)
BACKGROUND_COLOR = (240, 240, 245)

#Łamana strzałki
ARROW_TEMPLATE = [(0, 10), (15, 10), (15, 20), (30, 0), (15, -20), (15, -10), (0, -10)]
ARROW = [(0.8 * x, 0.8 * y) for (x, y) in ARROW_TEMPLATE]
INV_ARROW = [(-x, y) for (x, y) in ARROW]

#Siatka
GRID_SIZE = CELL_WIDTH//25
GRID_COLOR = (235, 235, 235)
GRID = pygame.surface.Surface((CELL_WIDTH, CELL_HEIGHT))
GRID.fill(BACKGROUND_COLOR)
for x in range(0,CELL_WIDTH,GRID_SIZE):
    for y in range(0,CELL_HEIGHT, GRID_SIZE):
        pygame.draw.rect(GRID, GRID_COLOR, (x,y,GRID_SIZE, GRID_SIZE), 1)

Cache  = model.Cache

#Przyporządkowanie poprawnego koloru w zależności od znaku
def assign_correct_color(expr : float):
    if expr > 0.00005:
        return RIGHT_COLOR
    elif expr < -0.00005:
        return LEFT_COLOR
    else:
        return UI_COLOR

#Narysowanie całej komórki na ekranie
#grid + obwódka + kula + parametry + względne parametry
def draw_cell(screen : pygame.surface.Surface, num : int,  t : float, font : pygame.font.Font, scroll : int):
    v = CELLS_VEL[num]

    #Bezwzględna pozycja komórki na ekranie
    cell_top_left_corner = ((CELL_WIDTH_TEXT + 2*MARGIN)*(num // ROWS) + MARGIN, -scroll + (CELL_HEIGHT+2*MARGIN)*(num % ROWS) + MARGIN + TITLE)
    ball_start_pos = (cell_top_left_corner[0] + MARGIN + BALL_RADIUS, cell_top_left_corner[1] + MARGIN + BALL_RADIUS)

    (dir, ball_curr_rel_pos, number_of_boinks) = Cache[num]
    ball_curr_rel_pos = round(ball_curr_rel_pos * PX_TO_M_FACTOR)

    default_state = (Cache[DEFAULT_NUM][0], round(Cache[DEFAULT_NUM][1] * PX_TO_M_FACTOR), Cache[DEFAULT_NUM][2])

    text_rel_pos = (cell_top_left_corner[0] + CELL_WIDTH + MARGIN, cell_top_left_corner[1] + MARGIN)
    vel_text = font.render(f"V₀: {v:.2f} [m/s]", True, UI_COLOR)
    rel_vel_text = font.render(f"{(v-DEFAULT_VEL):+.2f}", True, CELLS_COL[num])
    pos_text = font.render(f"X: {(ball_curr_rel_pos/PX_TO_M_FACTOR):.2f} [m]", True, UI_COLOR)
    rel_pos_text = font.render(f"{(ball_curr_rel_pos - default_state[1])/PX_TO_M_FACTOR:+.2f}", True, assign_correct_color(ball_curr_rel_pos - default_state[1]))
    nob_text = font.render(f"B: {number_of_boinks}", True, UI_COLOR)
    rel_nob_text = font.render(f"{number_of_boinks - default_state[2]:+}", True, assign_correct_color(number_of_boinks - default_state[2]))

    screen.blit(GRID, cell_top_left_corner)
    pygame.draw.rect(screen, UI_COLOR, (cell_top_left_corner[0], cell_top_left_corner[1], CELL_WIDTH, CELL_HEIGHT), CONTOURS_WIDTH)
    pygame.draw.circle(screen, CELLS_COL[num], (ball_start_pos[0] + ball_curr_rel_pos, ball_start_pos[1]), BALL_RADIUS, CONTOURS_WIDTH)
    if dir == 1:
        pygame.draw.polygon(screen, RIGHT_COLOR, [(x*v + ball_start_pos[0] + ball_curr_rel_pos, y + ball_start_pos[1]) for (x, y) in ARROW], CONTOURS_WIDTH)
    elif dir == -1:
        pygame.draw.polygon(screen, LEFT_COLOR, [(x*v + ball_start_pos[0] + ball_curr_rel_pos, y + ball_start_pos[1]) for (x, y) in INV_ARROW], CONTOURS_WIDTH)
    screen.blit(vel_text, text_rel_pos)
    screen.blit(rel_vel_text, (text_rel_pos[0] + int(TEXT_SPACE*0.8), text_rel_pos[1]))
    screen.blit(pos_text, (text_rel_pos[0], text_rel_pos[1] + MARGIN + TEXT_SIZE))
    screen.blit(rel_pos_text, (text_rel_pos[0] + int(TEXT_SPACE*0.8), text_rel_pos[1] + MARGIN + TEXT_SIZE))
    screen.blit(nob_text, (text_rel_pos[0], text_rel_pos[1] + 2*(MARGIN + TEXT_SIZE)))
    screen.blit(rel_nob_text, (text_rel_pos[0] + int(TEXT_SPACE*0.8), text_rel_pos[1] + 2*(MARGIN + TEXT_SIZE)))


def main():
    global WIDTH, HEIGHT

    pygame.init()

    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Symulacja')
    font = pygame.font.SysFont('times', TEXT_SIZE)

    FPS = pygame.time.Clock()
    pygame.key.set_repeat(int(1000*TIMESTEP))
 
    running = True
    t = 0
    auto_run = False
    scroll = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not auto_run:
                    t = t + TIMESTEP
                elif event.key == pygame.K_LEFT and not auto_run:
                    t = t - TIMESTEP
                elif event.key == pygame.K_UP:
                    scroll = min(max(0,scroll - SCROLL_DELTA), TRUE_HEIGHT - HEIGHT)
                elif event.key == pygame.K_DOWN:
                    scroll = min(max(0,scroll + SCROLL_DELTA), TRUE_HEIGHT - HEIGHT)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    auto_run = not auto_run
                elif event.key == pygame.K_0 and not auto_run:
                    t = 0
                elif event.key == pygame.K_1 and not auto_run:
                    t = 4
                elif event.key == pygame.K_2 and not auto_run:
                    t = 15 
                elif event.key == pygame.K_3 and not auto_run:
                    t = 30 
                elif event.key == pygame.K_4 and not auto_run:
                    t = 60  
        
        if auto_run:
            t = t + AUTO_RUN_STEP

        screen.fill(BACKGROUND_COLOR)
        model.update_pos(t)
        for i in range(CELLS):
            draw_cell(screen, i, t, font, scroll)

        (known_dir, delta_x, delta_b) = model.calculate_error()

        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, WIDTH, TITLE))
        t_text = font.render(f"t = {t:.2f} [s]  δV = ±{MAX_ERROR:.2f} [m/s]  δX = {delta_x:.2f} [m]  δB = ±{delta_b:.2f}  zwrot? = {known_dir}", True, UI_COLOR)
        hint_text = font.render(f"Strzałki - czas i scroll   Spacja - auto   0, 1, 2, 3, 4 - predefiniowany czas", True, UI_COLOR)
        screen.blit(t_text, (MARGIN, TITLE//2 - TEXT_SIZE//2))
        screen.blit(hint_text, (WIDTH - TEXT_SIZE*35, TITLE//2 - TEXT_SIZE//2))
        
        #print(FPS.get_fps())
        pygame.display.update()
        FPS.tick(60)

if __name__=="__main__":
    main()