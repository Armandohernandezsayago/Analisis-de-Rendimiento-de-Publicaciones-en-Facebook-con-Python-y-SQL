-- 1. ¿A qué hora los videos tienen mejor desempeño? (solo horas con 10+ videos)

SELECT
    hora_publicacion,
    COUNT(*) AS num_videos,
    ROUND(AVG(reproducciones_3s)) AS promedio_reproducciones_3s,
    ROUND(AVG(comentarios), 1) AS promedio_comentarios,
    ROUND(AVG(reacciones), 1) AS promedio_reacciones
FROM posts
WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
GROUP BY hora_publicacion
HAVING COUNT(*) >= 10
ORDER BY promedio_reproducciones_3s DESC;


-- 2. ¿Qué día de la semana funciona mejor para los videos?

SELECT
    dia_semana,
    COUNT(*) AS num_videos,
    ROUND(AVG(reproducciones_3s)) AS promedio_reproducciones_3s,
    ROUND(AVG(alcance)) AS promedio_alcance
FROM posts
WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
GROUP BY dia_semana
ORDER BY promedio_reproducciones_3s DESC;


-- 3a. Curva de retención promedio — videos de HASTA 40 s (para graficar en Power BI)
--     Aquí cada intervalo = 1 segundo. Solo videos (sin Reels, fotos ni texto).
--     Al final num_videos baja porque los videos cortos ya terminaron.

SELECT
    r.tipo_retencion,
    r.intervalo AS segundo,
    COUNT(*) AS num_videos,
    ROUND(AVG(r.porcentaje) * 100, 1) AS retencion_promedio_pct
FROM retencion_video r
JOIN posts p ON p.id_publicacion = r.id_publicacion
WHERE p.tipo_publicacion = 'Videos'
  AND p.duracion_segundos > 0
  AND p.duracion_segundos <= 40
GROUP BY r.tipo_retencion, r.intervalo
ORDER BY r.tipo_retencion, r.intervalo;


-- 3b. Curva de retención promedio — videos de MÁS de 40 s
--     Aquí el video se divide en 40 partes iguales: cada intervalo es el
--     2.5% del video (intervalo 20 = la mitad del video).

SELECT
    r.tipo_retencion,
    r.intervalo * 2.5 AS pct_del_video,
    COUNT(*) AS num_videos,
    ROUND(AVG(r.porcentaje) * 100, 1) AS retencion_promedio_pct
FROM retencion_video r
JOIN posts p ON p.id_publicacion = r.id_publicacion
WHERE p.tipo_publicacion = 'Videos'
  AND p.duracion_segundos > 40
GROUP BY r.tipo_retencion, r.intervalo
ORDER BY r.tipo_retencion, r.intervalo;


-- 4. Palabras más usadas en las descripciones  

SELECT palabra, frecuencia
FROM top_palabras
ORDER BY frecuencia DESC
LIMIT 15;


-- 5. Comparación entre tipos de contenido — para gráfico de barras general  

SELECT
    tipo_publicacion,
    COUNT(*) AS num_publicaciones,
    ROUND(AVG(alcance), 0) AS alcance_promedio,
    ROUND(AVG(reacciones + comentarios + veces_compartido), 1) AS interaccion_promedio
FROM posts
GROUP BY tipo_publicacion
ORDER BY alcance_promedio DESC;


-- 6. Mapa de calor día × hora — para una matriz/heatmap en Power BI
--    (solo combinaciones con 5+ videos)

SELECT
    dia_semana,
    hora_publicacion,
    COUNT(*) AS num_videos,
    ROUND(AVG(reproducciones_3s)) AS promedio_reproducciones_3s
FROM posts
WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
GROUP BY dia_semana, hora_publicacion
HAVING COUNT(*) >= 5
ORDER BY dia_semana, hora_publicacion;


-- 7. ¿La duración del video importa?

SELECT
    CASE
        WHEN duracion_segundos < 30 THEN '1) < 30s'
        WHEN duracion_segundos < 60 THEN '2) 30-60s'
        WHEN duracion_segundos < 180 THEN '3) 1-3 min'
        ELSE '4) 3+ min'
    END AS rango_duracion,
    COUNT(*) AS num_videos,
    ROUND(AVG(reproducciones_3s)) AS promedio_reproducciones_3s,
    ROUND(AVG(comentarios), 1) AS promedio_comentarios
FROM posts
WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
GROUP BY rango_duracion
ORDER BY rango_duracion;


-- 8. Evolución mensual — para una línea de tendencia

SELECT
    strftime('%Y-%m', fecha_hora_publicacion) AS anio_mes,
    COUNT(*) AS num_videos,
    ROUND(AVG(alcance), 0) AS alcance_promedio,
    ROUND(SUM(reacciones + comentarios + veces_compartido), 0) AS interacciones_totales
FROM posts
WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
GROUP BY anio_mes
ORDER BY anio_mes;


-- 9a. Los 10 mejores videos usando reproducciones_3s 

