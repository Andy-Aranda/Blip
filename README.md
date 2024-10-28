# 💬 Blip 

Este pequeño ejercicio desarrolla una base de datos que aloja información sobre los clientes, pacientes y razas de una veterinaria, apoyándonos del ORM SQLAlchemy para la creación de la misma y sus tablas, además de la creación de un API REST en Python utilizando FastAPI para interactuar con la base de datos a través de operaciones CRUD.

## Requisitos

Tener instalados lo siguiente:

- **Python 3.8+**
- **FastAPI** y **SQLAlchemy** (si no están instalados, ver la sección de instalación de dependencias)

## Instalación

1. Clonar el repositorio:

    ```bash
    git clone https://github.com/Andy-Aranda/Blip.git
    cd Blip
    ```

2. Crear un entorno virtual para aislar las dependencias:

    ```bash
    python -m venv venv
    ```

3. Activa el entorno virtual:

    - En **Windows**:

      ```bash
      venv\Scripts\activate
      ```

    - En **MacOS/Linux**:

      ```bash
      source venv/bin/activate
      ```

4. Instalar las dependencias necesarias:

    ```bash
    pip install fastapi sqlalchemy uvicorn
    ```

## Configuración y Ejecución

1. Correr el archivo `database.py` usando el comando:
    ```bash
    python3 database.py
    ```
    Esto permitirá crear la base de datos. Se recomienda tener instalada alguna extensión de SQLite en VisualStudio para visualizar las tablas de la base de datos o instalar directamente DB Browser for SQLite. 

2. Ejecuta la aplicación con el siguiente comando:

    ```bash
    uvicorn main:app --reload
    ```

   Esto iniciará un servidor en `http://127.0.0.1:8000`.

## Uso de la API

Para interactuar con la API, se pueden utilizar herramientas como [Postman](https://www.postman.com/) o acceder a la documentación generada automáticamente por FastAPI en `http://127.0.0.1:8000/docs`.

### Endpoints

- `POST /personas/`: Crear una nueva persona
- `GET /personas/`: Obtener una lista de personas
- `GET /personas/{persona_id}`: Obtener una persona por ID
- `PUT /personas/{persona_id}`: Actualizar una persona existente
- `DELETE /personas/{persona_id}`: Eliminar una persona por ID

## Base de Datos

La base de datos se gestiona mediante el archivo `database.py`. Cuando se ejecuta por primera vez, se crea el archivo `veterinaria.db` en el directorio del proyecto.


