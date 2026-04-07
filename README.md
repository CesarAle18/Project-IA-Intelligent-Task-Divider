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

**🎯 Objetivo:** Enriquecer la calidad de los datos para mejorar la capacidad predictiva del modelo.

### 🔧 Tareas

- 📊 **Ampliar dataset**
  - Crear mínimo 50–100 registros sintéticos o reales
  - Incluir variedad en:
    - Tamaños (Story Points)
    - Experiencia
    - Rendimiento

- 🧠 **Agregar nuevas features clave**
  - ⏳ **Complejidad técnica (1–5)** → lógica, algoritmos, integraciones
  - 🔗 **Número de dependencias** → cuántas tareas externas afectan esta
  - 👥 **Cantidad de desarrolladores asignados**
  - 🧩 **Tipo de tarea** (Backend, Frontend, DevOps, QA)
  - 📅 **Urgencia/prioridad** (Baja, Media, Alta)

- 🔄 **Preprocesamiento de datos**
  - Normalización de variables numéricas
  - Codificación de variables categóricas (One-Hot Encoding o Label Encoding)

- 📈 **Análisis exploratorio (EDA)**
  - Correlación entre variables
  - Identificar patrones:
    - ¿Mayor tamaño → más subtareas?
    - ¿Más experiencia → menos tiempo?

---

## 🗓️ Semana 2: Implementación de nuevos modelos

**🎯 Objetivo:** Mejorar la precisión comparando múltiples modelos de Machine Learning.

### 🤖 Modelos a implementar

#### 🔢 Para regresión (y_tasks, y_time)
- 📉 Regresión Lineal (baseline)
- 🌲 Random Forest Regressor
- ⚡ Gradient Boosting Regressor
- 🔍 Support Vector Regressor (SVR)

#### 🧠 Para clasificación (y_risk)
- 📊 Logistic Regression (baseline)
- 🌲 Random Forest Classifier
- ⚡ Gradient Boosting Classifier
- 🧩 K-Nearest Neighbors (KNN)

---

### 🔧 Tareas

- 🧪 Entrenar cada modelo con el dataset mejorado
- ⚖️ Evaluar desempeño:
  - Regresión:
    - MAE (Error absoluto medio)
    - RMSE
  - Clasificación:
    - Accuracy
    - Precision / Recall
    - Matriz de confusión

- 📊 Comparar resultados entre modelos
- 🏆 Seleccionar los mejores modelos para cada variable objetivo

---

## 🗓️ Semana 3: Optimización y simulación del sistema inteligente

**🎯 Objetivo:** Afinar el modelo y simular su uso en escenarios reales.

### 🔧 Tareas

- ⚙️ **Optimización de hiperparámetros**
  - GridSearch o RandomSearch
  - Ajustar:
    - Número de árboles (Random Forest)
    - Profundidad
    - Learning rate

- 🧪 **Validación cruzada (Cross-validation)**
  - Asegurar que el modelo generaliza bien

- 🧠 **Simulación del sistema**
  - Crear inputs nuevos (historias de usuario ficticias)
  - Obtener predicciones:
    - Número de subtareas
    - Tiempo estimado
    - Riesgo

- 🖥️ **Prototipo simple (opcional pero recomendado)**
  - Interfaz básica:
    - Formulario de entrada
    - Mostrar predicciones
  - Puede ser en:
    - HTML + JS
    - o consola Python

- 📦 **Documentación del modelo**
  - Cómo funciona
  - Qué variables usa
  - Qué modelo se eligió y por qué

---

# 📌 Resultado esperado al final de las 3 semanas

✔️ Modelo más preciso y robusto  
✔️ Dataset más completo y representativo  
✔️ Comparación clara entre múltiples algoritmos  
✔️ Sistema capaz de:

- Dividir tareas automáticamente 🧩  
- Estimar tiempos ⏱️  
- Predecir riesgos 🚨  
