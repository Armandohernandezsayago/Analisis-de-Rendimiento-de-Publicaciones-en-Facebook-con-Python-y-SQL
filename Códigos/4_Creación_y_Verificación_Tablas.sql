-- ESQUEMA PARA EL PROYECTO DE ANÁLISIS DE FACEBOOK

PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS retencion_video;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS top_palabras;

CREATE TABLE posts (
    id_publicacion               TEXT PRIMARY KEY,
    id_pagina                    TEXT,
    nombre_pagina                TEXT,
    titulo                       TEXT,
    descripcion                  TEXT,
    duracion_segundos            REAL,
    fecha_hora_publicacion       TIMESTAMP,
    tipo_subtitulo                TEXT,
    enlace                       TEXT,
    es_publicacion_cruzada       TEXT,
    es_publicacion_compartida    TEXT,
    tipo_publicacion             TEXT,
    idiomas                      TEXT,
    etiquetas                    TEXT,
    estado_contenido_financiado  TEXT,
    comentario_datos             TEXT,
    fecha_reporte                DATE,
    visualizaciones              REAL,
    alcance                      REAL,
    interacciones_totales        REAL,
    reacciones                   REAL,
    comentarios                  REAL,
    veces_compartido             REAL,
    total_clics                  REAL,
    clics_otro_tipo               REAL,
    clics_enlace                 REAL,
    consumo_photo_click          REAL,
    ingresos_aproximados         REAL,
    ingresos_estrellas_usd       REAL,
    ingresos_estimados_usd       REAL,
    visualizaciones_organicas    REAL,
    visualizaciones_promocionadas REAL,
    alcance_organico             REAL,
    alcance_promocionado         REAL,
    reproducciones_3s            REAL,
    reproducciones_1min          REAL,
    espectadores_3s              REAL,
    espectadores_1min            REAL,
    reproducciones_3s_promocionadas REAL,
    reproducciones_3s_organicas  REAL,
    reproducciones_1min_recomendaciones REAL,
    reproducciones_1min_compartido REAL,
    reproducciones_1min_seguidores REAL,
    reproducciones_1min_promocionadas REAL,
    reproducciones_1min_recurrentes REAL,
    segundos_recomendaciones     REAL,
    segundos_compartido          REAL,
    segundos_seguidores          REAL,
    segundos_promocionadas       REAL,
    segundos_recurrentes         REAL,
    segundos_promedio_recomendaciones REAL,
    segundos_promedio_compartido REAL,
    segundos_promedio_seguidores REAL,
    segundos_promedio_promocionadas REAL,
    segundos_promedio_recurrentes REAL,
    segundos_reproducidos_total  REAL,
    segundos_promedio_total      REAL,
    espectadores_recurrentes     REAL,
    comentarios_negativos        REAL,
    comentarios_negativos_unicos REAL,
    comentarios_negativos_ocultar_todo REAL,
    comentarios_negativos_unicos_ocultar_todo REAL,
    comentarios_negativos_ocultar REAL,
    comentarios_negativos_unicos_ocultar REAL,
    -- estas tres van AL FINAL porque así las agrega el script de Python
    hora_publicacion              INTEGER,  -- 0-23
    dia_semana                    TEXT,
    mes                           INTEGER
);

CREATE TABLE retencion_video (
    id_publicacion   TEXT REFERENCES posts(id_publicacion),
    tipo_retencion   TEXT,
    intervalo        INTEGER,
    porcentaje       REAL
);

CREATE TABLE top_palabras (
    palabra      TEXT,
    frecuencia   INTEGER
);


-- VERIFICACIÓN DE EXISTENCIA DE TABLAS
SELECT
    (SELECT COUNT(*) FROM posts) AS total_posts,
    (SELECT COUNT(*) FROM retencion_video) AS total_retencion,
    (SELECT COUNT(*) FROM top_palabras) AS total_palabras;