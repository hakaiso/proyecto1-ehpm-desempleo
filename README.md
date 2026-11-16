# Proyecto 1 — Mercado laboral de Honduras (EPHPM)

Reporte y **tablero** de indicadores clave del mercado de trabajo hondureño a partir de la
Encuesta Permanente de Hogares de Propósitos Múltiples (EPHPM) del INE.

Es la **Fase 1** del proyecto de tesis *«El desempleo en Honduras 2001–2024»*: sirve como
preparación para un puesto de análisis de datos y produce insumos reutilizables para la tesis.
Limpieza en **Python/Jupyter**, con **SQL** (SQLite/DuckDB) de forma transversal y
visualización en un tablero.

---

## Estructura del repositorio

```
proyecto1-ehpm-desempleo/
├── data/
│   ├── raw/         # .sav/.dta originales (INMUTABLES, NO versionados)
│   ├── sample/      # muestra pequeña versionable para pruebas
│   └── processed/   # tablas finales (NO versionadas)
├── sql/             # consultas .sql de los indicadores (versionadas)
├── notebooks/       # 01_ingesta, 02_limpieza, 03_carga_bd, 04_indicadores_sql ...
├── src/             # funciones reutilizables (p. ej. 01_sav_a_parquet.py)
├── dashboard/       # app de Streamlit o archivo .pbix de Power BI
├── docs/            # diccionario de salida, esquema de la base, bitácora
├── tests/           # pruebas de las funciones de limpieza
├── .gitignore
└── README.md
```

> Los **datos no se versionan** (`data/raw/`, `data/processed/`, `*.sav`, `*.dta`, `*.parquet`
> están en `.gitignore`). En GitHub viaja el **código**, no los microdatos: en cada máquina hay
> que colocar los `.sav` en `data/raw/`. La EPHPM es pública, así que el resultado es reproducible.

---

## Puesta en marcha

Requiere **Python 3.12**.

```bash
# 1. Clonar (solo la primera vez en una máquina nueva)
git clone https://github.com/hakaiso/proyecto1-ehpm-desempleo.git
cd proyecto1-ehpm-desempleo

# 2. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows (PowerShell/CMD)
# source .venv/bin/activate   # macOS / Linux

# 3. Instalar dependencias (cuando exista requirements.txt)
pip install -r requirements.txt

# 4. Colocar los microdatos en data/raw/  (no vienen en el repo)
```

> Pendiente: fijar las versiones con `pip freeze > requirements.txt` y commitearlo,
> para que el entorno sea reproducible en cualquier máquina.

---

## Sincronización con GitHub (flujo de trabajo)

**Git no sincroniza solo, como OneDrive.** Hay que subir y bajar los cambios a mano. Este repo
vive en `C:\dev\…`, **fuera de OneDrive, a propósito** (evita conflictos con la carpeta `.git`).

### El ciclo del día a día (línea de comandos)

```bash
# --- Antes de empezar a trabajar: traer lo último de GitHub ---
git pull

# --- Mientras trabajás: guardar avances ---
git status                       # ver qué cambió
git add .                        # preparar todos los cambios (o: git add <archivo>)
git commit -m "Describe el cambio en pocas palabras"

# --- Al terminar (o cada tanto): subir a GitHub ---
git push
```

Regla mínima: **`pull` al empezar, `commit` seguido de `push` al terminar.** Con eso, GitHub
siempre tiene tu última versión y podés seguir desde cualquier máquina.

### Lo mismo con GitHub Desktop (sin comandos)

1. **Fetch origin** (arriba a la derecha) al empezar → si dice *Pull origin*, hacé clic para bajar cambios.
2. Trabajá en tus archivos normalmente.
3. En la pestaña **Changes**, escribí un resumen y pulsá **Commit to main**.
4. Pulsá **Push origin** para subirlo a GitHub.

### Comandos útiles de apoyo

```bash
git status            # ¿qué cambió y qué falta commitear?
git log --oneline -10 # historial reciente de commits
git fetch             # consultar GitHub sin fusionar (solo mira si hay novedades)
git diff              # ver exactamente qué líneas cambiaron
```

### Consejos

- **Commits pequeños y descriptivos** («añade carga a SQLite», «corrige subempleo invisible»),
  no «cambios varios». El historial debe contar una historia.
- Si trabajás en **dos máquinas**, hacé `push` al terminar en una y `pull` al empezar en la otra;
  nunca edites en ambas sin sincronizar, o aparecerán conflictos.
- **No muevas este repo dentro de OneDrive.** Dejalo en `C:\dev\`.

---

## Fases del proyecto

- **Fase 1 (este repo):** reporte + tablero con indicadores del mercado laboral; limpieza en
  Python, indicadores en SQL, documentación completa.
- **Fase 2:** la tesis — serie 2001–2024 del ejército industrial de reserva ampliado y modelos
  probit/logit. Ver la guía de limpieza del proyecto para el detalle por fase.
