Date:
-----
07-05-2023 18:28

LISTA DE ARCHIVOS 
-----------------

Los archivos deben ser consultados en el en el que se generaron:

1. Scrapping >> cochesnet_scrapper_v08.ipynb: scrapping del sitio web para obtener los datos de un modelo de vehículo

2. Data integration >> cochesnet_v13.ipynb: recopilar los datos de todos los vehículos en un único archivo CSV. Se realizan algunas operaciones de limpieza.

3. Data cleaning >> cochesnet_Preprocess_v02.ipynb: cuaderno de prueba en el que se toma el CSV con todos los datos de los vehículos y se realiza el pre-proceso. No está acutalizado (OUTDATED)

4. Train MLP model >> cochesnet_ALL_IN_ONE_v11.ipynb: en este cuadernos se realizan las acciones de CARGA DE DATOS, LIMPIEZA, DEFINICIÓN DEL MODELO, ENTRENAMIENTO Y EVALUACIÓN (All-In-One). Contiene los datos actualizados del modelo final utilizado en el serividor Flask.

5. Flask App >> Flask.py: se define la App principal del servidor Flask.

6. Flask template >> predict.html: el servidor Flask consta de tres webs: index, input1, input2 y predict. Esta última muestra el resultado de las predicciones.


