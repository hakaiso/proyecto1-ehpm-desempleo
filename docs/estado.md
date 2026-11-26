# Estado del proyecto: EPHPM 2025 (Proyecto 1)

Última actualización: 25/11/2026

## Resumen
Cálculo de indicadores del mercado laboral de la EPHPM 2025 (LXXXIII, julio 2025) con factor de expansión, contrastados con lo publicado por el INE. Flujo: raw → interim → processed → SQL (DuckDB) → Parquet/CSV → Power BI.

## Premisas (vigentes)
1. Se usan exactamente las definiciones operacionales de los documentos metodológicos del INE, más aproximaciones propias, solo para contrastar.
2. No se reconstruyen las decisiones internas del INE.
3. Toda contradicción, inconsistencia o brecha se registra en `docs/discrepancias.csv`.

## Hecho
- Limpieza: `data/processed/ephpm_2025_limpia.parquet` (28,714 filas; PET 20,953).
- Notebook `02_indicadores.ipynb` limpio (config, carga, banderas, indicadores y cortes, contraste, resumen de discrepancias).
- Indicadores estructurales coinciden con el INE (PET, PEA, ocupados, desocupados, TDA 4.9, TGP 58.2, asalariados).
- Variable oficial `subocup` reproduce 8.0 / 33.4.
- Contraste guardado en `docs/contraste_ine_2025.csv`; 23 discrepancias en `docs/discrepancias.csv`.
- Informe Word del proceso y hallazgos (25/11/2026).
- Práctica SQL: DuckDB + DBeaver con vista sobre el Parquet (PET = 7,363,421 verificado).

## Hallazgos clave
- Regla literal del documento (40 h): subocupación visible 6.8% (INE 8.0), invisible 39.5% (INE 33.4). El comportamiento de los datos corta en 44 h; la etiqueta dice 36 h.
- Medias de ingreso con `ytrab`: entre 1.4% y 2.7% sobre las del INE, siempre en el mismo sentido (D22 abierta).
- Informalidad: aproximación propia (A 42.8%, B 76.6%); el INE publica 74.8% de noviembre 2024. No es la definición del INE.

## Siguiente paso
1. Correr `02_indicadores` completo (con la corrección de `RAIZ`) y confirmar que no falla ningún assert.
2. Editar a mano las decisiones de D04 y D22 en `docs/discrepancias.csv`.
3. Crear `03_sql`: vistas en DuckDB que reproduzcan PET, PEA, ocupados, desocupados, TDA y TGP, y comprobar con asserts que cuadran con `data/indicadores/cortes_2025.parquet`.

## Pendientes
- Probar `ytraop` en las medias de ingreso y registrar el resultado en D22.
- Verificar las cifras del resumen ejecutivo del INE contra el PDF oficial.
- Verificar D18 (TDA por sexo de la cifra de prensa).
- Ingresos, subocupación oficial e informalidad (A y B, con advertencia) por cortes.
- Exportar Parquet para Power BI.
- Documentación: `docs/fuentes.md`, README, `docs/configurar_maquina_nueva.md`.

## Pausado por decisión de simplificar
- Nivel educativo derivado de `anosest`.
- Alineación de Pre-básica (D09).
- Identificación de las variables del método de informalidad del INE.

## Cómo retomar
Abrir VS Code en `c:\dev\proyecto1-ehpm-desempleo`, activar el entorno, leer este archivo y la última entrada de `docs/bitacora.md`.
