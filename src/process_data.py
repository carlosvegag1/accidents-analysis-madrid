import os
import pandas as pd

def cargar_datos():
    """Carga los archivos CSV de la carpeta data/ y los combina en un DataFrame."""
    data_path = "data/"
    files = ["2019_Accidentalidad.csv", "2020_Accidentalidad.csv", "2021_Accidentalidad.csv",
             "2022_Accidentalidad.csv", "2023_Accidentalidad.csv", "2024_Accidentalidad.csv"]

    dfs = [pd.read_csv(os.path.join(data_path, file), delimiter=";") for file in files]
    df = pd.concat(dfs, ignore_index=True)
    
    return df

if __name__ == "__main__":
    df = cargar_datos()
    print(df.head())  # Ver las primeras filas
