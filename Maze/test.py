import pygame
import const
import Grid as GR
import numpy
import re

START_POS = [(0, 0), (37, 37)] # Starting, goal positions
restart = True
while restart:
    # -------- Init -----------
    maze = GR.Grid(const.grid_size)
    maze.start_end_pos(START_POS[0], START_POS[1])
    pygame.init()
    screen = pygame.display.set_mode(const.WINDOW_SIZE)
    pygame.display.set_caption("Maze")
    clock = pygame.time.Clock()
    # -------- Main Program Loop -----------
    done = False
    clicked = False
    selected = None
    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                # User clicks the mouse. Get the position
                try:
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    assert (pos[0] < const.WINDOW_SIZE[0] and pos[1] < const.WINDOW_SIZE[1])
                    assert (pos[1] < const.WINDOW_SIZE[1] and pos[0] < const.WINDOW_SIZE[0])
                    row, column = const.row_col_pos(pos[0], pos[1])

                    #print(row)
                    #print(column)

                    if row != const.grid_size and column != const.grid_size: # Happnes when clicked on the absolute edge
                        # Check if starting/goal position was clicked on
                        print(f"Clicked on color:{maze.grid[row, column]}")
                        if clicked and maze.grid[row, column] == const.WHITE: # place starting/goal position
                            #print("Placing start/goal")
                            START_POS[selected] = (row, column)
                            maze.start_end_pos(START_POS[0], START_POS[1])
                            clicked = False
                            selected = None
                        elif maze.grid[row, column] != const.WHITE and maze.grid[row, column] != const.RED: #clicked on starting/goal pos
                            #print("Clicked on start/goal")
                            clicked = True
                            selected = (0 if (row, column) == START_POS[0] else 1)
                            maze.grid[row, column] = const.WHITE
                        else:# place/remove obstacled depending on mouse click
                            maze.grid[row, column] = (const.RED if pygame.mouse.get_pressed()[0] else const.WHITE)
                except AttributeError:
                    print("AttributeError")
                    maze.grid[row, column] = (const.RED if pygame.mouse.get_pressed()[0] else const.WHITE)

        screen.fill(const.COLORS[const.BLACK])
        # Code here for ALGO - Constantly Updated
        # Start another thread, that will be running the chosen
        # algo, which will be sending positions to this thread into
        # queue -> adding colors where the algorithms is passing trough
        # accordingly -> different color for different algo
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP_ENTER]:
            print("Not implemented yet, going to restart")
            break
        # Draw the grid
        maze.grid_update(screen)
        clock.tick(60)
pygame.quit()
quit()







