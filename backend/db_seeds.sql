

INSERT INTO usuarios (nombre,       email,           contrasena) VALUES
                     ('Ana Pérez',  'ana@mail.com',  '1234'),
                     ('Juan López', 'juan@mail.com', '1234');
                    
INSERT INTO predicciones (id_usuario, id_partido, goles_local, goles_visitante) VALUES
                         (1,          1,          2,           1),
                         (1,          2,          1,           0),
                         (2,          1,          1,           1);

INSERT INTO partidos (equipo_local, equipo_visitante, fecha,                 fase) VALUES
                     ('Argentina',  'Brasil',         '2026-06-15 18:00:00', 'Grupo A'),
                     ('Alemania',   'Francia',        '2026-06-16 15:00:00', 'Grupo B');
