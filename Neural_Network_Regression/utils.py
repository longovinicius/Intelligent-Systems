import matplotlib.pyplot as plt
import numpy as np


def add_pontos_interpolados(x_existing, y_existing, num_interp_points=1000):
    x_interp, y_interp = [], []
    for i in range(len(x_existing) - 1):
        x_start = x_existing[i]
        x_end = x_existing[i+1]
        y_start = y_existing[i]
        y_end = y_existing[i+1]
        
        # Realizar interpolação linear
        x_interp_values = np.linspace(x_start, x_end, num_interp_points+2)[:-1]  # Descartar o primeiro e último valor para evitar repetições
        y_interp_values = np.interp(x_interp_values, [x_start, x_end], [y_start, y_end])
        
        # Adicionar os pontos interpolados às listas
        x_interp.extend(list(x_interp_values))
        y_interp.extend(list(y_interp_values))
    
    return x_interp, y_interp

def plot_predicted_values_graph(x_interp, y_interp, y_pred_train, x_test, y_pred_test, specification):
    plt.figure(figsize=(8, 6))
    plt.scatter(x_interp, y_interp, label='True values')
    plt.scatter(x_interp, y_pred_train, color='red', label='Predicted values (train)')
    plt.scatter(x_test, y_pred_test, color='green', label='Predicted values (test)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Resultados: {specification}')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_loss_graph(loss_values, specification):
    plt.plot(loss_values)
    plt.title(f'Loss: {specification}')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.show()