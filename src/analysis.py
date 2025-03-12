import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from process_data import cargar_datos

df = cargar_datos()

# Visualización: Número de accidentes por hora
df["hora_reducida"] = pd.to_datetime(df["hora"], format="%H:%M:%S").dt.hour
accidentes_por_hora = df['hora_reducida'].value_counts().sort_index()

plt.figure(figsize=(10, 5))
sns.barplot(x=accidentes_por_hora.index, y=accidentes_por_hora.values, palette="Reds")
plt.xlabel("Hora del Día")
plt.ylabel("Número de Accidentes")
plt.title("Accidentes por Hora del Día")
plt.show()
