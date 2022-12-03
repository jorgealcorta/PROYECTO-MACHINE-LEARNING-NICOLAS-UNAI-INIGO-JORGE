import pandas as pd
import numpy as np
import os
path = "C:/Users/usuario/OneDrive/Documentos/GitHub/PROYECTO-MACHINE-LEARNING-NICOLAS-UNAI-INIGO-JORGE/datasets_kaggle/"

def unir_datasets():
    # Carga de los datasets
    
    df1 = pd.read_csv(os.path.join(path, "dataset1.csv"), sep = ";")
    df2 = pd.read_csv(os.path.join(path, "dataset2.csv"), sep = ";")
    df3 = pd.read_csv(os.path.join(path, "dataset3.csv"), sep = ";")
    df4 = pd.read_csv(os.path.join(path, "dataset4.csv"), sep = ";")
    df5 = pd.read_csv(os.path.join(path, "dataset5.csv"), sep = ";")
    print("Carga de los datasets completada")
    #print(df1)
    #print(df2)
    #print(df3)
    #print(df4)
    #print(df5)

    # Unión de los datasets
    df = pd.concat([df1, df2, df3, df4, df5], axis = 0)
    print("Unión de los datasets completada")
    return df
    



unir_datasets().to_csv(os.path.join(path, "dataset_unido.csv"), sep = ";", index = False)