SELECT titulo, fecha_hora_publicacion, hora_publicacion, duracion_segundos,
       reproducciones_3s, comentarios, alcance
FROM posts
WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
ORDER BY reproducciones_3s DESC
LIMIT 10;


-- 9b. Los 10 peores videos (ya excluye los casos con metadata incompleta)

SELECT titulo, fecha_hora_publicacion, hora_publicacion, duracion_segundos,
       reproducciones_3s, comentarios, alcance
FROM posts
WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
ORDER BY reproducciones_3s ASC
LIMIT 10;


-- 10. Retención individual de los 3 mejores videos — para elegir casos a destacar
--     Se filtra por id_publicacion (no por título, que podría repetirse).
--     Recordatorio: Para comparar curvas de videos de distinta duración, recorfemos que
--     en videos de 40 s o menos el intervalo es 1 s, y en los de más de 40 s
--     es duración/40 segundos.

SELECT p.titulo, p.duracion_segundos, r.tipo_retencion, r.intervalo,
       ROUND(r.porcentaje * 100, 1) AS retencion_pct
FROM retencion_video r
JOIN posts p ON p.id_publicacion = r.id_publicacion
WHERE p.id_publicacion IN (
    SELECT id_publicacion
    FROM posts
    WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
    ORDER BY reproducciones_3s DESC
    LIMIT 3
)
ORDER BY p.titulo, r.tipo_retencion, r.intervalo;


-- 11. CTE + función de ventana RANK() — los 3 mejores videos de cada mes

-- La CTE (WITH) arma una tabla temporal con el ranking ya calculado,
-- y la consulta de afuera solo filtra el resultado. Separar en dos
-- pasos así hace el SQL mucho más legible que anidar todo en un solo SELECT.
WITH ranking_mensual AS (
    SELECT
        titulo,
        strftime('%Y-%m', fecha_hora_publicacion) AS anio_mes,
        reproducciones_3s,
        RANK() OVER (
            PARTITION BY strftime('%Y-%m', fecha_hora_publicacion)
            ORDER BY reproducciones_3s DESC
        ) AS posicion_en_el_mes
    FROM posts
    WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
)
SELECT *
FROM ranking_mensual
WHERE posicion_en_el_mes <= 3
ORDER BY anio_mes, posicion_en_el_mes;


-- 12. Función de ventana AVG() OVER — compara cada video contra el promedio de su propio mes

-- A diferencia de un GROUP BY normal (que colapsa las filas), una función
-- de ventana calcula el promedio SIN perder el detalle de cada fila individual.
SELECT
    titulo,
    strftime('%Y-%m', fecha_hora_publicacion) AS anio_mes,
    reproducciones_3s,
    ROUND(AVG(reproducciones_3s) OVER (
        PARTITION BY strftime('%Y-%m', fecha_hora_publicacion)), 1) AS promedio_del_mes,
    ROUND(reproducciones_3s - AVG(reproducciones_3s) OVER (
        PARTITION BY strftime('%Y-%m', fecha_hora_publicacion)), 1) AS diferencia_vs_promedio
FROM posts
WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
ORDER BY anio_mes, diferencia_vs_promedio DESC;


-- 13. Subconsulta — videos que superaron el promedio general de TODOS los videos

-- La subconsulta entre paréntesis se resuelve primero (da un solo número:
-- el promedio general), y la consulta de afuera compara cada fila contra ese número.
SELECT titulo, strftime('%Y-%m', fecha_hora_publicacion) AS anio_mes, reproducciones_3s
FROM posts
WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
  AND reproducciones_3s > (
      SELECT AVG(reproducciones_3s)
      FROM posts
      WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
  )
ORDER BY reproducciones_3s DESC;


-- 14. ¿Dependes de pocos videos virales?
--     NTILE(10) reparte los videos en 10 grupos iguales (grupo 1 = el 10%
--     con más reproducciones) y se ve qué porcentaje del total aporta cada uno.

WITH videos AS (
    SELECT reproducciones_3s,
           NTILE(10) OVER (ORDER BY reproducciones_3s DESC) AS grupo
    FROM posts
    WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
)
SELECT
    grupo,
    COUNT(*) AS num_videos,
    ROUND(100.0 * SUM(reproducciones_3s) / (SELECT SUM(reproducciones_3s) FROM videos), 1) AS pct_del_total
FROM videos
GROUP BY grupo
ORDER BY grupo;


-- 15. ¿Los videos que mencionan una palabra tienen más reproducciones?
--     Cambiemos 'ramones' por la palabra que quieramos probar.

SELECT
    CASE WHEN descripcion LIKE '%ramones%' THEN 'La menciona'
         ELSE 'No la menciona' END AS grupo,
    COUNT(*) AS num_videos,
    ROUND(AVG(reproducciones_3s)) AS promedio_reproducciones_3s,
    ROUND(AVG(comentarios), 1) AS promedio_comentarios
FROM posts
WHERE tipo_publicacion = 'Videos' AND duracion_segundos > 0
GROUP BY grupo;