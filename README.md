
# E-nergy

Esta es una pequeña App que te muestra como mejorar tu consumo de energia

# Instalacion y Ejecucion
primero clona el repositorio mediante el siguiente comando

```console
git clone https://github.com/parZival26/E-nergy.git

```

luego accede a la carpeta donde se encuentren los requerimientos
```console
cd E-nergy/

```

Crea un entorno virtual
```console
python -m venv env
```
Inica el entorno virtual
```console
source env/Scripts/activate
```
Instala las libreias requeridas
```console
pip intall -r requirements.txt
```
Añade el archivo .env en la misma carpeta que el archivo settings.py

Posisionate en la mimas carpeta que el manage.py y ejecuta el siguientes comando para correr la App
```console
py manage.py migrate
py manage.py runserver
```

Por ultimo en tu navegador accede al LocalHost o a la siguiente url:  http://127.0.0.1:8000/

¡Listo y Bienvenido a E-nergy!