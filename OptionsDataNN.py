# -*- coding: utf-8 -*-
"""OptionsDataAnalysisPy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cu17gQmPBiw75l21bZAFz1k8p7ROODJ8
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout
from keras import backend as K
from sklearn import preprocessing
import matplotlib.pyplot as plt

df = pd.read_csv('/content/optionData.csv', header = None)
df.columns = df.iloc[0]
df = df[1:]

df = df.dropna()
df = df.sample(frac = 1)

df = df.drop(['CallPut', 'Side', 'Expiration', 'SeInstructionId', 'OrderId', 'TimeSe', 'OptionId', 'Exchange', 'TimeOmOut', 'OrderEventType', 'TimeOmIn', 'OptionIdOmIn'], axis=1)

df1 = pd.get_dummies(df["OrderEventTypeOmIn"])

df = pd.concat((df, df1), axis = 1)
df = df.drop(['CANCEL', 'OrderEventTypeOmIn'], axis = 1)

le = preprocessing.LabelEncoder()
le.fit(df['UnderlyingSymbol'])
df['UnderlyingSymbol'] = le.transform(df['UnderlyingSymbol'])

df = df.to_numpy()
df = np.delete(df, 0, axis = 0)

training = df[0:23000].astype('float32')
testing = df[23000:].astype('float32')
X1 = training[:,0:5]
Y1 = training[:,5]
X2 = testing[:,0:5]
Y2 = testing[:,5]

print(X1)
print(Y1)

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(5,)),
    keras.layers.Dense(64, activation=tf.nn.relu),
    keras.layers.Dense(248, activation=tf.nn.relu),
	  keras.layers.Dense(512, activation=tf.nn.relu),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(64, activation=tf.nn.relu),
    keras.layers.Dense(1, activation=tf.nn.sigmoid),
])

model.compile(optimizer='sgd',
              loss='binary_crossentropy',
              metrics=['accuracy'])

K.set_value(model.optimizer.learning_rate, 0.001)
print("Learning rate before first fit:s", model.optimizer.learning_rate.numpy())

history = model.fit(X1, Y1, epochs=50, batch_size = 200, validation_data = (X2, Y2))

plt.plot(history.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train'], loc='upper left')
plt.show()

model.summary()