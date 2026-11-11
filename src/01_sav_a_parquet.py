"""
01_sav_a_parquet.py
===================
Capa RAW -> capa PROCESSED del pipeline de la EPHPM.

Qué hace, para cada archivo .sav de data/raw:
  1. Lo lee con pyreadstat (formato original del INE, SPSS).
  2. Lo guarda como Parquet en data/processed (rápido, compacto, con tipos).
  3. Exporta las etiquetas de variables y de valores a un JSON.
  4. Calcula el hash SHA-256 del .sav original (huella de control).
  5. Escribe un resumen de todo el proceso en control_ingesta.csv.

Los .sav originales NUNCA se modifican.

Cómo ejecutarlo (desde la raíz del proyecto, con el entorno virtual activo):
    python src\\01_sav_a_parquet.py
"""

# ---------------------------------------------------------------------------
# 1. IMPORTACIONES
# Librerías que usa el script:
#   hashlib   -> calcula el hash (huella digital) de un archivo
#   json      -> guarda las etiquetas en formato JSON
#   re        -> expresiones regulares, para sacar el año del nombre
#   Path      -> manejo de rutas de carpetas y archivos
#   pandas    -> tablas de datos (DataFrame)
#   pyreadstat-> lee archivos .sav de SPSS
# ---------------------------------------------------------------------------
import hashlib, json, re
from pathlib import Path
import pandas as pd
import pyreadstat


# ---------------------------------------------------------------------------
# 2. RUTAS
# Las rutas se calculan a partir de la ubicación de este script, así que
# funciona aunque lo ejecutes desde otra carpeta.
#   RAIZ -> carpeta principal del proyecto (dos niveles arriba de este archivo)
#   RAW  -> donde están los .sav originales
#   OUT  -> donde se guardan los Parquet, los JSON y el control
# ---------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent.parent
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)  # crea la carpeta si no existe


# ---------------------------------------------------------------------------
# 3. FUNCIÓN DE HASH (huella digital del archivo)
# Lee el archivo por bloques de 1 MB (para no cargar todo en memoria) y
# devuelve su SHA-256. Si el .sav cambia aunque sea un byte, el hash cambia.
# Sirve para demostrar que trabajaste con el archivo original sin alterar.
# ---------------------------------------------------------------------------
def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloque)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# 4. BÚSQUEDA DE ARCHIVOS
# Lista todos los .sav de data/raw. Imprime dónde busca y cuántos encontró.
# Si no hay ninguno, se detiene con un mensaje claro en lugar de terminar
# en silencio.
# ---------------------------------------------------------------------------
archivos = sorted(RAW.glob("*.sav"))
print(f"Buscando en: {RAW}")
print(f"Archivos .sav encontrados: {len(archivos)}")
if not archivos:
    raise SystemExit("No hay .sav en data/raw. Revisa la carpeta y los nombres.")


# ---------------------------------------------------------------------------
# 5. BUCLE PRINCIPAL: un archivo .sav a la vez
# ---------------------------------------------------------------------------
control = []  # aquí se acumula una fila de resumen por archivo

for sav in archivos:

    # --- 5.1 Identificar el año y el nombre base ---------------------------
    # Busca un año (2000 a 2099) dentro del nombre del archivo, por ejemplo
    # "hogar_2019.sav" -> 2019. Si no hay año, el archivo se omite.
    # "nombre" es el nombre en minúsculas y sin espacios (ej. hogar_2019);
    # se usa para nombrar los archivos de salida.
    m = re.search(r"(20\d{2})", sav.stem)
    if not m:
        print(f"Sin año en el nombre, se omite: {sav.name}")
        continue
    anio = int(m.group(1))
    nombre = re.sub(r"\s+", "_", sav.stem.lower())

    # --- 5.2 Leer el .sav ---------------------------------------------------
    # apply_value_formats=False: deja los códigos numéricos tal cual (por
    # ejemplo 1, 2) en lugar de reemplazarlos por texto. Las etiquetas se
    # guardan aparte (bloque 5.4) y se aplican después en una tabla de
    # dimensiones, para que el mismo código no cambie de texto según el año.
    # Si la lectura falla por la codificación de caracteres (común en
    # archivos antiguos con tildes y eñes), reintenta con "latin1".
    try:
        df, meta = pyreadstat.read_sav(sav, apply_value_formats=False)
    except Exception:
        df, meta = pyreadstat.read_sav(sav, apply_value_formats=False,
                                       encoding="latin1")

    # --- 5.3 Normalizar y guardar en Parquet --------------------------------
    # Pasa los nombres de columna a minúsculas (evita errores por mayúsculas
    # distintas entre años), añade la columna "anio" y guarda en Parquet.
    df.columns = [c.lower() for c in df.columns]
    df["anio"] = anio
    df.to_parquet(OUT / f"{nombre}.parquet", index=False)

    # --- 5.4 Exportar las etiquetas a JSON ----------------------------------
    # Parquet no guarda las etiquetas del .sav, así que se exportan aparte:
    #   "variables": nombre de variable -> descripción (ej. edad -> "Edad")
    #   "valores":   nombre de variable -> {código: texto} (ej. 1 -> "Hombre")
    # Este archivo es la materia prima del diccionario de datos y de la
    # armonización entre años.
    etiquetas = {
        "variables": dict(zip([c.lower() for c in meta.column_names],
                              meta.column_labels)),
        "valores": {k.lower(): v for k, v in
                    meta.variable_value_labels.items()},
    }
    with open(OUT / f"etiquetas_{nombre}.json", "w", encoding="utf-8") as f:
        json.dump(etiquetas, f, ensure_ascii=False, indent=2, default=str)

    # --- 5.5 Registrar el control de este archivo ---------------------------
    # Guarda año, archivo, filas, columnas y el hash del .sav original.
    # Las filas y columnas permiten detectar lecturas incompletas; el hash,
    # que el archivo de origen no se alteró.
    control.append({"anio": anio, "archivo": sav.name,
                    "filas": len(df), "columnas": df.shape[1],
                    "sha256": sha256(sav)})
    print(f"{anio} ({sav.name}): {len(df):,} filas, {df.shape[1]} columnas")


# ---------------------------------------------------------------------------
# 6. REPORTE FINAL
# Guarda el resumen de todos los archivos procesados en un CSV. Este archivo
# es el primer control de calidad del pipeline: se compara con los totales
# publicados y se conserva como evidencia de la ingesta.
# ---------------------------------------------------------------------------
pd.DataFrame(control).to_csv(OUT / "control_ingesta.csv", index=False)
print("Listo.")