# Proyecto Ingenieria de Software y Magneto

## KeyWork: Proyecto Django con Python

Este es un proyecto sencillo desarrollado en Django con Python, diseñado para ser un modelo por el cual se pueda tener un manejo de hojas de vida automatizando su envio y descarga 
y funcionalidades por medio de IA.

## integrantes

- Felipe Ochoa
- Esteban Molina
- Juan Gonzalo de los Rios
- Mariana Muñoz

## Requisitos previos

Asegúrate de tener lo siguiente instalado en tu sistema:

- **Python** (Versión 3.8 o superior)
- **Django** (Versión más reciente, puedes instalarlo con `pip install django`)
- **Un IDE o editor de texto** compatible con Python, como **PyCharm**, **Visual Studio Code** (con la extensión de Python instalada) u otro.
- **Git** para clonar el repositorio.

### Instalación rápida
Si no tienes Python y Django instalados, puedes configurarlos rápidamente con los siguientes comandos:

```sh
# Verifica que Python esté instalado
python --version  # o python3 --version

# Instala Django
pip install django

# Verifica la instalación de Django
python -m django --version
```

### Clonar el repositorio

Para obtener el proyecto en tu equipo, usa el siguiente comando:

```sh
git clone https://github.com/FelipeOchoaL/KeyWork.git
cd djangoproject
```
## Ejecutar el proyecto localmente:
Para ejecutar el proyecto Django en tu máquina local, sigue estos pasos:

1. **Instalar dependencias**
   ```sh
   pip install -r requirements.txt
   ```

2. **Aplicar migraciones**
   ```sh
   python manage.py migrate
   ```

3. **Iniciar el servidor de desarrollo**
   ```sh
   python manage.py runserver
   ```

Esto ejecutará la aplicación en la terminal. Se abrirá en el navegador en la URL especificada (por defecto es `http://127.0.0.1:8000`).

---

## Ejecutar pruebas:
Para ejecutar las pruebas del proyecto, usa el siguiente comando:
```sh
python manage.py test
```
