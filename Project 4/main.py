# Omer Khan
# CS461 Project 4
# Brian Hare

import pandas as pd
import tensorflow as tf
from tensorflow import keras
from configure import configure

trainingData = 'ramen-ratings-training.csv'
testData = 'ramen-ratings-test.csv'
validationData = 'ramen-ratings-validation.csv'
oldFile = 'ramen-ratings.csv'

configure(oldFile, trainingData, testData, validationData)

df_training = pd.read_csv(trainingData)
df_test = pd.read_csv(testData)
df_validation = pd.read_csv(validationData)

df_training['Brand'] = pd.Categorical(df_training['Brand'])
df_training['Brand'] = df_training.Brand.cat.codes
df_training['Style'] = pd.Categorical(df_training['Style'])
df_training['Style'] = df_training.Style.cat.codes
df_training['Country'] = pd.Categorical(df_training['Country'])
df_training['Country'] = df_training.Country.cat.codes

df_test['Brand'] = pd.Categorical(df_test['Brand'])
df_test['Brand'] = df_test.Brand.cat.codes
df_test['Style'] = pd.Categorical(df_test['Style'])
df_test['Style'] = df_test.Style.cat.codes
df_test['Country'] = pd.Categorical(df_test['Country'])
df_test['Country'] = df_test.Country.cat.codes

df_validation['Brand'] = pd.Categorical(df_validation['Brand'])
df_validation['Brand'] = df_validation.Brand.cat.codes
df_validation['Style'] = pd.Categorical(df_validation['Style'])
df_validation['Style'] = df_validation.Style.cat.codes
df_validation['Country'] = pd.Categorical(df_validation['Country'])
df_validation['Country'] = df_validation.Country.cat.codes

training_final = df_training.pop('Stars')
training_final = keras.utils.to_categorical(training_final)

test_final = df_test.pop('Stars')
test_final = keras.utils.to_categorical(test_final)

validation_final = df_validation.pop('Stars')
validation_final = keras.utils.to_categorical(validation_final)

dataset_training = tf.data.Dataset.from_tensor_slices((df_training.values, training_final))
dataset_test = tf.data.Dataset.from_tensors((df_test.values, test_final))
dataset_validation = tf.data.Dataset.from_tensor_slices((df_validation.values, validation_final))

dataset_training = dataset_training.shuffle(len(df_training)).batch(1)
#dataset_test = dataset_test.shuffle(len(df_test)).batch(1)
dataset_validation = dataset_validation.shuffle(len(df_validation)).batch(1)


def model():
    layers = tf.keras.Sequential([
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(100, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(1, activation='sigmoid'),
    ])
    layers.compile(optimizer='adam',
                   loss=tf.keras.losses.MeanSquaredError(),
                   metrics=['accuracy'])
    return layers

tf_model = model()
tf_model.fit(dataset_training, batch_size=None, epochs=10, validation_data=dataset_validation)

loss, accuracy = tf_model.evaluate(dataset_test)
print('\n\nTest Dataset Loss: {}, \nTest Dataset Accuracy: {}'.format(loss, accuracy))
