from solvers import *
from matrix_generator import matrix
import pygame
import time
import sys


def menu_1(user_input):
    while True:
        print()
        print("Seja bem vindo ao Solucionador de Labirintos!")
        print()
        print("Selecione o tamanho do Labirinto:")
        print("1 - Pequeno")
        print("2 - Médio")
        print("3 - Grande")
        escolha = int(input("Digite o número da opção desejada: "))

        if escolha in range(1, 4):
            return escolha
        else:
            print("Opção inválida. Digite novamente.")


def menu_2(user_input):
    while True:
        print()
        print("Selecione o tipo de algoritmo solucionador:")
        print("1 - Busca em Largura")
        print("2 - Busca em Profundidade")
        escolha = int(input("Digite o número da opção desejada: "))

        if escolha in range(1, 3):
            return escolha
        else:
            print("Opção inválida. Digite novamente.")


def final_msg():
    print()
    print("Obrigado por participar!")


def popup_perf(msg):
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    screen = pygame.display.set_mode((400, 140))
    font = pygame.font.SysFont(None, 32)
    text = font.render(msg, True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (200, 70)

    screen.fill(WHITE)
    screen.blit(text, text_rect)
    pygame.display.flip()
    final_msg()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def display_solution(matrix, visited, solution):
    """
    Grafico que apresenta o labirinto, a busca, e sua solucao de acordo com o solver

    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255, 200, 0)
    BLUE = (0, 0, 255)
    GREY = (69, 69, 69)

    pygame.init()

    size = (len(matrix[0]) * 30, len(matrix) * 30)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Maze Solver")

    done = False

    clock = pygame.time.Clock()

    for position in visited:  # Start with displaying the visited path slowly

        screen.fill(BLACK)  # Set the screen background

        for row in range(len(matrix)):  # Draw the maze
            for column in range(len(matrix[0])):
                if matrix[row][column] == 1:
                    color = WHITE
                elif matrix[row][column] == 3:
                    color = BLUE
                else:
                    color = BLACK
                pygame.draw.rect(
                    screen, color, [(30 * column), (30 * row), 30, 30])

        # Draw the visited path
        for pos in visited[:visited.index(position)+1]:
            row, col = pos
            pygame.draw.rect(screen, YELLOW, [(30 * col), (30 * row), 30, 30])

        pygame.display.flip()  # Update the screen

        pygame.time.wait(100)  # Slow down the display of the visited path

    for position in solution:

        screen.fill(BLACK)  # Set the screen background

        for row in range(len(matrix)):  # Draw the maze
            for column in range(len(matrix[0])):
                if matrix[row][column] == 1:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.rect(
                    screen, color, [(30 * column), (30 * row), 30, 30])

        for pos in visited:  # Draw the visited path
            row, col = pos
            pygame.draw.rect(screen, GREY, [(30 * col), (30 * row), 30, 30])

        # Draw the solution path
        for pos in solution[:solution.index(position)+1]:
            row, col = pos
            pygame.draw.rect(screen, BLUE, [(30 * col), (30 * row), 30, 30])

        start_row, start_col = solution[0]
        end_row, end_col = solution[-1]
        pygame.draw.rect(
            screen, GREEN, [(30 * start_col), (30 * start_row), 30, 30])
        pygame.draw.rect(screen, RED, [(30 * end_col), (30 * end_row), 30, 30])

        pygame.display.flip()  # Update the screen

        clock.tick(60)

    # Close the window and quit
    time.sleep(2)
    pygame.quit()


def print_matrix(mat, text):
    print(text)
    for row in mat:
        print(row)


def print_solved_path(mat, solver=exe_largura):
    print_matrix(mat, 'INITIAL MATRIX')
    path = solver(mat)
    for row, col in path:
        mat[row][col] = 9
    print_matrix(mat, 'SOLVED MATRIX')


def matrix_rgb(mat):
    """Convert matrix values into RGB"""
    # Define a dictionary to map values to colors
    color_map = {0: (0, 0, 0),  # Black
                 1: (255, 255, 255),  # White
                 2: (0, 255, 0),  # Green
                 3: (255, 0, 0),  # Red
                 9: (128, 128, 128)}  # Grey

    # Create a new matrix with the same shape as the input matrix
    new_mat = [[None for _ in range(len(mat[0]))]
               for _ in range(len(mat))]

    # Replace each value in the input matrix with its corresponding color
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            new_mat[i][j] = color_map[mat[i][j]]

    return new_mat
