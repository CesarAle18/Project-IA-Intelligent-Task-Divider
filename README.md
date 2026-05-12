# 🤖 Project-IA-Intelligent-Task-Divider

# 1. 🧩 Problema a resolver

En las empresas de desarrollo de software, especialmente aquellas que trabajan con metodologías ágiles como Scrum, es común que los proyectos se planifiquen mediante historias de usuario o requerimientos generales. En la práctica surgen varios problemas:

- ❗ Las tareas son demasiado amplias o ambiguas.
- ⏱️ Existe una mala estimación del tiempo y esfuerzo.
- 🔗 Se generan cuellos de botella por dependencias no identificadas.
- 🧠 El líder técnico o Scrum Master debe invertir tiempo considerable dividiendo tareas manualmente.
- 📉 La productividad se ve afectada por una descomposición ineficiente del trabajo.

## 🎯 ¿Qué quieres predecir?

El modelo propuesto permitiría predecir y recomendar la división de tareas, estimaciones de tiempo y riesgos de retrasos en proyectos, para poder optimizar la planificación.

## 🤖 ¿Por qué un modelo de IA podría ayudar a resolver ese problema?

El modelo de IA ayudaría a optimizar la división de tareas analizando la complejidad del código, habilidades de los desarrolladores y dependencias, mientras estima tiempos basados en datos históricos y predice retrasos por métricas como rendimiento del equipo.

# 2. 📊 Definición de las features

## 🔍 ¿Qué representa cada característica?
- **Tamaño del software:** Es la magnitud o volumen de la tarea o funcionalidad a desarrollar (Story Points)
- **Experiencia del equipo:** Nivel promedio de experiencia del equipo o desarrollador asignado - Nivel (Junior, Mid, Senior)
- **Rendimiento histórico:** Métricas pasadas del equipo o desarrollador - Velocidad, Porcentaje de tareas entregadas a tiempo, Tiempo promedio real vs estimado

## 💡 ¿Por qué crees que esa información ayudaría al modelo a tomar una decisión?
- **Tamaño del software:** proporciona una estimación del esfuerzo base necesario para completar una tarea, lo que permite al modelo identificar cuándo una tarea puede ser demasiado grande y requerir más tiempo o división.
- **Experiencia del equipo:** aporta contexto sobre la capacidad de ejecución, ya que equipos con mayor experiencia pueden resolver tareas más rápidamente y con menor probabilidad de errores, lo que influye directamente en la estimación del tiempo y el riesgo.
- **Rendimiento histórico:** permite al modelo aprender de datos pasados, identificando patrones de cumplimiento, retrasos y desviaciones entre lo estimado y lo real. Esto mejora la precisión de las predicciones y permite anticipar posibles problemas.

## 3. 🧪 Creación de un dataset de ejemplo

A continuación se presenta un pequeño dataset de prueba utilizando las tres características definidas: **Software Size** (Story Points), **Team Experience** (nivel del desarrollador) y **Performance** (velocidad histórica del equipo).

| Software Size (Story Points) | Team Experience (1=Junior, 2=Mid, 3=Senior) | Performance (0.0 a 1.0)   |
|------------------------------|---------------------------------------------|---------------------------|
| 8                            | 1                                           | 0.55                      |
| 13                           | 2                                           | 0.70                      |
| 5                            | 3                                           | 0.90                      |
| 21                           | 2                                           | 0.60                      |
| 3                            | 1                                           | 0.50                      |

### 📌 ¿Qué representa cada fila (entrada)?

Cada fila representa **una tarea de software que ya fue desarrollada en el pasado**. El modelo lee cada fila para aprender la relación entre las condiciones iniciales y el resultado final. Básicamente, le estás diciendo al modelo:  
*"Con estos datos de entrada (tamaño, experiencia del equipo, rendimiento), así es como se comportó esta tarea en el pasado. Aprende de eso para que puedas predecir o recomendar cómo dividir, estimar o anticipar riesgos en tareas nuevas."*

### 📊 ¿Qué representa cada columna?

- **Software Size (Story Points):**  
  La complejidad de la tarea en Story Points. Define qué tan "pesado" es el trabajo.

- **Team Experience:**  
  El nivel del desarrollador asignado (1 = Junior, 2 = Mid, 3 = Senior). Es el factor que compensa la complejidad.

- **Performance:**  
  Un valor de 0.0 a 1.0. Representa la velocidad real o fiabilidad histórica del equipo (su "ritmo").

