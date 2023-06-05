import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from utils import *

EPOCHS = 40

# Leitura dados Excel
df = pd.read_excel('data.xlsx')
X, y = df.values[:, 1], df.values[:, 2]

x_interp, y_interp = add_pontos_interpolados(X, y, 1000)

# Divisão treinamento e teste
x_train, x_test, y_train, y_test = train_test_split(x_interp, y_interp, test_size=0.2, random_state=42)


models = {}
iterated_amount_layers = [2, 3, 5]
iterated_amount_neurons = [32, 64, 128]
iterated_activation_function = ['relu', 'sigmoid']

for num_layers in iterated_amount_layers:
    for num_neurons in iterated_amount_neurons:
        for activation_function in iterated_activation_function:
            description = f"{num_layers} hidden layers, {num_neurons} neurons each, activation function: {activation_function}"
            models[description] = build_model(num_layers, num_neurons, activation_function)


for specification in models.keys():
    model = models[specification]
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    history = model.fit(x_train, y_train, epochs=EPOCHS, verbose=1)
    loss = model.evaluate(x_test, y_test, verbose=0)
    print(f"Test loss, model {specification}:", loss)
    y_pred_train = model.predict(x_interp)
    y_pred_test = model.predict(x_test)

    # Plot the results
    plot_predicted_values_graph(x_interp, y_interp, y_pred_train, x_test, y_pred_test, specification)
    plot_loss_graph(history.history['loss'][2:], specification)
