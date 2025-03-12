import os
import pandas as pd

def cargar_datos():
    """Carga los archivos CSV de la carpeta data/ y los combina en un DataFrame."""
    data_path = "data/"
    files = ["2019_Accidentalidad.csv", "2020_Accidentalidad.csv", "2021_Accidentalidad.csv",
             "2022_Accidentalidad.csv", "2023_Accidentalidad.csv", "2024_Accidentalidad.csv"]

    dfs = []
    for file in files:
        file_path = os.path.join(data_path, file)
        if os.path.exists(file_path):  # Verificar si el archivo existe antes de intentar leerlo
            dfs.append(pd.read_csv(file_path, delimiter=";"))
        else:
            print(f"Advertencia: {file} no encontrado. Se omitirá.")

    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        return df
    else:
        raise FileNotFoundError("No se encontraron archivos CSV en la carpeta data/")

if __name__ == "__main__":
    df = cargar_datos()
    print(df.head())
