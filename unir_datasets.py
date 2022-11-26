# funcion que une los datasets

import pandas as pd
import numpy as np
import os

def unir_datasets():
    # Carga de los datasets
    path = "C:/Users/usuario/OneDrive/Documentos/GitHub/PROYECTO-MACHINE-LEARNING-NICOLAS-UNAI-INIGO-JORGE/datasets_kaggle/"
    df1 = pd.read_csv(os.path.join(path, "dataset1.csv"))
    df2 = pd.read_csv(os.path.join(path, "dataset2.csv"))
    df3 = pd.read_csv(os.path.join(path, "dataset3.csv"))
    df4 = pd.read_csv(os.path.join(path, "dataset4.csv"))
    df5 = pd.read_csv(os.path.join(path, "dataset5.csv"))
    print("Carga de los datasets completada")
    print(df1)

    # Unión de los datasets 

unir_datasets()