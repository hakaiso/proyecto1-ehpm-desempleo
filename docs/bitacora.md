# Bitácora del proyecto

Proyecto 1: desempleo e informalidad con la EPHPM (2024). Entradas de la más reciente a la más antigua.

## 16-11-2026 · S1(preparación) y arranque de S2 · máquina: <CRUZ ROJA>

* Meta: dejar listo el entorno y la estructura del proyecto para limpiar la EPHPM 2024, y empezar a revisar qué contiene `hogar\\\\\\\_2024`
* Hecho:

  * Abrí la carpeta `proyecto1-ehpm-desempleo` en VS Code. El notebook usa el kernel `.venv (Python 3.12.0)`.
  * Instalé las librerías de la guía (pandas, pyarrow, pyreadstat, duckdb, jupyter, matplotlib, seaborn, pandera, ipykernel) y generé `requirements.txt`.
  * Verifiqué que la ingesta ya estaba hecha: hay un Parquet y un `etiquetas\\\\\\\_hogar\\\\\\\_AAAA.json` por año (2001 en adelante) y `control\\\\\\\_ingesta.csv`, generados el 9/11/2026.
  * Moví esos archivos de `data\\\\\\\\processed` a `data\\\\\\\\interim`.
  * Dejé el `.gitignore` con `data/`, `db/\\\\\\\*.duckdb` y `db/\\\\\\\*.wal`.
  * Comprobé que no existe una carpeta `dashboard}` creada por error.
  * Hice el commit de la preparación en la rama `fase-1-limpieza`.
  * Primer notebook creado: `limpieza-portafolio-2024`.
* Hallazgo: **`hogar\\\\\\\_2024` es un archivo de personas** (una fila por persona), aunque el nombre diga «hogar». Resuelve la duda principal de S2.
* Decisión: trabajar S1 a S9 en `fase-1-limpieza` y fusionar a `main` al cerrar S9. Motivo: `main` queda estable mientras hago pruebas.
* Decisión: la conversión del `.sav` va a `data\\\\\\\\interim` y `data\\\\\\\\processed` queda solo para tablas limpias. Motivo: separar «original en otro formato» de «tabla validada» y poder regenerar `processed` sin releer los `.sav`.
* Decisión: el `.gitignore` excluye `data/` completo y `db/\\\\\\\*.duckdb`. Motivo: que ningún dato ni la base lleguen a GitHub.
* Problema: `requirements.txt` no aparecía en la raíz. Causa probable: la terminal no estaba en la raíz o no se ejecutó la segunda línea. Solución: desde la raíz y con `(.venv)` visible, instalar los paquetes con `pip install ...` y ejecutar `pip freeze | Out-File -Encoding utf8 requirements.txt`.
* Hallazgo: `etiquetas\\\\\\\_hogar\\\\\\\_2001.json` pesa 27 KB y el de 2005, 2.475 KB; de 2010 en adelante rondan los 60 KB. Coincide con que el `.sav` de 2001 trae pocas etiquetas de valor.
* Pendiente o dudoso:

  * Verificar que `src\\\\\\\\01\\\\\\\_sav\\\\\\\_a\\\\\\\_parquet.py` apunta a `"data" / "interim"` (buscar `"data" / "processed"` con Ctrl+F; si aparece, cambiarlo a `"interim"`).
  * Anotar en `docs\\\\\\\\fuentes.md` que `hogar\\\\\\\_2024` es de personas, con filas, columnas y la clave de identificación (S2).
  * Decidir qué hacer con `data\\\\\\\\sample` (viene de un `mkdir` inicial; no se usa en la guía).
  * Colocar `docs\\\\\\\\configurar\\\\\\\_maquina\\\\\\\_nueva.md` y añadir el enlace en el README.
* Siguiente paso: en el notebook `limpieza-portafolio-2024`, pegar la celda estándar, leer `data\\\\\\\\interim\\\\\\\\hogar\\\\\\\_2024.parquet`, contar filas y columnas y buscar la combinación de columnas que identifica a cada persona (S2).
* Commit: Prepara estructura y entorno para la limpieza de 2024 (ajusta el mensaje al que usaste)
* Se creó el docuemento de configuración de entornos entre máquinas y la bitácora del Proyecto ambos en C:\\dev\\proyecto1-ehpm-desempleo\\docs

## 17-11-2026· S2 Ingesta y limpieza de datos · máquina: <CRUZ ROJA>



* Añadí a la notebook la configuración correspondiente de las rutas a las bases de datos lo que tendrá que ser modificado en la otra m,áquina
* Decidí trabajar con los datos de 2026 por lo que se creó otro archive limpieza-portsfolio-2025
* La dimensiones parecen las correctas
* Se verificó que los nombres de las variables son los mismos para 2024 y 2025 con excepción de las horas trabajadas qu en 2025 es TOTHRSOP
* Se creó la Nueva table de las 14 variables con las que se trabajará en el análisis
* La mayoría de las varianles son categoricas, queda pendiente corroborar con precision el tipo para cada una y determiner si se Deben agragar más variables para el análisis.

## 19-11-2026· S3 limpieza de datos · máquina: <CRUZ ROJA>



* Se prosiguio con la limpieza agregando 8 nuevas variables a la base de trabajo \[base] para estimar los indicadores del mercado de trabajo requeridos, esta fueron:departamento (DEPTO), ingreso total, ingreso de la ocupacion principal y secundaria (ytrab, ytraop, ytraos respectivamente); variables para estimar informalidad  "aguinaldo": "OC620", "catorceavo": "OC621", "vacaciones": "OC622 y la variable pregunta si desearia trabajar mas horas CA522.
* Se comenzó a perfilar las variables para limpiar, faltantes, centinelas y valores fuera de rango, comprobándose que en la variable de inactividad muchos valores correspondían a una categoría "Inactivos fuera de la fuerza de trabajo potencial" que fue creada comparando con las etiquetas del archive meta de etiquetas de metadatos asociado a las bases de datos .sav.

