CREATE DATABASE IF NOT EXISTS prode;

USE prode;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    puntos INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS partidos (
    id INT AUTO_INCREMENT NOT NULL,
    equipo_local VARCHAR(50) NOT NULL,
    equipo_visitante VARCHAR(50) NOT NULL,
    fecha DATETIME NOT NULL,
    fase VARCHAR(10) NOT NULL,
    goles_equipo_local INT DEFAULT -1,
    goles_equipo_visitante INT DEFAULT -1
);

CREATE TABLE IF NOT EXISTS predicciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_partido INT NOT NULL,
    goles_equipo_local INT NOT NULL,
    goles_equipo_visitante INT NOT NULL,
    fecha_prediccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREING KEY id_usuario REFERENCES usuarios(id),
    FOREING KEY id_partido REFERENCES partidos(id)
);
