
# VERIFICAR CÓMO SE DIVIDEN LOS INTERVALOS DE RETENCIÓN
# (bloque independiente: relee los CSV limpios)

import pandas as pd
import numpy as np

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

posts = pd.read_csv("posts_clean.csv", encoding="utf-8-sig")
ret = pd.read_csv("retencion_video.csv", encoding="utf-8-sig")

curvas = (
    ret.groupby(["id_publicacion", "tipo_retencion"])
       .agg(n_intervalos=("intervalo", "count"),
            max_intervalo=("intervalo", "max"),
            suma_pct=("porcentaje", "sum"))
       .reset_index()
       .merge(posts[["id_publicacion", "tipo_publicacion",
                     "duracion_segundos", "segundos_promedio_total"]],
              on="id_publicacion")
)
# Se excluyen los posts con duración 0 (texto/fotos con metadata rara)
curvas = curvas[curvas["duracion_segundos"] > 0].copy()

print("=" * 60)
print("PRUEBA 1: videos cortos (<= 36 s) -> ¿el intervalo es 1 segundo?")
print("=" * 60)
cortos = curvas[curvas["duracion_segundos"] <= 36].copy()
cortos["esperado_bloque4"] = np.ceil(cortos["duracion_segundos"] / 4) * 4
cortos["dif_vs_duracion"] = cortos["max_intervalo"] - cortos["duracion_segundos"]
contiguas = (cortos["n_intervalos"] == cortos["max_intervalo"] + 1).mean()
coincide = (cortos["max_intervalo"] == cortos["esperado_bloque4"]).mean()
print(f"Curvas analizadas: {len(cortos)}")
print(f"Correlación duración vs intervalo máximo: "
      f"{cortos['duracion_segundos'].corr(cortos['max_intervalo']):.3f}")
print(f"Diferencia (intervalo máx - duración), mediana: "
      f"{cortos['dif_vs_duracion'].median():.1f} | rango: "
      f"{cortos['dif_vs_duracion'].min():.0f} a {cortos['dif_vs_duracion'].max():.0f}")
print(f"Curvas sin huecos (todos los intervalos 0..max presentes): {contiguas:.1%}")
print(f"Intervalo máx = duración redondeada al siguiente múltiplo de 4: {coincide:.1%}")
print("Intervalo máximo más frecuente:")
print(cortos["max_intervalo"].value_counts().sort_index().to_string())

print("\n" + "=" * 60)
print("PRUEBA 2: videos largos (> 40 s) -> ¿todos llegan a 40?")
print("=" * 60)
largos = curvas[curvas["duracion_segundos"] > 40]
print(f"Curvas analizadas: {len(largos)}")
print(f"Curvas con los 41 intervalos: {(largos['n_intervalos'] == 41).mean():.1%}")

print("\n" + "=" * 60)
print("PRUEBA 3: en videos largos, ¿los 41 puntos son los primeros 40 s")
print("          o el video completo escalado (duración / 40)?")
print("=" * 60)
g = curvas[(curvas["tipo_retencion"] == "general")
           & (curvas["segundos_promedio_total"] > 0)].copy()
corto_g = g[g["duracion_segundos"] <= 40]
# Factor de calibración: en videos cortos (1 punto = 1 s) la suma de la
# curva debería aproximar los segundos promedio reproducidos.
factor = (corto_g["segundos_promedio_total"] / corto_g["suma_pct"]).median()
print(f"Factor de calibración (segundos promedio / suma de la curva, videos <= 40 s): {factor:.2f}")

largo_g = g[g["duracion_segundos"] > 40].copy()
largo_g["pred_primeros_40s"] = largo_g["suma_pct"] * factor
largo_g["pred_escalado"] = largo_g["suma_pct"] * largo_g["duracion_segundos"] / 40 * factor

def error_tipico(pred):
    # factor multiplicativo típico de error (1.0 = perfecto)
    return float(np.exp(np.median(np.abs(np.log(pred / largo_g["segundos_promedio_total"])))))

e1 = error_tipico(largo_g["pred_primeros_40s"])
e2 = error_tipico(largo_g["pred_escalado"])
print(f"Videos largos analizados: {len(largo_g)}")
print(f"Error típico si son los primeros 40 s : x{e1:.2f}")
print(f"Error típico si es el video escalado  : x{e2:.2f}")

largo_g["rango_duracion"] = pd.cut(
    largo_g["duracion_segundos"], [40, 60, 120, 300, 900, 100000],
    labels=["41-60 s", "1-2 min", "2-5 min", "5-15 min", "15+ min"])
resumen = largo_g.groupby("rango_duracion", observed=True).agg(
    videos=("suma_pct", "size"),
    seg_prom_reales=("segundos_promedio_total", "median"),
    pred_primeros_40s=("pred_primeros_40s", "median"),
    pred_escalado=("pred_escalado", "median"),
).round(1)
print("\nMedianas por rango de duración:")
print(resumen.to_string())

print("\nCONCLUSIÓN AUTOMÁTICA:")
if e2 < e1:
    print(" -> Se ajusta mejor 'video completo escalado': en videos > 40 s cada intervalo ~ duración/40 segundos.")
else:
    print(" -> Se ajusta mejor 'primeros 40 segundos': cada intervalo ~ 1 segundo también en videos largos.")