# LIMPIEZA DE DATOS DE FACEBOOK
# (continúa con la exploración y exportación de "1_Exploración_inicial.ipynb")


import pandas as pd
import numpy as np
import re
from collections import Counter

pd.set_option("display.max_columns", None)


# 17. CARGAR ARCHIVO

ruta_archivo = "Datos Crudos Facebook 10 de Marzo.csv"

try:
    df = pd.read_csv(ruta_archivo, encoding="utf-8-sig")
except UnicodeDecodeError:
    df = pd.read_csv(ruta_archivo, encoding="latin-1")

print(f"Archivo cargado: {df.shape[0]} filas, {df.shape[1]} columnas")


# 18. DEFINIR LAS COLUMNAS NÚCLEO Y SU NUEVO NOMBRE

mapa_columnas = {
    "Identificador de la publicación": "id_publicacion",
    "Identificador de la página": "id_pagina",
    "Nombre de la página": "nombre_pagina",
    "Título": "titulo",
    "Descripción": "descripcion",
    "Duración (segundos)": "duracion_segundos",
    "Hora de publicación": "fecha_hora_publicacion",
    "Tipo de subtítulo": "tipo_subtitulo",
    "Enlace permanente": "enlace",
    "Es una publicación cruzada": "es_publicacion_cruzada",
    "Es una publicación compartida": "es_publicacion_compartida",
    "Tipo de publicación": "tipo_publicacion",
    "Idiomas": "idiomas",
    "Etiquetas personalizadas": "etiquetas",
    "Estado de contenido financiado": "estado_contenido_financiado",
    "Comentario sobre los datos": "comentario_datos",
    "Fecha": "fecha_reporte",
    "Visualizaciones": "visualizaciones",
    "Alcance": "alcance",
    "Reacciones, comentarios y veces que se compartió": "interacciones_totales",
    "Reacciones": "reacciones",
    "Comentarios": "comentarios",
    "Veces que se compartió": "veces_compartido",
    "Total de clics": "total_clics",
    "Clics de otro tipo": "clics_otro_tipo",
    "Clics en el enlace": "clics_enlace",
    "Consumo de segmentación del público coincidente (Photo Click)": "consumo_photo_click",
    "Ingresos aproximados por monetización de contenido": "ingresos_aproximados",
    "Ingresos por estrellas estimados (USD)": "ingresos_estrellas_usd",
    "Ingresos estimados (USD)": "ingresos_estimados_usd",
    "Visualizaciones de Publicaciones orgánicas": "visualizaciones_organicas",
    "Visualizaciones de Publicaciones promocionadas": "visualizaciones_promocionadas",
    "Alcance de Publicaciones orgánicas": "alcance_organico",
    "Alcance de Publicaciones promocionadas": "alcance_promocionado",
    "Reproducciones de video de 3 segundos": "reproducciones_3s",
    "Reproducciones de video de 1 minuto": "reproducciones_1min",
    "Espectadores de 3 segundos": "espectadores_3s",
    "Espectadores de 1 minuto": "espectadores_1min",
    "Reproducciones de video de 3 segundos de Publicaciones promocionadas": "reproducciones_3s_promocionadas",
    "Reproducciones de video de 3 segundos de Publicaciones orgánicas": "reproducciones_3s_organicas",
    "Reproducciones de video de 1 minuto de Recomendaciones": "reproducciones_1min_recomendaciones",
    "Reproducciones de video de 1 minuto de Contenido compartido": "reproducciones_1min_compartido",
    "Reproducciones de video de 1 minuto de Seguidores": "reproducciones_1min_seguidores",
    "Reproducciones de video de 1 minuto de Publicaciones promocionadas": "reproducciones_1min_promocionadas",
    "Reproducciones de video de 1 minuto de espectadores recurrentes": "reproducciones_1min_recurrentes",
    "Segundos reproducidos en Recomendaciones": "segundos_recomendaciones",
    "Segundos reproducidos en Contenido compartido": "segundos_compartido",
    "Segundos reproducidos en Seguidores": "segundos_seguidores",
    "Segundos reproducidos en Publicaciones promocionadas": "segundos_promocionadas",
    "Segundos reproducidos por espectadores recurrentes": "segundos_recurrentes",
    "Segundos en promedio producidos en Recomendaciones": "segundos_promedio_recomendaciones",
    "Segundos en promedio producidos en Contenido compartido": "segundos_promedio_compartido",
    "Segundos en promedio producidos en Seguidores": "segundos_promedio_seguidores",
    "Segundos en promedio producidos en Publicaciones promocionadas": "segundos_promedio_promocionadas",
    "Segundos en promedio reproducidos por espectadores recurrentes": "segundos_promedio_recurrentes",
    "Segundos reproducidos": "segundos_reproducidos_total",
    "Segundos en promedio reproducidos": "segundos_promedio_total",
    "Espectadores recurrentes": "espectadores_recurrentes",
    "Comentarios negativos de los usuarios": "comentarios_negativos",
    "Comentarios negativos únicos de los usuarios": "comentarios_negativos_unicos",
    "Comentarios negativos de los usuarios: Ocultar todo": "comentarios_negativos_ocultar_todo",
    "Comentarios negativos únicos de los usuarios: Ocultar todo": "comentarios_negativos_unicos_ocultar_todo",
    "Comentarios negativos de los usuarios: Ocultar": "comentarios_negativos_ocultar",
    "Comentarios negativos únicos de los usuarios: Ocultar": "comentarios_negativos_unicos_ocultar",
}

