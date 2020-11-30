# -*- coding: utf-8 -*-
import pygame as pg
from PrisonersDilemma import PrisonersDilemma, Strategy
from RectangularGrid import RectangularGrid

"""
for the graphical representation of the simulations
"""

# sets up the screen (dimensions, title, background color)
def setup_screen(screen_dimensions, background_colour):
    """ some things for the graphics....
    """
    pg.init()
    screen = pg.display.set_mode((screen_dimensions[1], screen_dimensions[0]))
    pg.display.set_caption("Conway's Game of Life")
    screen.fill(background_colour)
    pg.display.flip()
    return screen


def draw_update(screen, grid):
    """ updates the display according the the grid
    """
    green = (0, 255, 0)
    red = (255, 0, 0)
    black = (0, 0, 0)

    for i in range(grid.height):
        for j in range(grid.width):

            # define top-left pixel of cell
            tup = (i * 16, j * 16, 16, 16)

            # determine cell colouring
            player = grid.grid[i][j]
            if player:
                if player.strategy == Strategy.cooperate:
                    pg.draw.rect(screen, green, tup, 0)
                elif player.strategy == Strategy.defect:
                    pg.draw.rect(screen, red, tup, 0)
                else:
                    pg.draw.rect(screen, black, tup, 0)
            else:
                pg.draw.rect(screen, black, tup, 0)

    pg.display.flip()
    

def animation_2d(width, height, game = False, grid = False):
    """
    - width, height of animation grid 
    
    to make spesific setups you need to give this function a Dilemma(game) object
    and/or a RectangularGrid (grid)
    
    !note: if you give a RectangularGrid object the width and height will be ignored!
    """
    
    # init Dilemma and grid
    if not game:
        game = PrisonersDilemma(1.3, 1 ,0 , 0.1)
    if not grid:
        grid = RectangularGrid(width, height, game, p_needs = 0.25)
        
    grid_width = grid.width
    grid_height = grid.height
    
    # screen setup
    background_color = (0, 0, 0)
    cell_height = 16
    cell_width = 16
    screen_dimensions = (cell_width * grid_width, cell_height * grid_height)
    screen = setup_screen(screen_dimensions, background_color) 
    
    
    # first rendering
    draw_update(screen, grid)

    # simulation loop
    running = True
    counter = 0
    while running:
        # counter to prevent infinite loop
        # why do we need this??? (yannik)
        counter += 1
        if counter >= 100000:
            running = False

        # group updates together to speed up visualization
        for i in range(50):
            grid.update_player(game)
        draw_update(screen, grid)

        # proper closing of the window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                

                
if __name__ == "__main__":
    game = PrisonersDilemma(1.3, 1 ,0 , 0.1)
    animation_2d(30, 40, game)
    
    

    
    
"""
examples:
    
# migration
game = PrisonersDilemma(1.3, 1 ,0 , 0.1)
migration(game)
# asymetric mygration  
ame = AsPrisonersDilemma(1.5, 1 ,0 , 0.1)
migration(game)

"""
    
    
    
    
    
    
    
    