CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contrasena VARCHAR(100) NOT NULL
);

CREATE TABLE partidos (
    id_partido INT AUTO_INCREMENT NOT NULL,
    equipo_local VARCHAR(50) NOT NULL,
    equipo_visitante VARCHAR(50) NOT NULL,
    ciudad VARCHAR(50),
    fecha DATETIME,
    estadio VARCHAR(50),
    fase VARCHAR(10)
);

CREATE TABLE equipos (
    id_equipo INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    pais VARCHAR(20) NOT NULL,
    grupo VARCHAR(10) NOT NULL
);