columnas_faltantes = [c for c in mapa_columnas if c not in df.columns]
if columnas_faltantes:
    print("AVISO: estas columnas no se encontraron en tu CSV (revisa nombres):")
    for c in columnas_faltantes:
        print("  -", c)

df_core = df[[c for c in mapa_columnas if c in df.columns]].rename(columns=mapa_columnas)



# 19. PARSEAR FECHA Y HORA DE PUBLICACIÓN

df_core["fecha_hora_publicacion"] = pd.to_datetime(
    df_core["fecha_hora_publicacion"], errors="coerce"
)

df_core["hora_publicacion"] = df_core["fecha_hora_publicacion"].dt.hour
df_core["dia_semana"] = df_core["fecha_hora_publicacion"].dt.day_name()
df_core["mes"] = df_core["fecha_hora_publicacion"].dt.month

sin_fecha = df_core["fecha_hora_publicacion"].isna().sum()
print(f"Filas sin fecha parseada correctamente: {sin_fecha}")
# Si este número es alto, el formato de fecha en tu CSV es distinto al
# esperado (revisa un valor original con: df['Hora de publicación'].head())



# 20. CONVERTIR COLUMNAS NUMÉRICAS

columnas_numericas = [
    "duracion_segundos", "visualizaciones", "alcance", "interacciones_totales",
    "reacciones", "comentarios", "veces_compartido", "total_clics",
    "clics_otro_tipo", "clics_enlace", "consumo_photo_click",
    "ingresos_aproximados", "ingresos_estrellas_usd", "ingresos_estimados_usd",
    "visualizaciones_organicas", "visualizaciones_promocionadas",
    "alcance_organico", "alcance_promocionado", "reproducciones_3s",
    "reproducciones_1min", "espectadores_3s", "espectadores_1min",
    "reproducciones_3s_promocionadas", "reproducciones_3s_organicas",
    "reproducciones_1min_recomendaciones", "reproducciones_1min_compartido",
    "reproducciones_1min_seguidores", "reproducciones_1min_promocionadas",
    "reproducciones_1min_recurrentes", "segundos_recomendaciones",
    "segundos_compartido", "segundos_seguidores", "segundos_promocionadas",
    "segundos_recurrentes", "segundos_promedio_recomendaciones",
    "segundos_promedio_compartido", "segundos_promedio_seguidores",
    "segundos_promedio_promocionadas", "segundos_promedio_recurrentes",
    "segundos_reproducidos_total", "segundos_promedio_total",
    "espectadores_recurrentes", "comentarios_negativos",
    "comentarios_negativos_unicos", "comentarios_negativos_ocultar_todo",
    "comentarios_negativos_unicos_ocultar_todo", "comentarios_negativos_ocultar",
    "comentarios_negativos_unicos_ocultar",
]