## 4. 🎯 Variable objetivo (label)

A continuación se define la variable que el modelo intentará predecir. Dado que el problema busca optimizar la planificación desde tres dimensiones (división, tiempo y riesgo), se proponen tres posibles variables objetivo.

### 📌 Variables objetivo propuestas

| Nombre      | Tipo                              | Descripción                                                                | Posibles valores               |
|-------------|-----------------------------------|----------------------------------------------------------------------------|--------------------------------|
| **y_tasks** | Numérico (entero)                 | Número de sub-tareas en las que se dividió el requerimiento original       | 1, 2, 3, ... (ejemplo: 1 a 10) |
| **y_time**  | Numérico (decimal)                | Duración real desde que se empezó la tarea hasta que se terminó (en días)  | 0.5, 1.0, 2.5, 5.0, ...        |
| **y_risk**  | Categórico (numérico codificado)  | Nivel de riesgo de retraso experimentado en el pasado                      | 0 = Bajo, 1 = Medio, 2 = Alto  |

### 🧠 ¿Qué representa el resultado?

Representa la **"Verdad Histórica"**. Es el dato real de lo que sucedió en proyectos pasados. Al aprender de esta información, el modelo podrá asociar las características de entrada (tamaño, experiencia, rendimiento) con los resultados observados y así generar predicciones para nuevas tareas.

### 🔢 ¿Qué significan sus valores?

- **y_tasks (Número de sub-tareas):**  
  Representa en cuántas piezas atómicas se dividió el requerimiento original para ser desarrollado.  
  *Ejemplo:* Una historia de 8 puntos puede haberse dividido en 4 tareas más pequeñas.

- **y_time (Tiempo en días):**  
  Representa la duración real desde que se empezó la tarea hasta que se terminó.  
  *Ejemplo:* 3.5 días calendario o hábiles, según la métrica del equipo.

- **y_risk (Nivel de riesgo):**  
  Aquí es donde los números actúan como categorías para clasificar el riesgo de retraso:  
  - 🟢 **0 = Bajo:** La tarea se completó antes o dentro del tiempo estimado sin incidentes críticos.  
  - 🟡 **1 = Medio:** Hubo retrasos moderados (20-50% más del tiempo estimado) o dependencias problemáticas.  
  - 🔴 **2 = Alto:** Retraso significativo (>50% del tiempo estimado), bloqueos o necesidad de re-planificación urgente.

## 5. ⚙️ Entrenamiento del modelo

Incluye el código necesario para:

- 📦 importar las librerías
- ✂️ dividir los datos en entrenamiento y prueba
- 🧠 entrenar el modelo

Explica brevemente qué ocurre en cada uno de estos pasos.

- **train_test_split:** Divide el 80% de los datos para Entrenamiento (train) y el 20% para Pruebas (test). Esto evita que el modelo simplemente memorice los datos; queremos que aprenda patrones reales.

- **LinearRegression:** Es el cerebro matemático para predecir números. Se usa para las tareas y el tiempo porque estos valores pueden subir o bajar en una escala infinita. Busca una línea que conecte los puntos de la mejor manera.

- **LogisticRegression:** Es el cerebro para clasificar. Aunque se llame "regresión", su trabajo aquí es decidir si un proyecto cae en la caja de riesgo "Alto", "Medio" o "Bajo".

- **max_iter=1000:** Le da al modelo de riesgo 1000 "oportunidades" de ajustar sus cálculos internos hasta encontrar la solución más precisa.

# 🚀 Plan de trabajo (3 semanas)

## 🗓️ Semana 1: Expansión de features y mejora del dataset

**Objetivo:** Enriquecer la calidad de los datos para mejorar la capacidad predictiva del modelo.

### 🔧 Tareas

- **Ampliar dataset**
  - Crear mínimo 50–100 registros sintéticos o reales
  - Incluir variedad en:
    - Tamaños (Story Points)
    - Experiencia
    - Rendimiento

- **Agregar nuevas features clave**
  - **Complejidad técnica (1–5)** → lógica, algoritmos, integraciones
  - **Número de dependencias** → cuántas tareas externas afectan esta
  - **Cantidad de desarrolladores asignados**
  - **Tipo de tarea** (Backend, Frontend, DevOps, QA)
  - **Urgencia/prioridad** (Baja, Media, Alta)

