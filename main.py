import pygame
import pygame.camera
from pygame.locals import *

from init import *
import utility as util
from handle_file_maze import *
from handle_maze import *
from handle_visualize import make_image, Video
from algorithms.algorithm import *
# import sys
# sys.path.insert(0, './alogorithms')
# # importing the hello
# from algorithm import *
# Build all need to visualization
"""
Description: Node is cell in matrix, it has another state with different color:
- White: Can go
- Black: Wall
- Orange: Start
- Turquoise: End
- Green: Process find way
- Purple: Correct way
- Yellow: Bonus point
"""
def run():
    levels, files = list_file()

    # print(levels)
    
    for level in levels:
        for file in files[level]:
            maze, bonus_points, pickup_points, portal_points = read_file("./input/" + level + "/" + file)
            
            ROWS = len(maze)
            COLS = len(maze[0])
            WIDTH = COLS * SIZE
            HEIGHT = ROWS * SIZE
            way = []
            cost = 0
            start = None
            end = None

            algs = []
            no_bonus_alg = ["dfs","bfs","ucs","gbfs_heuristic_1","gbfs_heuristic_2","astar_heuristic_1","astar_heuristic_2"]
            bonus_alg = ["algo1", "algo2"]
            if(level == "level_1"):
                algs = no_bonus_alg
            else:
                algs = bonus_alg
            for alg in algs:
                grid = make_grid(ROWS, COLS)
                start, end = merge_maze_grid(maze, grid,ROWS,COLS)
                bonus_queue = merge_bonus_grid(bonus_points, grid)
                pickup_queue = merge_pickups_grid(pickup_points,grid)
                portal_queue = merge_portal_grid(portal_points,grid)
                if(not level == "level_1"):
                    util.update_bonus_grid(grid, bonus_points, portal_points)
                    util.update_distance_grid(grid, pickup_points, portal_points)
                for row in grid:
                    for node in row:
                        node.update_neighbors(grid)            
                
                pygame.display.set_caption("Simulation of finding the way")
                # SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.HIDDEN)
                SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
                is_alg_do = False # kiem tra co thuat toan nao chay  khong
                if level == "level_1":
                    if(alg == "dfs"):
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way, cost = algorithm_dfs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
                        is_alg_do = True
                    elif(alg== "bfs"):
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way,cost = algorithm_bfs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
                        is_alg_do = True                        
                    elif(alg == "ucs"):
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way, cost = algorithm_ucs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
                        is_alg_do = True
                    elif(alg == "gbfs_heuristic_1"):
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way, cost =algorithm_greedy_bfs_heuristic_1(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
                        is_alg_do = True
                    elif(alg == "gbfs_heuristic_2"):
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way, cost =algorithm_greedy_bfs_heuristic_2(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
                        is_alg_do = True
                    
                    elif(alg == "astar_heuristic_1"):
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way, cost = algorithm_astar_heuristic_1(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
                        is_alg_do = True
                    else:
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way, cost = algorithm_astar_heuristic_2(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
                        is_alg_do = True                        
                elif level == "level_2":
                    if(alg == "algo1"):
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way, cost = algorithm_handle_all(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, bonus_points, pickup_points, portal_points, start, end,clock)
                        is_alg_do = True
                        
                    if(alg == "algo2"):
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way, cost = algorithm_bonus_astar(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, bonus_queue, start, end, clock)
                        is_alg_do = True
                elif level == "level_3":
                    if(alg == "algo2"):
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way, cost = algorithm_handle_bonus_pickup(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, bonus_queue, pickup_queue, start, end, clock)
                        is_alg_do = True
                    if(alg == "algo1"):
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way, cost = algorithm_handle_all(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, bonus_points, pickup_points, portal_points, start, end,clock)
                        is_alg_do = True
                elif level == "advance":
                    if(alg == "algo1"):
                        print("Start ", alg, " with maze", file, " in folder", level )
                        way, cost = algorithm_handle_all(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, bonus_points, pickup_points, portal_points, start, end,clock)
                        is_alg_do = True
                if(is_alg_do):
                    # print("Done ", alg, " with maze", file, " in folder", level )
                    dir_output = ""
                    if(alg.split("_")[0] == "gbfs" or alg.split("_")[0] == "astar"):
                        dir_output = level + "/" + file.split(".")[0] + "/" + alg.split("_")[0]
                    else:
                        dir_output = level + "/" + file.split(".")[0] + "/" + alg
                    create_folder(dir_output)               
                    write_file(dir_output + "/" + alg + ".txt", cost )
                    video.make_mp4(dir_output+ "/" + alg)
                    video.destroy_png()
                    maze, bonus_points, pickup_points, portal_points = read_file("./input/" + level + "/" + file)
                    make_image(maze,bonus_points, pickup_points, portal_points,start,end,way,DIR_OUTPUT + dir_output + "/" + alg )
    pygame.quit()
            
if __name__ == "__main__":
    video = Video((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    run()

    
    