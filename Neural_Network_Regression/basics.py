import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# TODO: Plot do grafico de loss e validação
# TODO: Adaptação de 3 Arquiteturas (c/ Sigmoid, linear com normalização)
EPOCHS = 800

df = pd.read_excel('data.xlsx')
data = df.values

x_train, x_test, y_train, y_test = train_test_split(data[:, 1], data[:, 2], test_size=0.2, random_state=42)

model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(1,)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(1)
])




model.compile(optimizer='adam', loss='mse')
model.fit(x_train, y_train, epochs=EPOCHS, batch_size=2, verbose=1) # batch_size=10 

loss = model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", loss)

y_pred = model.predict(x_test)
y_pred_train = model.predict(x_train)

plt.figure(figsize=(8, 6))
plt.scatter(data[:, 1], data[:, 2], label='True values')
plt.scatter(x_test, y_pred, color='red', label='Predicted values')
plt.scatter(x_train, y_pred_train, color='blue', label='Predicted values Train')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Third-Degree Function Regression')
plt.legend()
plt.grid(True)
plt.show()
