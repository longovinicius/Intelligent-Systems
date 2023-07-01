import tensorflow as tf
import pandas as pd

loaded_model = tf.keras.models.load_model('weights')

user_input = input("Digite um ou mais(em formato val1, val2) valores de x")

splitted_answer = user_input.split(", ")
data = [int(num) for num in splitted_answer]

predictions = loaded_model.predict(data)

df = pd.read_excel('data.xlsx')
X, y = df.values[:, 1], df.values[:, 2]

for i, x in enumerate(data):
    prediction = "{:.2f}".format(predictions[i][0])
    print(f"Input: {x}, y Real: {y[x]} ---> Predicao: {prediction}")


