# Dahua api

url:  http://127.0.0.1:8000/ 

- Agregar nuevas camaras y acceder a su configuracion
- Modificar la configuracion de canales



[ Ejecucion ]

pip install -r requeriments
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


[ Otros comandos ]

celery -A app worker --loglevel=info --autoscale=10,2
celery -A app flower


[ dependences ]
sudo apt install default-libmysqlclient-dev