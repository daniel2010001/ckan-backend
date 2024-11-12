# CKAN Backend

Este es el backend del proyecto CKAN, utilizando Django y CKAN API.

## Requisitos

- Python 3.6+
- Pip
- Virtualenv (opcional pero recomendado)

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto:

1. Clonar el repositorio:

   ```sh
   git clone https://github.com/daniel2010001/ckan-backend.git
   cd ckan-backend
   ```

2. Crear un entorno virtual (opcional pero recomendado):

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # En Windows, usar `.venv\Scripts\activate`
   ```

3. Instalar las dependencias:

   ```sh
   pip install -r requirements.txt
   ```

4. Configurar las variables de entorno:

   - Crea un archivo `.env` en el directorio `config` con las siguientes variables:
     ```sh
     SECRET_KEY='tu_clave_secreta_aqui'
     DEBUG=True
     ALLOWED_HOSTS=localhost,127.0.0.1
     DATABASE_URL='postgres://USER:PASSWORD@HOST:PORT/DBNAME'
     CKAN_URL='URL_DE_TU_INSTANCIA_CKAN'
     CKAN_API_KEY='TU_CKAN_API_KEY'
     ```

5. Realizar las migraciones de la base de datos:

   ```sh
   python manage.py migrate
   ```

6. Crear un superusuario (opcional):

   ```sh
   python manage.py createsuperuser
   ```

7. Ejecutar el servidor de desarrollo:
   ```sh
   python manage.py runserver
   ```

## Uso

Después de seguir los pasos anteriores, el servidor estará disponible en `http://localhost:8000/`. Puedes acceder a la interfaz de administración en `http://localhost:8000/admin/` utilizando las credenciales del superusuario que creaste.

## Contribuir

Si deseas contribuir al proyecto, por favor sigue los siguientes pasos:

1. Crea un fork del repositorio.
2. Crea una rama para tu feature o fix:
   ```sh
   git checkout -b feature/nueva-feature
   ```
3. Realiza tus cambios y haz commit:
   ```sh
   git commit -m "Descripción de los cambios"
   ```
4. Sube tus cambios a tu fork:
   ```sh
   git push origin feature/nueva-feature
   ```
5. Abre un Pull Request en el repositorio original.

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo `LICENSE`.