- **Preprocesamiento de datos**
  - Normalización de variables numéricas
  - Codificación de variables categóricas (One-Hot Encoding o Label Encoding)

- **Análisis exploratorio (EDA)**
  - Correlación entre variables
  - Identificar patrones:
    - ¿Mayor tamaño → más subtareas?
    - ¿Más experiencia → menos tiempo?

---

🗓️ Semana 2: Integración de datos y automatización básica (Google Colab)
🎯 Objetivo: Hacer que el modelo deje de depender de datos hardcodeados y pueda trabajar con datasets externos (CSV).

🔧 Tareas

Lectura de dataset desde CSV (clave)

- Subir archivo a Google Colab (files.upload() o Google Drive)
  - Leer dataset con pandas.read_csv()
  - Validar estructura:
  - Columnas correctas
  - Tipos de datos (numéricos vs categóricos)
  - Limpieza básica

- Manejo de valores nulos
  - Eliminación de duplicados
  - Validación de rangos (ej: rendimiento entre 0–1)
  - Adaptar pipeline actual

- Reemplazar raw_data por lectura desde CSV
  - Mantener:
  - Encoding (Label + OneHot)
  - Escalado (StandardScaler)
  - Asegurar que todo funcione igual pero con datos externos

- Persistencia simple (opcional pero recomendado)

- Guardar dataset limpio como nuevo CSV
- Versionar datasets (ej: dataset_v2.csv)
  - Prueba rápida

- Ejecutar entrenamiento completo desde CSV
- Validar que métricas sigan siendo coherentes

---

### 🗓️ Semana 3: Optimización y simulación del sistema inteligente

## Calidad de datos

- Detectar y tratar outliers con IQR en columnas `SP`, `Complejidad` y `Dependencias`
- Agregar validación de tipos de datos por columna antes de la limpieza

---

## Logs y Pipeline

- Guardar reporte completo de limpieza (filas eliminadas por criterio) en archivo de log
- Construir pipeline unificado de sklearn (`Pipeline`) que encadene preprocesamiento + escalado + modelo

---

##  Nuevos modelos

- Probar modelos Random Forest y Gradient Boosting (XGBoost/LightGBM) para las tres variables objetivo
- Comparar resultados contra la regresión lineal/logística actual

---

## Validación y métricas

- Implementar validación cruzada k-fold en lugar del único split 80/20
- Agregar métricas adicionales: RMSE y MAPE para regresión; matriz de confusión, F1, precisión y recall para clasificación
- Exportar reporte de métricas en CSV al Drive para historial de experimentos

---

## Persistencia del modelo

- Serializar y guardar los tres modelos entrenados con `joblib` en Google Drive
- Agregar celda de carga de modelos ya entrenados como alternativa al entrenamiento completo

---

## Bug fix y predicción mejorada

- Corregir bug: variable `Rendimiento_Equipo` no definida en sección 8 (debe ser `Rendimiento`)
- Mostrar probabilidad por clase del riesgo usando `predict_proba` en lugar de solo la etiqueta ganadora
- Validar datos de entrada del usuario antes de predecir, con mensajes de error descriptivos

---

## Estructura y mantenibilidad

