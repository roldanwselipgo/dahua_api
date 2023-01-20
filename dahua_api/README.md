# elipgo-prueba

En la url http://127.0.0.1:8000/ es una vista para agregar 1 o mas camaras

- Cuenta con un boton para agregar una camara ingresando la url y su autenticacion

- El boton de Ver enviara a la url http://127.0.0.1:8000/camera/1 donde se accede a la camara
    y se consultan algunos metodos del api

- Tambien se toma en ese momento un snapshot, se manda a un archivo .jpg y se muestra en la vista

- monitor/Monitor/Camera.py  define un dispositivo Camara
- monitor/Monitor/Comunicacion.py construye los datos del protocolo
- monitor/Monitor/Interfaz.py  envia y recibe peticiones usando la libreria requests
- monitor/views.py instancia un objeto Camara y obtienene datos para enviarlas vistas del navegador


[ Ejecucion ]

pip install -r requeriments
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
