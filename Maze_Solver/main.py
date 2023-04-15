from matrix_generator import small_matrix, matrix, big_matrix
from solvers import exe_largura, exe_profund
from graphics import *
from time import perf_counter

if __name__ == "__main__":

    maze_list = [small_matrix, matrix, big_matrix]
    solver_list = [exe_largura, exe_profund]

    user_input = []
    user_input.append(menu_1(user_input))
    user_input.append(menu_2(user_input))

    start_counter = perf_counter()
    solution, visited = solver_list[user_input[1] -
                                    1](maze_list[user_input[0]-1])
    perf_time = perf_counter() - start_counter
    display_solution(maze_list[user_input[0]-1], visited, solution)
    popup_perf("Tempo de execução: " + str(round(perf_time*1000, 3)) + "ms")