- Modularizar el código en funciones reutilizables: `cargar_datos()`, `preprocesar()`, `entrenar()`, `predecir()`
- Agregar bloque de configuración centralizada al inicio del notebook (rutas, hiperparámetros, columnas

---

# 📌 Resultado esperado al final de las 3 semanas

✔️ Modelo más preciso y robusto  
✔️ Dataset más completo y representativo  
✔️ Comparación clara entre múltiples algoritmos  
✔️ Sistema capaz de:

- Dividir tareas automáticamente 🧩  
- Estimar tiempos ⏱️  
- Predecir riesgos 🚨

---

# Plan de Trabajo UI + API

Stack definido
Next.js + Tailwind CSS → FastAPI → MySQL + .pkl cargado en memoria

# Semana 1 — Backend + Integración del Modelo

## Objetivo
Tener la API 100% funcional antes de tocar el frontend.

---

## Configuración del entorno y estructura del proyecto
Crear la estructura de carpetas del proyecto (`/backend`, `/frontend`), configurar el entorno virtual de Python, instalar dependencias de FastAPI (`fastapi`, `uvicorn`, `sqlalchemy`, `pymysql`, `joblib`, `scikit-learn`, `pandas`), y verificar que los tres archivos `.pkl` cargan correctamente en memoria al iniciar el servidor.

---

## Diseño e implementación de la base de datos MySQL
Crear la base de datos local, diseñar y crear dos tablas:

- `predicciones`
  - Almacena el historial de predicciones:
    - Inputs del usuario
    - Outputs del modelo
    - Timestamp

- `metricas_modelo`
  - Almacena:
    - MAE
    - RMSE
    - R²
    - F1
    - Ganadores
    - Timestamp

Configurar SQLAlchemy con los modelos ORM correspondientes y probar la conexión con la base de datos.

---

## Endpoints de predicción e historial

### POST `/predecir`
- Recibe los 7 parámetros del formulario.
- Ejecuta los tres pipelines del modelo.
- Guarda el resultado en MySQL.

### GET `/historial`
- Devuelve el historial de predicciones.
- Implementar paginación básica.

### GET `/historial/{id}`
- Devuelve el detalle completo de una predicción específica.

---

## Endpoints de métricas y configuración

### GET `/metricas`
- Devuelve el historial de métricas del modelo.
- Los datos pueden leerse desde:
  - `metricas_historial.csv`
  - o desde la tabla MySQL.

### GET `/config`
- Devuelve la configuración actual del sistema.

### PUT `/config`
- Permite editar los parámetros del `CONFIG dict`:
  - Rangos
  - Columnas
  - Hiperparámetros

La configuración debe serializarse en un archivo JSON en disco.

---

## Pruebas del backend y documentación Swagger
- Probar todos los endpoints desde la UI automática de FastAPI (`/docs`).
- Validar los schemas de entrada y salida con Pydantic.
- Asegurar el manejo de errores:
  - Entradas inválidas
  - Modelo no cargado
- Dejar el backend completamente listo para ser consumido por el frontend.

---

# Semana 2 — Frontend Next.js + Integración completa

## Objetivo
Construir la interfaz, conectarla al backend y dejarlo todo funcionando localmente.

---

## Setup del proyecto Next.js y estructura de páginas
Inicializar el proyecto con `create-next-app`, configurar Tailwind CSS, instalar `axios` o utilizar `fetch` para las llamadas a la API, y definir el layout base con una barra de navegación lateral que contenga las siguientes secciones:

- Predicción
- Dashboard
- Historial
- Configuración

---

## Formulario de predicción
Construir el formulario con los 7 campos necesarios utilizando:

- Sliders
- Selects
- Inputs numéricos

Conectar el formulario al endpoint:

### POST `/predecir`

Mostrar los resultados en tarjetas visuales incluyendo:

- Sub-tareas con intervalo de confianza
- Tiempo estimado con intervalo de confianza
- Nivel de riesgo con barra de probabilidades por clase

---

## Dashboard de métricas y gráficas
Construir la vista de métricas utilizando una librería de gráficas como:

- Recharts

Visualizar las siguientes métricas:

- Evolución temporal de MAE y R² de regresión
- Evolución de F1 y Accuracy de clasificación
- Comparativa de modelos ganadores a lo largo del tiempo

Conectar la vista al endpoint:

### GET `/metricas`

---

## Historial de predicciones
Construir una tabla paginada con todas las predicciones almacenadas en MySQL.

La tabla debe incluir:

- Inputs clave del usuario
- Outputs generados por los modelos

Agregar:

- Panel lateral
  o
- Modal de detalle

al hacer clic sobre una fila.

Conectar al endpoint:

### GET `/historial`

---

## Página de configuración del modelo
Construir un editor visual del objeto `CONFIG` con:

- Campos editables para rangos válidos
- Configuración de columnas de outliers
- Parámetros de K-Fold

Al guardar cambios:

### PUT `/config`

Mostrar una confirmación visual de actualización exitosa.

Incluir además una sección de solo lectura con:

- Modelos ganadores del último entrenamiento

---

## Integración final, pruebas end-to-end y ajustes
Probar el flujo completo de la aplicación:

1. Formulario
2. Predicción
3. Guardado en MySQL
4. Aparición en historial
5. Actualización de métricas

Realizar:

- Corrección de bugs de integración
- Ajustes responsive de estilos
- Optimización visual y funcional

Documentar cómo levantar el proyecto localmente mediante un archivo:

### `README.md`

Incluyendo:

- Comandos para ejecutar el backend
- Comandos para ejecutar el frontend
- Variables de entorno necesarias
- Pasos de instalación y ejecución
