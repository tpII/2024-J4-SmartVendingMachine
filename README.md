# Smart Fridge

**Smart Fridge** es una aplicacion de codigo abierto diseada para gestionar y optimizar la compra de alimentos en refrigeradores comunitarios ubicados en reas de alta afluencia. A travs de la aplicacion, los usuarios pueden adquirir productos dentro del refrigerador mediante una plataforma de Ecommerce. Una vez completada la compra, el refrigerador se desbloquea, permitiendo el acceso al artculo adquirido. Utilizamos un sistema de cmaras y tecnologa de inteligencia artificial para monitorear las extracciones y garantizar que coincidan con las compras realizadas, lo que permite el dbito automtico en la tarjeta del usuario por el producto retirado.


Este proyecto fue presentado por **Aldana Tedesco**, **Emiliano Mengoni**, **Lisandro Vicens**, y **Toms Schattmann**. El backend est desarrollado en **Django Rest Framework** y el frontend utiliza **Next.js** con **React**.

---

## Instalacion

### Requisitos previos
- Python 3.8+
- Node.js 14+
- Django Rest Framework
- Next.js

---

### Instalacion del Backend (Django Rest Framework)

1. Clona el repositorio del proyecto:

   ```bash
   cd Backend

2. Crea y activa un entorno virtual:
        
    En Linux/MacOS:

        python3 -m venv venv
        source venv/bin/activate

    En Windows:

        python -m venv venv
        venv\Scripts\activate

3. Instala las dependencias de Python:

        pip install -r requirements.txt

3*. Crear container docker con las credenciales correctas:

        docker run --name some-postgres -e POSTGRES_DB=smartfridgebd -e POSTGRES_USER=smart -e POSTGRES_PASSWORD=fridge -p 5432:5432 -d postgres

4. Realiza las migraciones de base de datos:

        python manage.py migrate

5. Crea un superusuario para acceder al panel de administracion:

        python manage.py createsuperuser

6. Ejecuta el servidor de desarrollo de Django:

        python manage.py runserver

El backend estar corriendo en http://localhost:8000/.


## Instalacion del Frontend (Next.js con React)

1. Ve al directorio del frontend:

        cd Frontend

2. Instala las dependencias de Node.js:

        npm install

3. Configura las variables de entorno:
    
    Crea un archivo .env en la raz del proyecto con las siguientes variables:

        NEXT_PUBLIC_API_URL=http://localhost:8000/

4. Ejecuta el servidor de desarrollo de Next.js:

        npm run dev

El frontend estar corriendo en http://localhost:3000/.

## Uso

Una vez que tanto el backend como el frontend estn en funcionamiento, puedes acceder a la aplicacion desde http://localhost:3000. Si necesitas acceder al panel de administracion de Django, ve a http://localhost:8000/admin e inicia sesion con el superusuario que creaste.


## Contribucion

Este proyecto es de codigo abierto. Si quieres contribuir, por favor crea un fork del repositorio, realiza tus cambios y enva un pull request. Las contribuciones son bienvenidas.

## Licencia

Smart Fridge es un proyecto de codigo abierto bajo la licencia MIT.
