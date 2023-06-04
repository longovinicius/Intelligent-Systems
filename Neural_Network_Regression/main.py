import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from utils import *

EPOCHS = 40

# Ler os dados do arquivo Excel
df = pd.read_excel('data.xlsx')
X, y = df.values[:, 1], df.values[:, 2]

x_interp, y_interp = add_pontos_interpolados(X, y, 1000)

# Split the data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(x_interp, y_interp, test_size=0.2, random_state=42)

models = {}
# Build the model
models["5 hidden layers, 128 neurons each, RELU"] = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(1,)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(1)
])

models["5 hidden layers, 64 neurons each, RELU"] = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(1,)),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1)
])


models["3 hidden layers, 128 neurons each, RELU"] = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(1,)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(1)
])

models["5 hidden layers, 128 neurons each, SIGMOID"] = keras.Sequential([
    keras.layers.Dense(128, activation='sigmoid', input_shape=(1,)),
    keras.layers.Dense(128, activation='sigmoid'),
    keras.layers.Dense(128, activation='sigmoid'),
    keras.layers.Dense(128, activation='sigmoid'),
    keras.layers.Dense(128, activation='sigmoid'),
    keras.layers.Dense(1)
])

models["5 hidden layers, 64 neurons each, SIGMOID"] = keras.Sequential([
    keras.layers.Dense(64, activation='sigmoid', input_shape=(1,)),
    keras.layers.Dense(64, activation='sigmoid'),
    keras.layers.Dense(64, activation='sigmoid'),
    keras.layers.Dense(64, activation='sigmoid'),
    keras.layers.Dense(64, activation='sigmoid'),
    keras.layers.Dense(1)
])

models["3 hidden layers, 64 neurons each, SIGMOID"] = keras.Sequential([
    keras.layers.Dense(64, activation='sigmoid', input_shape=(1,)),
    keras.layers.Dense(64, activation='sigmoid'),
    keras.layers.Dense(64, activation='sigmoid'),
    keras.layers.Dense(1)
])

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
