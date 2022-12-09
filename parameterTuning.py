import pandas as pd
import numpy as np
from xgboost import XGBRegressor

from dataAnalysis import *


def tuneXGBoost(scaler, X_test, Y_test, X_train, Y_train):


    # print("######MAX_DEPTH PARAMETER TUNING######")
    # max_depths = []
    # for depth in max_depths:
    #     print(f"####EVALUATION FOR MAX_DEPTH: {depth}####")
    #     model = XGBRegressor(max_depth = depth)

    #     model.fit(scaler.transform(X_train), Y_train)
    #     model_evaluate(model, scaler, X_test, Y_test)
    #     model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
    #     model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

    # etas = [0.1, 0.3, 0.5, 1]
    # for eta in etas:
    #     print(f"####EVALUATION FOR eta: {eta}####")
    #     model = XGBRegressor(eta = eta)

    #     model.fit(scaler.transform(X_train), Y_train)
    #     model_evaluate(model, scaler, X_test, Y_test)
    #     model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
    #     model_evaluate(model, scaler, X_test, Y_test, pop_max=30)

    # sampling = ["uniform", "gradient_based"]
    # for method in sampling:
    #     print(f"####EVALUATION FOR method: {method}####")
    #     model = XGBRegressor(sampling_method = method)

    #     model.fit(scaler.transform(X_train), Y_train)
    #     model_evaluate(model, scaler, X_test, Y_test)
    #     model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
    #     model_evaluate(model, scaler, X_test, Y_test, pop_max=30)
    
    gammas = [0.1, 0.3, 0.5, 1]
    for gamma in gammas:
        print(f"####EVALUATION FOR gamma: {gamma}####")
        model = XGBRegressor(gamma = gamma)

        model.fit(scaler.transform(X_train), Y_train)
        model_evaluate(model, scaler, X_test, Y_test)
        model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
        model_evaluate(model, scaler, X_test, Y_test, pop_max=30)