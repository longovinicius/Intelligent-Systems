import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from utils import *

EPOCHS = 4

# TODO: Leitura do usuario coordenada x, resposta em Y.
# TODO: Salvar Pesos em um arquivo, interacao com usuario em outro arquivo.
# TODO: Video: explicar funcionalidade basica de codigo
# TODO: Video: grafico de erro para DS de train e teste para identificar overfitting apos muito treinamento
# TODO: Numero de epocas foi suficiente? FOi demais?

# Ler os dados do arquivo Excel
df = pd.read_excel('data.xlsx')
X, y = df.values[:, 1], df.values[:, 2]

x_interp, y_interp = add_pontos_interpolados(X, y, 1000)

# Split the data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(x_interp, y_interp, test_size=0.2, random_state=42)

models = {}
# Build the model
models["4 hidden layers, 64 neurons each, RELU"] = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(1,)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1)
])

models["4 hidden layers, 16-128 neurons progressive, RELU"] = keras.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(1,)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(1)
])

models["4 hidden layers, 16-128 neurons progressive, SIGMOID"] = keras.Sequential([
    keras.layers.Dense(16, activation='sigmoid', input_shape=(1,)),
    keras.layers.Dense(32, activation='sigmoid'),
    keras.layers.Dense(64, activation='sigmoid'),
    keras.layers.Dense(128, activation='sigmoid'),
    keras.layers.Dense(1)
])

best_model = {'loss': 100000, 'model': None}
plot_params = []
for specification in models.keys():
    model = models[specification]
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
    history = model.fit(x_train, y_train, epochs=EPOCHS, verbose=1)
    loss = model.evaluate(x_test, y_test, verbose=0)[0]
    print(f"Test loss, model {specification}:", loss)
    y_pred_train = model.predict(x_interp)
    y_pred_test = model.predict(x_test)

    # Plot the results
    plot_params.append([x_interp, y_interp, y_pred_train, x_test, y_pred_test,
                        specification, history.history['loss'][2:], specification])
    # plot_predicted_values_graph(x_interp, y_interp, y_pred_train, x_test, y_pred_test, specification)
    # plot_loss_graph(history.history['loss'][2:], specification)

    if loss < best_model['loss']:
        print(f"New model saved: {loss}")
        best_model['loss'] = loss 
        best_model['model'] = model

for param in plot_params:
    plot_predicted_values_graph(param[0], param[1], param[2], param[3], param[4], param[5])
    plot_loss_graph(param[6], param[7])
best_model['model'].save('weights')

