# Implementação BFS e DFS - Sistemas Inteligentes
Este projeto é uma implementação de algoritmos de busca em largura e busca em profundidade para encontrar solucionar labirintos. Foi desenvolvido em Python e possui uma implementação gráfica para facilitar a visualização das soluções encontradas.

### Pré-requisitos:
Antes de executar o projeto, você precisará ter instalado em sua máquina:

- Python 3.x
- Pygame

## Arquivos
O projeto é composto pelos seguintes arquivos python:

### Solvers
Este arquivo contém a implementação das buscas em largura e profundidade. Ele define duas funções:

- BFS: algoritmo para realizar busca em largura
- DFS: algoritmo para realizar busca em profundidade

Cada função recebe um labirinto (representado como uma matriz) e retorna a solução do labirinto e todos as coordendas vizitadas em ordem.

#### Matrix_generator
Este arquivo contém as matrizes de labirinto que são utilizadas para testar as implementações das buscas. Existem três matrizes diferentes:

- small_matrix: uma matriz pequena para testes rápidos
- medium_matrix: uma matriz média para testes mais elaborados
- large_matrix: uma matriz grande para testes mais intensos

Cada matriz é representada como uma lista de listas.

### Graphics
Este arquivo contém a implementação gráfica do projeto. Ele define funções que são responsaveis por desenhar o labirinto, a busca e a solução encontrada.

#### Utils
Este arquivo contém as funções base utilizadas por ambas as buscas, incluindo as funções   sucessor e de teste de objetivo, especificadas para o projeto.

## Como executar
Para executar o projeto, basta executar o arquivo main:
```py
python3 main.py
```
No Terminal, selecione numericamente o tamanho do labirinto a ser solucionado. Depois, selecione qual algorítimo de busca deve ser executado.

## Autores
- Lucas Tosetto Teixeira (19104273)
- Vinícius de Carvalho Monteiro Longo (21250044)
