import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from process_data import cargar_datos

df = cargar_datos()

print(f"---El dataframe tiene {df.shape[0]} filas y {df.shape[1]} columnas---\n")
df.info()

# Eliminar columnas referidas a coordenadas
columnas_coordenadas = ["coordenada_x_utm", "coordenada_y_utm"]
df.drop(columns=columnas_coordenadas, inplace=True)

# Reestructuración de la columna tipo de vehículo
diccionario_mapeo = {
    'Motocicleta > 125cc': 'Motocicleta', 'Motocicleta hasta 125cc': 'Motocicleta',
    'Ciclomotor': 'Motocicleta', 'Moto de tres ruedas > 125cc': 'Motocicleta',
    'Ciclomotor de dos ruedas L1e-B': 'Motocicleta', 'Moto de tres ruedas hasta 125cc': 'Motocicleta',
    'Ciclo de motor L1e-A': 'Motocicleta', 'Bicicleta': 'Bicicleta', 'Bicicleta EPAC (pedaleo asistido)': 'Bicicleta',
    'Ciclo': 'Bicicleta', 'Patinete': 'Bicicleta', 'Patinete no eléctrico': 'Bicicleta',
    'Camión rígido': 'Camión', 'Tractocamión': 'Camión', 'Vehículo articulado': 'Camión',
    'Maquinaria de obras': 'Camión', 'Maquinaria agrícola': 'Camión', 'Remolque': 'Camión',
    'Semiremolque': 'Camión', 'Autobús': 'Autobús', 'Autobús articulado': 'Autobús',
    'Autobús EMT': 'Autobús', 'Autobús articulado EMT': 'Autobús', 'Microbús <= 17 plazas': 'Autobús',
    'Tranvía': 'Autobús', 'Tren/metro': 'Autobús', 'Turismo': 'Turismo', 'Furgoneta': 'Furgoneta',
    'Todo terreno': 'Turismo', 'Autocaravana': 'Turismo', 'Caravana': 'Turismo',
    'Cuadriciclo ligero': 'Otro vehículo', 'Cuadriciclo no ligero': 'Otro vehículo',
    'VMU eléctrico': 'Otro vehículo', 'Otros vehículos con motor': 'Otro vehículo',
    'Otros vehículos sin motor': 'Otro vehículo', 'Ambulancia SAMUR': 'Otro vehículo',
    'Camión de bomberos': 'Otro vehículo', 'Sin especificar': 'Otro vehículo', 'nan': 'Otro vehículo'
}
df.insert(df.columns.get_loc("tipo_vehiculo") + 1, "tipo_vehiculo_reducido", df["tipo_vehiculo"].map(diccionario_mapeo))

# Tratamiento de valores nulos
df["positiva_droga"].fillna(0, inplace=True)
df["positiva_alcohol"].fillna("N", inplace=True)
df["lesividad"].fillna("Sin atención sanitaria", inplace=True)
df["cod_lesividad"].fillna(0, inplace=True)
df["estado_meteorológico"].fillna("Se desconoce", inplace=True)
df.dropna(inplace=True)

print(f"Ahora el DataFrame tiene {df.shape[0]} filas y {df.shape[1]} columnas")
df.info()

# Análisis de positivos en alcohol y drogas
ambos_positivos = df[(df["positiva_alcohol"] == "S") & (df["positiva_droga"] == 1)]
print(f"Hay un total de {ambos_positivos.shape[0]} personas implicadas y {len(ambos_positivos['num_expediente'].unique())} expedientes únicos")

# Análisis de horas más peligrosas
df["hora_reducida"] = pd.to_datetime(df["hora"], format="%H:%M:%S").dt.hour
accidentes_por_hora = df['hora_reducida'].value_counts().reset_index()
accidentes_por_hora.columns = ['hora', 'n_accidentes']
accidentes_por_hora.sort_values('hora', inplace=True)

fig = px.bar(accidentes_por_hora, x='hora', y='n_accidentes', color='n_accidentes',
             color_continuous_scale='RdYlGn_r', title='Horas más peligrosas para circular en Madrid')
fig.update_layout(xaxis_title='Hora del Día', yaxis_title='Número de Accidentes', font=dict(size=14), plot_bgcolor='white')
fig.show()

# Mapa de calor de accidentes por día de la semana y hora
df['día_semana'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y').dt.day_name()
mapeo_dias = {'Monday': 'lunes', 'Tuesday': 'martes', 'Wednesday': 'miércoles',
              'Thursday': 'jueves', 'Friday': 'viernes', 'Saturday': 'sábado', 'Sunday': 'domingo'}
df['día_semana'] = df['día_semana'].map(mapeo_dias)
accidentes_heatmap = df.groupby(['día_semana', 'hora_reducida']).size().unstack(fill_value=0)

plt.figure(figsize=(16, 8))
sns.heatmap(accidentes_heatmap, cmap="RdYlGn_r", annot=False, linewidths=0.5, linecolor='black')
plt.title('Accidentes por Hora del Día y Día de la Semana', fontsize=18, weight='bold', pad=20)
plt.xlabel('Hora del Día', fontsize=14)
plt.ylabel('Día de la Semana', fontsize=14, labelpad=20)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

# Calendario de accidentes
df['fecha_hora'] = pd.to_datetime(df['fecha'] + ' ' + df['hora'], format='%d/%m/%Y %H:%M:%S')
accidentes_por_dia = df['fecha_hora'].dt.floor('d').value_counts().sort_index()
calplot.calplot(accidentes_por_dia, cmap='RdYlGn_r', edgecolor='black', daylabels=['L', 'M', 'X', 'J', 'V', 'S', 'D'],
                 suptitle='Accidentes por Día durante 6 años en Madrid', suptitle_kws={'fontsize': 18, 'weight': 'bold'},
                 monthlabels=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
plt.show()
