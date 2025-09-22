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

A continuación se muestra el esquema de la relación entre las tablas:

![Diagrama de relación de tablas de la base de datos](https://raw.githubusercontent.com/spereze27/Desafio-Tecnico-Hackathon-Forecast-Big-Data-2025/main/union_tablas.png)

## 🧹 Preprocesamiento Básico

Antes de realizar el análisis y modelado, se llevó a cabo un preprocesamiento básico de los datos para asegurar su calidad y consistencia. Este proceso se dividió en tres pasos principales:

### 1. Gestión de Valores Nulos

Se identificó la cantidad de valores nulos por cada columna.

-   La característica `label` era la única con una cantidad considerable de valores ausentes (aproximadamente un 8%). Para no perder estos registros, se decidió imputar estos valores asignándoles la categoría **`sem_label`**.
-   Para el resto de las columnas (`premise`, `categoria_pdv`, `zipcode` y `subcategoria`), que contenían un porcentaje muy bajo de nulos (menos del 1%), se optó por eliminar las filas correspondientes.

A continuación, se muestra el porcentaje de valores nulos por columna antes de la limpieza:

| pdv | produto | distributor_id | transaction_date | reference_date | quantity | gross_value | net_value | gross_profit | discount | taxes | categoria | descricao | tipos | label | subcategoria | marca | fabricante | premise | categoria_pdv | zipcode |
|:---:|:-------:|:--------------:|:----------------:|:--------------:|:--------:|:-----------:|:---------:|:------------:|:--------:|:-----:|:---------:|:---------:|:-----:|:-----:|:------------:|:-----:|:----------:|:-------:|:-------------:|:-------:|
| 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | **8.03%** | **0.16%** | 0.0 | 0.0 | **0.69%** | **0.69%** | **0.69%** |

---

### 2. Normalización de Variables Categóricas

Para evitar inconsistencias y duplicidad en las categorías, se aplicaron las siguientes transformaciones a las columnas de tipo texto:

-   **Conversión a mayúsculas:** Todas las cadenas de texto se convirtieron a mayúsculas.
-   **Eliminación de espacios:** Se eliminaron los espacios en blanco al inicio y al final de cada texto.

Esto asegura que categorías idénticas pero con diferente formato (p. ej., `Specialty` y `specialty`) sean tratadas como una sola, unificándolas como `SPECIALTY`.

---

### 3. Verificación del Esquema de Datos

Finalmente, se revisó que el tipo de dato de cada columna fuera coherente con los valores que contenía. Por ejemplo, se verificó que las columnas de fechas tuvieran el formato de fecha adecuado y que las columnas numéricas no contuvieran caracteres extraños.

## 📈 Análisis de Ventas Semanales

Para entender la estacionalidad y el comportamiento de las ventas, se realizó un análisis de la cantidad total de productos vendidos por cada semana del año 2022.

### Comportamiento a lo Largo del Año

Al visualizar las ventas semanales, se observa un patrón mayormente estable durante todo el año, con una excepción notable: un **pico de ventas extremadamente alto** entre las semanas 30 y 40.

![Gráfico de ventas totales por semana en 2022](https://raw.githubusercontent.com/spereze27/Desafio-Tecnico-Hackathon-Forecast-Big-Data-2025/main/Captura%20desde%202025-09-21%2022-10-00.png)

Una investigación más profunda reveló que este comportamiento anómalo se concentraba específicamente en la **semana 36**.

---

### Investigación de la Anomalía en la Semana 36

Para determinar la causa del pico, se analizó si el aumento en las ventas se debía a un producto o a un punto de venta (PDV) específico. Se agruparon las ventas de esa semana por PDV para identificar a los principales contribuyentes.

**Top 5 Puntos de Venta (PDV) por Ventas en la Semana 36**

| pdv                 | categoria_pdv  | sum(quantity)      |
| ------------------- | -------------- | ------------------ |
| `6491855528940268514` | `PACKAGE/LIQUOR` | 176,202.57         |
| `3025867614395044464` | `PACKAGE/LIQUOR` | 170,252.53         |
| `8723723113467008071` | `PACKAGE/LIQUOR` | 132,026.31         |
| `4304226119364518876` | `PACKAGE/LIQUOR` | 130,715.99         |
| `9171644843739559005` | `PACKAGE/LIQUOR` | 126,486.75         |

El análisis demostró que el aumento **no se debía a un único producto o punto de venta**, sino que fue un comportamiento generalizado durante toda esa semana.
Dado que el comportamiento de la semana 36 es un **valor atípico (outlier)** que no representa la tendencia general de ventas, se tomó la decisión de **excluir todos los datos correspondientes a esa semana**. Esta medida se implementó para evitar que esta anomalía introdujera ruido y afectara negativamente el rendimiento del modelo de pronóstico.

## 📊 Visualización de Ventas Post-Limpieza

Tras excluir la semana 36, el comportamiento de las ventas a lo largo del año se puede apreciar con mayor claridad. La nueva gráfica muestra una tendencia mucho más coherente y representativa de la estacionalidad del negocio.

![Gráfico de ventas totales por semana en 2022 sin la semana 36](https://raw.githubusercontent.com/spereze27/Desafio-Tecnico-Hackathon-Forecast-Big-Data-2025/main/Captura%20desde%202025-09-21%2022-21-49.png)

### Observaciones Clave

Al eliminar el valor atípico, se pueden identificar patrones claros en los datos:

1.  **Tendencia Creciente:** Se observa una tendencia general al alza en las ventas a medida que avanza el año.
2.  **Picos de Fin de Año:** Las ventas alcanzan su punto máximo durante el último trimestre del año (semanas 45-52), lo cual es consistente con el aumento de la demanda durante las temporadas festivas.
3.  **Estacionalidad Visible:** La gráfica ahora revela fluctuaciones y picos estacionales que antes eran opacados por la anomalía, proporcionando una base mucho más fiable para el pronóstico.

Con un conjunto de datos limpio y representativo, podemos proceder con la construcción de un modelo de forecasting más preciso y robusto.

## 🔬 Análisis por Características

Una vez limpios los datos, se realizó un análisis exploratorio segmentando las ventas por diferentes características para entender mejor los factores que influyen en la demanda.

### Ventas por Tipo de Producto (Label)

Al analizar las ventas semanales agrupadas por el `label` del producto, se observa un claro dominador.

-   **Productos `CORE`:** Esta categoría representa la gran mayoría de las ventas y mantiene su liderazgo de manera consistente a lo largo de todo el año.
-   **Otras categorías:** Las demás etiquetas como `SEM_LABEL`, `DISCONTINUED`, `ALLOCATED` y `INGOUT` tienen un volumen de ventas significativamente menor.

![Ventas semanales por los 5 tipos de producto principales](https://raw.githubusercontent.com/spereze27/Desafio-Tecnico-Hackathon-Forecast-Big-Data-2025/main/producto%20mas%20vendido.png)

---

### Ventas por Categoría de Producto

El análisis de las categorías de producto revela una concentración de las ventas en un solo segmento.

-   **Categoría `PACKAGE`:** Es, por un amplio margen, la categoría con mayor cantidad de unidades vendidas, superando con creces a las demás.
-   **Otras categorías relevantes:** `DISTILLED SPIRITS` y `NON-ALCOHOL` le siguen en importancia, aunque con un volumen mucho menor.

![Top 10 categorías de producto por cantidad vendida](https://raw.githubusercontent.com/spereze27/Desafio-Tecnico-Hackathon-Forecast-Big-Data-2025/main/categoria%20mas%20vendida.png)

---

### Relación entre Descuento y Cantidad Vendida

Finalmente, se exploró la relación entre el descuento aplicado y la cantidad vendida para identificar patrones de compra. Durante este análisis, se hizo un descubrimiento importante.

-   **Detección de Valores Negativos:** El gráfico de dispersión mostró que existían registros con una **cantidad vendida negativa**. Estos valores atípicos probablemente corresponden a **devoluciones, reembolsos o ajustes de inventario**.

![Gráfico de dispersión de descuento vs cantidad vendida](https://raw.githubusercontent.com/spereze27/Desafio-Tecnico-Hackathon-Forecast-Big-Data-2025/main/dispersion%20con%20reembolsos.png)


El objetivo de este proyecto es construir un modelo para **predecir la demanda futura (ventas)**, no para pronosticar devoluciones. Por lo tanto, se tomó la decisión de **eliminar todos los registros con cantidades negativas**. Esto evita introducir ruido en el modelo y le permite generalizar mejor los patrones de compra reales.

Una vez eliminados los productos reembolsados se tiene la siguiente dispersión en donde se  muestra que la mayoria de clientes compra una cantidad reducida de productos con un descuento moderado pero que a medida que se aumenta el descuento se tienen compras en grandes cantidades de un producto.

![Gráfico de dispersión de descuento vs cantidad vendida](https://github.com/spereze27/Desafio-Tecnico-Hackathon-Forecast-Big-Data-2025/blob/main/Captura%20desde%202025-09-21%2023-27-26.png)

## 📦 Distribución de Ventas por Día de la Semana

Para completar el análisis exploratorio, se examinó cómo se distribuyen las ventas a lo largo de los días de la semana. Esta visualización nos permite identificar qué días son comercialmente más fuertes.

![Distribución de Ventas por Día de la Semana](https://raw.githubusercontent.com/spereze27/Desafio-Tecnico-Hackathon-Forecast-Big-Data-2025/main/Captura%20desde%202025-09-21%2023-23-20.png)

### Interpretación del Gráfico

El diagrama de cajas y bigotes revela un patrón claro en el comportamiento de compra semanal:

-   **Días de Menor Actividad:** Se observa que los días en medio de la semana, específicamente **miércoles, jueves y viernes**, presentan una mediana de ventas inferior en comparación con el resto de los días. La caja, que representa el 50% central de los datos, también se encuentra en un rango más bajo.
-   **Días de Mayor Actividad:** Por el contrario, el inicio de la semana (**lunes y martes**) y el fin de semana (**sábado y domingo**) muestran una distribución de ventas más alta y con mayor dispersión, indicando un volumen de transacciones superior.

Esta información es valiosa para el modelo, ya que confirma que el **día de la semana es una característica importante** que influye directamente en la cantidad de productos vendidos.