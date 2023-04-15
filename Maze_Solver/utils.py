def get_initial_state(mat) -> tuple:
    """
    Encontra 2 na matriz
    return: (row, column)
    """
    for i, row in enumerate(mat):
        for j, num in enumerate(row):
            if num == 2:
                return (i, j)


def in_matrix(mat, i, j) -> bool:
    """
    Checa se coordenadas estao dentro das dimensoes da matriz
    return: bool
    """
    n = len(mat)
    if (0 <= i < n) and (0 <= j < n):
        return True
    else:
        return False


def successor(mat, state) -> list:
    """
    Possiveis acoes que o agente pode realizar
    return: list(possible_moves)
    """
    possible_moves = []
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for di, dj in moves:
        ni = state[0] + di
        nj = state[1] + dj
        if in_matrix(mat, ni, nj):
            if (mat[ni][nj] != 0):
                possible_moves.append((ni, nj))

    return possible_moves


def is_objective(mat, state) -> bool:
    """
    Determina se o estado e objetivo ou nao
    return: bool
    """
    if mat[state[0]][state[1]] == 3:
        return True
    else:
        return False
