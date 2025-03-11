# README

## Descripción del Proyecto

Este proyecto tiene como objetivo crear un grafo de relaciones de artistas utilizando información obtenida a través de la API de Spotify. Se realiza un análisis de colaboraciones entre artistas hasta una cierta profundidad, y se genera un grafo dirigido que modela estas relaciones.

Las funcionalidades principales incluyen:
- Scraping de datos sobre artistas y colaboraciones desde la API de Spotify.
- Generación de nodos y aristas para representar a los artistas y sus colaboraciones en un grafo.
- Exportar los datos resultantes en un formato adecuado para análisis posterior.

### Contenido del Proyecto
- **src/data_collection**: Contiene las clases para interactuar con la API de Spotify y extraer datos relevantes.
- **src/utils/config.py**: Configuración para rutas y credenciales.
- **main.py**: Archivo de entrada al programa, que permite generar el grafo especificando parámetros como artista inicial, profundidad máxima y número máximo de artistas.

---

## Requisitos Previos

### Entorno Virtual
Es recomendable usar un entorno virtual para instalar las dependencias y aislarlas del sistema base. Sigue estos pasos para configurarlo:

1. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```

2. Activa el entorno virtual:
    - En Linux/Mac:
      ```bash
      source venv/bin/activate
      ```
    - En Windows:
      ```bash
      .\venv\Scripts\activate
      ```

3. Instala las dependencias necesarias definidas en `requirements.txt` (en caso de que este archivo exista o debas crearlo):
   ```bash
   pip install -r requirements.txt
   ```

Para salir del entorno virtual, simplemente ejecuta:
```bash
deactivate
```

---

### Variables de Entorno
Este proyecto requiere un archivo `.env` para utilizar las credenciales de la API de Spotify. El archivo `.env` debe ubicarse en la raíz del proyecto.

#### Creación del Archivo `.env`:
1. Crea un archivo llamado `.env` en la raíz del proyecto.
2. Añade las siguientes variables de entorno con tus claves de desarrollador obtenidas de Spotify Developer Portal:
   ```
   SPOTIFY_CLIENT_ID=tu_client_id
   SPOTIFY_CLIENT_SECRET=tu_client_secret
   ```

Reemplaza `tu_client_id` y `tu_client_secret` con los valores proporcionados al registrar tu aplicación.

---

### Uso del Proyecto

1. Asegúrate de que las variables de entorno están configuradas adecuadamente en el archivo `.env`.
2. Activa tu entorno virtual siguiendo los pasos indicados anteriormente.
3. Ejecuta el archivo principal del programa indicando los parámetros requeridos:
   ```bash
   python main.py
   ```
   El programa generará el grafo desde el artista raíz especificado, iterará hasta la profundidad y cantidad de artistas indicados, y exportará los datos generados.

### Parámetros de Entrada
La función principal del programa es `crear_grafo`, que acepta los siguientes parámetros:
- `max_artist` (int): Número máximo de artistas a procesar.
- `max_deep` (int): Profundidad máxima de las colaboraciones a analizar.
- `name_artist` (str): Nombre del artista inicial. Por defecto, usa "Melendi".

Puedes personalizar estos valores directamente en el archivo `main.py` antes de ejecutar el script.

---

## Dependencias

Asegúrate de tener las siguientes dependencias instaladas en tu entorno:

- **Python 3.12 o superior**
- **Paquetes necesarios**:
    - `spotipy`: Para interactuar con la API de Spotify.
    - `pandas`: Para manejar datos tabulares (opcional según el proceso de scraping).
    - Cualquier otro paquete mencionado en el proyecto (asegúrate de tenerlos en `requirements.txt`).

Instala los paquetes con:
```bash
pip install spotipy pandas
```

---

## Notas Adicionales

- El uso de la API de Spotify puede estar limitado a las credenciales que configures. Asegúrate de que tu aplicación de Spotify tenga los permisos necesarios para leer los datos requeridos.
- Este proyecto puede generar grandes cantidades de datos dependiendo de los parámetros de entrada configurados; ajusta `max_artist` y `max_deep` según tus necesidades y capacidad de procesamiento.