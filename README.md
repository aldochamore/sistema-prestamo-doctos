# 🏛️ Sistema de Gestión de Archivo

Este es un sistema web Full Stack desarrollado en Python y Flask para gestionar el inventario y los préstamos de documentos (libros, actas, expedientes). 

El sistema está diseñado para integrarse con lectores de códigos de barras, garantizando rapidez y evitando errores de captura manual.

## 🚀 Características Principales
- **Control de Inventario:** Rastreo en tiempo real de qué documentos están disponibles y cuáles están prestados.
- **Historial de Préstamos:** Registro transaccional de salidas y devoluciones.
- **Validación Lógica:** Prevención de errores comunes (ej. intentar prestar un documento ya prestado).
- **Dashboard Activo:** Vista instantánea de los préstamos en curso.
- **Diseñado para Hardware:** Interfaz optimizada para ingreso rápido vía escaner de código de barras.

## 🛠️ Tecnologías Utilizadas
* **Backend:** Python 3.x, Flask
* **Base de Datos:** PostgreSQL
* **Frontend:** HTML5, Bootstrap 5
* **Librerías:** `psycopg2-binary` (Conexión a DB)

## ⚙️ Requisitos Previos
Para correr este proyecto en tu entorno local, necesitas tener instalado:
1. Python 3.x
2. PostgreSQL (y pgAdmin para administrarlo).

## 📥 Instalación y Configuración

**1. Clonar el repositorio:**
Descarga este código en tu computadora.

**2. Configurar el Entorno Virtual (Recomendado):**

  Bash
    
    python -m venv venv
    source venv/bin/activate

**En Windows usa:** 

    venv\Scripts\activate

**3. Instalar dependencias:**

  Bash

    pip install flask psycopg2-binary


**4. Configurar la Base de Datos:**

Abre pgAdmin y crea una base de datos llamada registro_civil.

Ejecuta el archivo esquema.sql incluido en este repositorio para crear las tablas y datos de prueba.

Abre el archivo db.py y actualiza el diccionario DB_CONFIG con tus credenciales locales:
    
  Python

    DB_CONFIG = {
        "host": "localhost",
        "database": "registro_civil",
        "user": "postgres",
        "password": "TU_PASSWORD",
        "port": "5432"
    }

**▶️ Ejecución del Sistema**

Para encender el servidor web, ejecuta el siguiente comando en la terminal:
  
  Bash

    python app.py

El sistema estará disponible en tu navegador en la dirección: http://127.0.0.1:5000
