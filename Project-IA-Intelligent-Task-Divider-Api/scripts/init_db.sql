CREATE DATABASE IF NOT EXISTS task_divider_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE task_divider_db;

CREATE TABLE IF NOT EXISTS predicciones (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    -- Inputs
    sp              FLOAT NOT NULL,
    experiencia     INT NOT NULL,
    rendimiento     FLOAT NOT NULL,
    complejidad     FLOAT NOT NULL,
    dependencias    FLOAT NOT NULL,
    tipo_tarea      VARCHAR(20) NOT NULL,
    urgencia        VARCHAR(10) NOT NULL,
    -- Outputs
    pred_tasks      INT NOT NULL,
    ci_tasks_lower  FLOAT,
    ci_tasks_upper  FLOAT,
    pred_time       INT NOT NULL,
    ci_time_lower   FLOAT,
    ci_time_upper   FLOAT,
    pred_risk       VARCHAR(10) NOT NULL,
    proba_alto      FLOAT,
    proba_medio     FLOAT,
    proba_bajo      FLOAT,
    -- Metadata
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_created_at (created_at),
    INDEX idx_tipo_tarea (tipo_tarea)
);

CREATE TABLE IF NOT EXISTS metricas_modelo (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    -- Ganadores
    ganador_tasks   VARCHAR(50) NOT NULL,
    ganador_time    VARCHAR(50) NOT NULL,
    ganador_risk    VARCHAR(50) NOT NULL,
    -- Regresión: sub-tareas
    tasks_mae       FLOAT,
    tasks_rmse      FLOAT,
    tasks_mape      FLOAT,
    tasks_r2        FLOAT,
    -- Regresión: tiempo
    time_mae        FLOAT,
    time_rmse       FLOAT,
    time_mape       FLOAT,
    time_r2         FLOAT,
    -- Clasificación: riesgo
    risk_accuracy   FLOAT,
    risk_f1         FLOAT,
    risk_precision  FLOAT,
    risk_recall     FLOAT,
    -- Metadata
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
