CREATE DATABASE IF NOT EXISTS prode;
USE prode;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contrasena VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS partidos (
    id_partido INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    equipo_local VARCHAR(50) NOT NULL,
    equipo_visitante VARCHAR(50) NOT NULL,
    ciudad VARCHAR(50),
    fecha DATETIME,
    estadio VARCHAR(50),
    fase VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS equipos (
    id_equipo INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    pais VARCHAR(20) NOT NULL,
    grupo VARCHAR(10) NOT NULL
);

CREATE DATABASE IF NOT EXISTS predicciones_db;
USE predicciones_db;

CREATE TABLE predicciones (
    id_prediccion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_partido INT NOT NULL,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    fecha_prediccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_prediccion (id_usuario, id_partido)
);

INSERT INTO predicciones (id_usuario, id_partido, goles_local, goles_visitante) VALUES
(1, 1, 2, 1),
(1, 2, 1, 0),
(2, 1, 1, 1);
