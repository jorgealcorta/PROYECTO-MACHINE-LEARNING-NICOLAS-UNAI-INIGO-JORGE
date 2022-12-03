from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.activations import tanh, sigmoid, relu, softmax
from tensorflow.keras.metrics import categorical_crossentropy
from src.classificators.binary_metrics import *


def training_model(input_dimension):
    model = dense_model_1(X_train.shape[1])
    history = model.fit(
    scaler.transform(X_train), Y_train,
    epochs=10, 
    batch_size=50, 
    verbose=0, 
    validation_data=(scaler.transform(X_test), Y_test)
)


def dense_model_1(input_dimension):
    model = Sequential()
    model.add(Dense(units=32, input_dim=input_dimension, activation=relu))
    model.add(Dense(units=64, activation=relu))
    model.add(Dense(units=128, activation=tanh))
    model.add(Dense(units=16, activation=relu))
    model.add(Dense(1))
    model.compile(loss=categorical_crossentropy, optimizer='adam', metrics=[f1_tensor, recall_tensor, precision_tensor])
    return model


def recall_tensor(y_true, y_pred):
    y_true = tf.cast(tf.math.argmin(y_true, axis=1), tf.dtypes.float32)
    y_pred = tf.cast(tf.math.argmin(y_pred, axis=1), tf.dtypes.float32)
    true_positives = K.sum(y_true * y_pred)
    possible_positives = K.sum(y_true)
    recall = true_positives / (possible_positives + K.epsilon())
    return recall



def precision_tensor(y_true, y_pred):
    y_true = tf.cast(tf.math.argmin(y_true, axis=1), tf.dtypes.float32)
    y_pred = tf.cast(tf.math.argmin(y_pred, axis=1), tf.dtypes.float32)
    true_positives = K.sum(y_true * y_pred)
    predicted_positives = K.sum(y_pred)
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision




def f1_tensor(y_true, y_pred):
    precision = precision_tensor(y_true, y_pred)
    recall = recall_tensor(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))



def build_model(input_dimension):
  model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[input_dimension]),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model