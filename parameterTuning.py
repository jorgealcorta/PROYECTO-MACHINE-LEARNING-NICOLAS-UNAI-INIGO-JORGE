import pandas as pd
import numpy as np
from xgboost import XGBRegressor

from dataAnalysis import *


def tuneXGBoost(scaler, X_test, Y_test, X_train, Y_train):
    print("######MAX_DEPTH PARAMETER TUNING######")
    max_depths = [12,15,18]
    for depth in max_depths:
        print(f"####EVALUATION FOR MAX_DEPTH: {depth}####")
        model = XGBRegressor(max_depth = depth)

        model.fit(scaler.transform(X_train), Y_train)
        model_evaluate(model, scaler, X_test, Y_test)
        model_evaluate(model, scaler, X_test, Y_test, pop_min=70)
        model_evaluate(model, scaler, X_test, Y_test, pop_max=30)