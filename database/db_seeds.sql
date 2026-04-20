
INSERT INTO usuarios (nombre, email, puntos) VALUES
('Ana Pérez', 'ana@mail.com', 15),
('Juan López', 'juan@mail.com', 10),
('Carlos Gómez', 'carlos@mail.com', 0),
('Lucía Fernández', 'lucia@mail.com', 25),
('Martín Sosa', 'martin@mail.com', 5),
('Elena Ruiz', 'elena@mail.com', 12),
('Roberto Díaz', 'roberto@mail.com', 8),
('Sofía Torres', 'sofia@mail.com', 20),
('Diego Martínez', 'diego@mail.com', 3),
('Laura Castro', 'laura@mail.com', 18);

INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase) VALUES
('Argentina', 'Brasil', '2026-06-15 18:00:00', 'grupos'),
('Alemania', 'Francia', '2026-06-16 15:00:00', 'grupos'),
('España', 'Italia', '2026-06-16 21:00:00', 'grupos'),
('Uruguay', 'Portugal', '2026-06-17 14:00:00', 'grupos'),
('Inglaterra', 'Bélgica', '2026-06-17 17:00:00', 'grupos'),
('Países Bajos', 'Croacia', '2026-06-18 12:00:00', 'grupos'),
('México', 'USA', '2026-06-18 20:00:00', 'grupos'),
('Japón', 'Senegal', '2026-06-19 10:00:00', 'grupos'),
('Colombia', 'Chile', '2026-06-19 16:00:00', 'grupos'),
('Marruecos', 'Suiza', '2026-06-20 13:00:00', 'grupos');

INSERT INTO predicciones (id_usuario, id_partido, goles_equipo_local, goles_equipo_visitante) VALUES
(1, 1, 2, 1), (1, 2, 1, 0), (1, 3, 2, 2), (1, 4, 0, 1), (1, 5, 3, 1),
(2, 1, 1, 1), (2, 2, 2, 1), (2, 3, 0, 0), (2, 4, 1, 2), (2, 5, 1, 1),
(3, 1, 0, 2), (3, 2, 0, 0), (3, 3, 1, 3), (3, 4, 2, 1), (3, 5, 0, 2),
(4, 1, 3, 0), (4, 2, 2, 2), (4, 3, 1, 0), (4, 4, 0, 0), (4, 5, 2, 1),
(5, 1, 1, 2), (5, 2, 1, 1), (5, 3, 2, 0), (5, 4, 3, 2), (5, 5, 1, 0),
(6, 6, 2, 1), (6, 7, 1, 1), (6, 8, 0, 2), (6, 9, 2, 2), (6, 10, 1, 0),
(7, 6, 0, 0), (7, 7, 2, 3), (7, 8, 1, 0), (7, 9, 0, 1), (7, 10, 2, 2),
(8, 6, 1, 2), (8, 7, 0, 0), (8, 8, 3, 1), (8, 9, 1, 1), (8, 10, 0, 3),
(9, 6, 4, 1), (9, 7, 1, 2), (9, 8, 2, 2), (9, 9, 3, 0), (9, 10, 1, 1),
(10, 1, 2, 0), (10, 2, 0, 1), (10, 6, 1, 1), (10, 7, 2, 1), (10, 8, 0, 0);