for col in columnas_numericas:
    if col in df_core.columns:
        df_core[col] = pd.to_numeric(df_core[col], errors="coerce")


# 21. QUITAR DUPLICADOS

antes = len(df_core)
df_core = df_core.drop_duplicates(subset=["id_publicacion"])
print(f"Filas eliminadas por duplicado de id_publicacion: {antes - len(df_core)}")


# 22. TABLA DE RETENCIÓN DE VIDEO (FORMATO LARGO)

# 82 columnas anchas -> 1 tabla larga: id_publicacion, tipo_retencion,
# intervalo, porcentaje. Así se relaciona en SQL con un JOIN normal.

cols_retencion_general = [c for c in df.columns if c.startswith(
    "Porcentaje del total de reproducciones en el intervalo")]
cols_retencion_15s = [c for c in df.columns if c.startswith(
    "Porcentaje de reproducciones de 15 segundos en el intervalo")]

def construir_retencion_larga(df_original, columnas, tipo_retencion):
    sub = df_original[["Identificador de la publicación"] + columnas].copy()
    sub = sub.rename(columns={"Identificador de la publicación": "id_publicacion"})
    largo = sub.melt(
        id_vars="id_publicacion",
        var_name="columna_original",
        value_name="porcentaje",
    )
    largo["intervalo"] = largo["columna_original"].str.extract(r"(\d+)$").astype(int)
    largo["tipo_retencion"] = tipo_retencion
    largo["porcentaje"] = pd.to_numeric(largo["porcentaje"], errors="coerce")
    return largo[["id_publicacion", "tipo_retencion", "intervalo", "porcentaje"]]

retencion_general = construir_retencion_larga(df, cols_retencion_general, "general")
retencion_15s = construir_retencion_larga(df, cols_retencion_15s, "15_segundos")
retencion_video = pd.concat([retencion_general, retencion_15s], ignore_index=True)
retencion_video = retencion_video.dropna(subset=["porcentaje"])

print(f"Tabla de retención construida: {len(retencion_video)} filas")



# 23. PALABRAS MÁS FRECUENTES EN LAS DESCRIPCIONES

STOPWORDS_ES = set("""
de la que el en y a los del se las por un para con no una su al lo como
mas pero sus le ya o este si porque esta entre cuando muy sin sobre tambien
me hasta hay donde quien desde todo nos durante todos uno les ni contra
otros ese eso ante ellos e esto mi antes algunos que qué su tu tus es son
fue ser está están era eran ha han he has será seremos siendo sido soy eres
nuestro nuestra nuestros nuestras esa esas esos aquel aquella aquellos
aquellas mio mia mios mias tuyo tuya tuyos tuyas suyo suya suyos suyas
""".split())

def contar_palabras(serie_texto, top_n=40):
    contador = Counter()
    for texto in serie_texto.dropna():
        palabras = re.findall(r"[a-záéíóúüñ]+", str(texto).lower())
        palabras = [p for p in palabras if p not in STOPWORDS_ES and len(p) > 2]
        contador.update(palabras)
    return pd.DataFrame(contador.most_common(top_n), columns=["palabra", "frecuencia"])

top_palabras = contar_palabras(df_core["descripcion"])
print("\nTop 15 palabras en descripciones:")
print(top_palabras.head(15).to_string(index=False))



# 24. GUARDAR ARCHIVOS LIMPIOS

df_core.to_csv("posts_clean.csv", index=False, encoding="utf-8-sig")
retencion_video.to_csv("retencion_video.csv", index=False, encoding="utf-8-sig")
top_palabras.to_csv("top_palabras.csv", index=False, encoding="utf-8-sig")

print("\nListo. Archivos generados:")
print(" - posts_clean.csv      ", df_core.shape)
print(" - retencion_video.csv  ", retencion_video.shape)
print(" - top_palabras.csv     ", top_palabras.shape)


# NOTA: columnas excluidas de esta limpieza (disponibles si luego
# se quieren agregar con la misma lógica de mapa_columnas + melt):
#   - 159 columnas de "Reproducciones de video de 3 segundos por país (X)"
#   - 12 columnas de "... por público destacado (género, rango de edad)"
