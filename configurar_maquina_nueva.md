# Configurar una máquina nueva

Pasos para recrear el entorno de trabajo del proyecto desde cero en una computadora con Windows. Tiempo estimado: de 30 a 40 minutos, casi todo en descargas.

Qué trae el clon del repositorio y qué no:

| Llega con el clon | No llega (hay que prepararlo) | Por qué |
|---|---|---|
| Scripts de `src`, notebooks, archivos `.sql`, `docs`, `requirements.txt`, `.gitignore`, README, historial | `.venv` | Pesa mucho y es regenerable; está en el `.gitignore` |
| | Los `.sav` del INE | Los datos nunca se suben al repositorio |
| | `data\interim` y `data\processed` | Son datos; se regeneran con el script 01 y los notebooks |
| | `db\ephpm.duckdb` | Binario regenerable |
| | Carpetas vacías (`db`, `reports\tablas`, `data\raw`) | Git no guarda carpetas sin archivos |
| | Programas y extensiones | Son de cada máquina |

Antes de empezar, en la máquina de origen, comprueba que el último commit esté subido: en GitHub Desktop, si arriba dice **Push origin**, púlsalo. Un commit sin push solo existe en esa computadora.

## A. Programas (una sola vez)

1. **Python.** Descarga la versión 3.12.x desde python.org/downloads (la misma que usa el proyecto) y ábrela. En la primera pantalla marca **Add python.exe to PATH** y pulsa Install Now. Abre una PowerShell nueva y escribe `python --version`. Debe decir `Python 3.12.x`.
2. **Visual Studio Code.** Instálalo desde code.visualstudio.com. Dentro, ve a View > Extensions e instala **Python** y **Jupyter** (busca cada nombre y pulsa Install).
3. **GitHub Desktop.** Instálalo desde desktop.github.com (ya incluye Git). Entra en File > Options > Accounts > Sign in con tu cuenta de GitHub.
4. **Power BI Desktop** (solo para el tablero). Microsoft Store > Power BI Desktop > Instalar.

## B. Clonar y abrir

5. En GitHub Desktop: File > Clone repository > pestaña GitHub.com > elige `proyecto1-ehpm-desempleo`. En **Local path** escribe `C:\dev\proyecto1-ehpm-desempleo` y pulsa Clone. Usa una ruta corta para evitar el error *Filename too long*.

   Alternativa sin GitHub Desktop, desde una terminal:

   ```
   git clone https://github.com/<usuario>/proyecto1-ehpm-desempleo.git C:\dev\proyecto1-ehpm-desempleo
   ```

6. Cambia a la rama de trabajo. En GitHub Desktop, en Current branch elige `fase-1-limpieza`. Si no aparece, pulsa antes Fetch origin. Si sigue sin aparecer, es que no se subió desde la otra máquina: vuelve allá y pulsa Push origin.
7. Abre la carpeta en VS Code con Repository > Open in Visual Studio Code. Si VS Code pregunta si confías en los autores, elige **Yes, I trust the authors**.

## C. Recrear el entorno

8. En VS Code: Terminal > New Terminal. Escribe `pwd`; debe terminar en `proyecto1-ehpm-desempleo`.
9. Crea el entorno virtual (tarda medio minuto):

   ```
   python -m venv .venv
   ```

   Si aparece una ventana que dice que se detectó un nuevo entorno, elige **Yes**.
10. Actívalo:

    ```
    .venv\Scripts\Activate.ps1
    ```

    Debe aparecer `(.venv)` al inicio de la línea. Si Windows bloquea el script, ejecuta una sola vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y repite.
11. Instala las librerías (varios minutos):

    ```
    pip install -r requirements.txt
    ```

    Al final debe decir `Successfully installed ...`.
12. Elige el intérprete: Ctrl+Shift+P > `Python: Select Interpreter` > la opción que termina en `.venv\Scripts\python.exe`.
13. Comprueba que todo importa:

    ```
    python -c "import pandas, pyarrow, pyreadstat, duckdb; print('ok')"
    ```

    Debe imprimir `ok`.

## D. Carpetas y datos

14. Crea las carpetas que Git no trajo:

    ```
    mkdir data\raw
    mkdir data\interim
    mkdir data\processed
    mkdir db
    mkdir reports\tablas
    ```

15. Coloca los `.sav` de la EPHPM en `data\raw` (por ejemplo, cópialos desde un USB o la nube, o descárgalos del sitio del INE). Comprueba con `dir data\raw`: deben estar `hogar_2024.sav` y los demás años que uses, con el nombre `hogar_AAAA.sav`. Los datos **no** viajan por GitHub.
16. Ejecuta la ingesta:

    ```
    python src\01_sav_a_parquet.py
    ```

    Debe imprimir una línea por año con filas y columnas, y al final `Listo.`. Revisa con `dir data\interim`.

## E. Verificación final

17. **Mismos datos que en la otra máquina.** Abre `data\interim\control_ingesta.csv` y compara la fila de 2024 (filas, columnas y `sha256`) con la de la otra máquina. Si coinciden, trabajas con exactamente el mismo archivo.
18. **GitHub Desktop sin cambios.** En la pestaña Changes debe decir **0 changed files**. Si aparece `.venv` o algo de `data\`, el `.gitignore` no se está aplicando.
19. **Notebooks.** Cuando existan, abre cada uno en `notebooks` y ejecútalo de arriba abajo, en orden numérico, para regenerar `data\processed` y `db\ephpm.duckdb`.

## Si algo falla

| Síntoma | Qué hacer |
|---|---|
| `python` no se reconoce | No se marcó *Add python.exe to PATH*: reinstala Python con esa casilla |
| Error de versión en `pip install -r requirements.txt` | Tu Python no es 3.12: instala esa versión y recrea `.venv` |
| `(.venv)` no aparece en la terminal | Repite el paso 10 |
| El script dice que encontró 0 archivos `.sav` | Revisa `dir data\raw` y que los archivos se llamen `hogar_AAAA.sav` |

## Trabajar entre dos máquinas

- Cierra cada sesión con commit y **Push origin**.
- Abre cada sesión con **Fetch origin** y **Pull origin**. Si editas en las dos máquinas sin hacer pull, aparecen conflictos que son molestos de resolver.
- Anota en `docs\bitacora.md` en cuál máquina quedó el último trabajo.
