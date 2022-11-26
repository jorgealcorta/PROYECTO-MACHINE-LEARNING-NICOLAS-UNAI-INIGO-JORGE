from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.activations import tanh, sigmoid, relu, softmax
from tensorflow.keras.metrics import categorical_crossentropy
from src.classificators.binary_metrics import *

def dense_model_1(input_dimension):
    model = Sequential()
    model.add(Dense(units=32, input_dim=input_dimension, activation=relu))
    model.add(Dense(units=64, activation=relu))
    model.add(Dense(units=128, activation=tanh))
    model.add(Dense(units=16, activation=relu))
    model.add(Dense(units=2, activation=softmax))
    model.compile(loss=categorical_crossentropy, optimizer='adam', metrics=[f1_tensor, recall_tensor, precision_tensor])
    return model