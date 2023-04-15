from queue import Queue  # FIFO
from collections import deque  # LIFO
from utils import *


def exe_largura(mat) -> tuple:
    """
    Busca em Largura. 
    Retorna Tupla com lista de solucao e lista de caminhos visitados 
    """
    fila = Queue()
    head = get_initial_state(mat)
    fila.put(head)
    visited = {head: None}
    while not fila.empty():
        state = fila.get()
        if is_objective(mat, state):
            path = [state]
            parent = visited[state]
            while parent is not None:
                path.append(parent)
                parent = visited[parent]
            path.reverse()
            return path, list(visited.keys())
        successor_list = successor(mat, state)
        for branch in successor_list:
            if branch not in visited:
                visited[branch] = state
                fila.put(branch)

    return [], list(visited.keys())


def exe_profund(mat) -> tuple:
    """
    Busca em Profundidade. 
    Retorna Tupla com lista de solucao e lista de caminhos visitados 
    """
    pilha = deque()
    head = get_initial_state(mat)
    state = [head]
    last_state = head
    visitados = []
    pilha.append(state)
    while True:
        if not pilha:
            break
        state = pilha.pop()
        head = state[-1]
        if is_objective(mat, head):
            return state, visitados
        visitados.append(head)
        successor_list = successor(mat, head)
        if len(successor_list) >= 1:
            for i, branch in enumerate(successor_list):
                if branch not in state:
                    pilha.append(state + [branch])

    return [], visitados
