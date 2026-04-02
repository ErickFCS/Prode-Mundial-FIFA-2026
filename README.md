# Prode Mundial FIFA 2026 - API Backend

Este proyecto consiste en el desarrollo de una **API REST** utilizando **Python** y **Flask** para gestionar el fixture y un sistema de pronósticos deportivos (ProDe) con motivo del Mundial.

## Estado del Proyecto

El proyecto se encuentra en fase de desarrollo.

## Enlaces Útiles

- **Swagger Editor**: Herramienta recomendada para visualizar el contrato `swagger.yaml` adjunto en la consigna.

## ¿Por qué este proyecto?

La iniciativa busca fomentar el compañerismo y la interacción mediante un sistema de pronósticos con un carácter solidario, ya que para participar se requiere la donación de un alimento no perecedero.

## Proceso de Uso

1. **Gestión del Fixture:** Se registran los encuentros indicando equipos, estadio, ciudad, fecha y fase del torneo.
2. **Predicciones:** Los usuarios registrados realizan sus pronósticos sobre los partidos que aún no se han jugado.
3. **Actualización de Resultados:** Una vez finalizados los encuentros, se cargan los marcadores oficiales.
4. **Cálculo de Ranking:** El sistema asigna 3 puntos por acierto exacto y 1 punto por adivinar el ganador o empate con marcador distinto.

## Instalación

Es necesario contar con **Python** y **Docker** instalados en el sistema.

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repo>
   cd <nombre-del-repo>
   ```

2. **Configurar el entorno:**
   Ejecuta el script de automatización para crear el entorno virtual e instalar las dependencias necesarias:
   ```bash
   ./prepararEntorno.sh
   ```

3. **Variables de Entorno:**
   Crea un archivo `.env` basado en el archivo de plantilla provisto (`template.env`) y configura las credenciales de tu base de datos.

4. **Levantar la Base de Datos:**
   Utiliza Docker para iniciar el servicio de MySQL:
   ```bash
   docker compose up -d
   ```

## Documentación de Uso

Para iniciar el servidor, primero activa el entorno virtual y luego ejecuta el punto de entrada de la aplicación:

```bash
. .venv/bin/activate
python ./backend/app.py
```

### Ejemplos de Endpoints:

- **Listar partidos (con filtros y paginación):**
  ```bash
  curl "http://localhost:5000/partidos?fecha=2026-06-15&limit=10&offset=0"
  ```
- **Registrar un nuevo usuario:**
  ```bash
  curl -X POST http://localhost:5000/usuarios -d '{"nombre": "fiuba", "email": "fiuba@ejemplo.com"}'
  ```
- **Consultar el ranking actual:**
  ```bash
  curl http://localhost:5000/ranking
  ```

## Licencia

Este proyecto está bajo la Licencia **BSD 3-Clause**. Consulta el archivo `LICENSE.md` para más información.
