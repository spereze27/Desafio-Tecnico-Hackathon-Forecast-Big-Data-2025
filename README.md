# Desafío Técnico – Hackathon Forecast Big Data 2025
## Proyecto de Predicción de Ventas para el Sector Retail

### Resumen del Proyecto

Este repositorio contiene la solución desarrollada para el **Hackathon Forecast Big Data 2025**. El proyecto consiste en la creación de un modelo de machine learning para predecir la cantidad de ventas semanales por producto (SKU) y por punto de venta (PDV). Utilizando un historial de transacciones, registros de productos e información de los PDVs correspondientes al año 2022, el modelo genera predicciones de demanda para las cinco primeras semanas de enero de 2023.

La solución busca abordar un desafío real del sector retail, inspirado en el producto **One-Click Order**, con el fin de optimizar la gestión de inventario y el proceso de reposición de productos.

---

### 🎯 Objetivo

El objetivo principal de este proyecto es **desarrollar un modelo de *pronóstico* (predicción) preciso y robusto** que estime la cantidad de ventas semanales por Punto de Venta (PDV) y SKU para las cinco primeras semanas de enero de 2023.

Las predicciones generadas tienen como finalidad proporcionar una herramienta de apoyo a la decisión para el sector retail, permitiendo:

-   **Optimizar la gestión de inventario:** Garantizar que cada PDV tenga la cantidad ideal de cada producto.
-   **Automatizar la reposición:** Facilitar la creación de pedidos de reposición de forma automática e inteligente.
-   **Reducir costos operativos:** Minimizar tanto el exceso de inventario (costos de almacenamiento) como las roturas de stock (pérdida de ventas por falta de producto).


---

### ⚙️ Metodología

La solución se desarrolló siguiendo un flujo de trabajo estructurado, comenzando con el entendimiento y preparación de los datos, hasta la construcción y entrenamiento del modelo de pronóstico.

#### 1. Perfilado y Análisis Exploratorio de Datos (EDA)

El primer paso consistió en realizar un **perfilado de datos** (`data profiling`) para inspeccionar en detalle los archivos Parquet proporcionados.

* **¿Por qué es importante?** El perfilado de datos es un paso fundamental que permite entender la estructura, calidad y contenido de los datos. Ayuda a identificar el esquema (nombre y tipo de las columnas), detectar valores nulos o inconsistentes, entender la distribución de las variables y verificar las relaciones entre las tablas. Una comprensión clara de los datos desde el inicio es crucial para tomar decisiones informadas en las etapas de limpieza, ingeniería de características y modelado.

#### 2. Elección de la Tecnología: Spark vs. Pandas/Polars

El conjunto de datos de transacciones contiene **más de 6 millones de registros**, lo que lo clasifica como un problema de Big Data. Para procesar este volumen de información de manera eficiente, se eligió **Apache Spark**.

* **¿Por qué Spark?** Mientras que librerías como **Pandas** o **Polars** son extremadamente eficientes para conjuntos de datos que caben en la memoria RAM de una sola máquina (procesamiento de nodo único), **Spark** está diseñado para el **procesamiento distribuido**. Spark divide los datos y las operaciones a través de un clúster de múltiples máquinas, ejecutando tareas en paralelo. Esta arquitectura le permite escalar horizontalmente y manejar volúmenes de datos que superan con creces la capacidad de un solo computador, garantizando un rendimiento óptimo para este desafío.

#### 3. Estructura y Relación de los Datos

Los datos se encuentran distribuidos en tres tablas principales: `productos`, `pdvs` (puntos de venta) y `transacoes` (transacciones). La tabla `transacoes` actúa como la tabla de hechos, conectándose con las otras dos a través de las claves foráneas `produto` y `pdv`.

A continuación se muestra el esquema de la relación entre las tablas:

![Diagrama de relación de tablas de la base de datos](https://raw.githubusercontent.com/spereze27/Desafio-Tecnico-Hackathon-Forecast-Big-Data-2025/main/union_tablas.png)

A continuación, se presenta una vista previa del contenido de cada tabla.

---

### 🛍️ Datos de Productos

Esta tabla contiene la información detallada de cada producto.

| produto             | categoria         | descricao                |
| ------------------- | ----------------- | ------------------------ |
| `2282334733936076502` | `Distilled Spirits` | `JOSEPH CARTRON CA...`   |
| `6091840953834683482` | `Distilled Spirits` | `SPRINGBANK 18 YEA...`   |
| `1968645851245092408` | `Distilled Spirits` | `J BRANDT TRIPLE S...`   |
| `994706710729219179`  | `Draft`             | `REFORMATION CASHM...`   |
| `9209550539540384349` | `Non-Alcohol`       | `HELLA MOSCOW MULE...`   |

---

### 🛒 Datos de Transacciones

Esta es la tabla de hechos que registra cada venta, vinculando un producto con un punto de venta.

| pdv                 | produto             | transaction_date | quantity |
| ------------------- | ------------------- | ---------------- | -------- |
| `7384367747233276219` | `328903483604537190`  | `2022-07-13`     | `1.0`      |
| `3536908514005606262` | `5418855670645487653` | `2022-03-21`     | `6.0`      |
| `3138231730993449825` | `1087005562675741887` | `2022-09-06`     | `3.0`      |
| `3681167389484217654` | `1401422983880045188` | `2022-09-11`     | `129.0`    |
| `7762413312337359369` | `6614994347738381720` | `2022-02-18`     | `1.0`      |

---

### 🏪 Datos de PDVs (Puntos de Venta)

Aquí se almacena la información de los diferentes puntos de venta.

| pdv                 | premise     | categoria_pdv  | zipcode |
| ------------------- | ----------- | -------------- | ------- |
| `2204965430669363375` | `On Premise`  | `Mexican Rest` | `30741` |
| `5211957289528622910` | `On Premise`  | `Hotel/Motel`  | `80011` |
| `9024493554530757353` | `Off Premise` | `Convenience`  | `80751` |
| `8659197371382902429` | `On Premise`  | `Restaurant`   | `80439` |
| `1400854873763881130` | `On Premise`  | `Restaurant`   | `30093` |
