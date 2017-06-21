# Sharon Gao, 2017
# CHIP-8 Interpreter v1.0
import sys
import pygame
from pygame import gfxdraw, Rect
import mychip8
pygame.init()

def mainloop(game_file_name):
    WIDTH = 64
    HEIGHT = 32
    resolution = 64 * 10, 32 * 10
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    pixel_color_state = [BLACK, WHITE]
    screen_display = pygame.display.set_mode(resolution)
    screen_display.fill(BLACK)
    
    # -----------------
    # | 1 | 2 | 3 | 4 |
    #------------------
    # | Q | W | E | R |
    # -----------------
    # | A | S | D | F |
    # -----------------
    # | Z | X | C | V |
    # -----------------
    key_input = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
    pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
    pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
    pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v]
    
    chip8 = mychip8.MyChip8()
    chip8.initialize()
    chip8.load_game_rom(game_file_name)
    
    while True:
        chip8.emulate_cycle()
        if (chip8.draw_flag == True):
            draw_pixels(screen_display, WIDTH, HEIGHT, pixel_color_state, chip8)
        events = pygame.event.get()
        get_key_press(events, key_input, chip8)

def draw_pixels(screen_display, width, height, pixel_color_state, chip8):
    # Draw 32 x 32 rectangles for each pixel
    for x in range(width):
        for y in range(height):
            screen_display.fill(pixel_color_state[chip8.screen_pixel_states[x + (y * width)]], Rect(x * 10, y * 10, 10, 10))
    pygame.display.flip() # Update screen display
    chip8.draw_flag = False # Set draw flag to False
    
def get_key_press(events, keys, chip8):
    for event in events:
        key_state = -1
        if event.type == pygame.KEYDOWN: # On key press
        	key_state = 1 # Set key state to pressed
        elif event.type == pygame.KEYUP: # On key release
        	key_state = 0 # Set key state to not pressed
        elif event.type == pygame.QUIT:
        	sys.exit(0)

        if key_state == 0 or key_state == 1:
        	if event.key in keys:
        		key_pressed_index = keys.index(event.key)
        		chip8.keys[key_pressed_index] = key_state
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Missing CHIP-8 game file.")
        sys.exit(0)
    else:
        game_file_name = sys.argv[1]
        mainloop(game_file_name)