# Analisis-de-Rendimiento-de-Publicaciones-en-Facebook-con-Python-y-SQL

Análisis de datos con Python y SQL para evaluar el rendimiento de publicaciones y maximizar la retención de videos en mi página de Facebook con más de 70,000 seguidores.

## Documentación Principal
El detalle completo de este proyecto se encuentra en el archivo adjunto "Análisis de Rendimiento Facebook.pdf". Se recomienda revisar este documento, ya que ahí se describe a fondo:
* El contexto y los objetivos del proyecto.
* Los pasos de limpieza y generación de tablas.
* Los hallazgos técnicos descubiertos durante la exploración (como el funcionamiento real de las curvas de retención en Meta).
* Las respuestas a las consultas de negocio mediante SQL y las conclusiones generales.

## Estructura del Repositorio
Este repositorio está organizado en dos carpetas principales que separan el proceso de extracción, transformación y carga, del análisis de datos.

### 1. Códigos
Contiene los scripts y cuadernos utilizados en las distintas fases del proyecto, utilizando Python para la limpieza y SQL para el análisis:
* 1_Exploración_inicial.ipynb: Cuaderno para la revisión inicial de la estructura general del archivo crudo.
* 2_Exploración_y_exportación.py: Script de Python para seleccionar las columnas núcleo y limpiar la información.
* 3_Verificacion_intervalos.py: Comprobación estadística de los intervalos de retención de video.
* 4_Creación_y_Verificación_Tablas: Código para diseñar el esquema y crear las tablas en la base de datos.
* 5_consultas_finales.sql: Las consultas en SQL utilizadas para responder las preguntas estratégicas sobre el rendimiento del contenido.

### 2. Muestras de Datos .csv
Para facilitar la revisión técnica del proyecto sin exponer la base de datos completa, se incluyen muestras representativas:
* Muestra de Datos Crudos.csv: Un fragmento del archivo original descargado de Facebook antes del proceso de limpieza.
* Muestra Datos Exportados de Python: Tablas limpias resultantes de la ejecución de los scripts de Python, listas para ser insertadas en la base de datos.
* Resultados Pregunta 1.csv: Un ejemplo de los datos tabulados obtenidos tras ejecutar una consulta SQL exitosa.
