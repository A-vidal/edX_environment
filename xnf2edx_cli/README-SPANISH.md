# Descripción

Herramienta en linea de comandos para convertir ficheros XNF en cursos de edX
en .tar.gz.

Basada en el trabajo de leosamu en:
https://github.com/leosamu/UPVX-tools

# Instalación
Hay dos formas de instalar el proyecto: la tradicional y con Docker

## Docker
Usar un contenedor Docker es la forma más sencilla de evitar los errores
derivados de incompatibilidades derivadas del entorno, o también si no quieres
instalar ningún software adicional, crear entornos virtuales, etc. Sin embargo,
necesitarás tener Docker instalado en tu sistema, obviamente.

Tienes la documentación oficial para instalar Docker cualquier SO aquí:

https://docs.docker.com/get-docker/

### Obtener la imagen
Cuando usas Docker, de nuevo, tienes dos posibilidades de obtener la imagen:

1. Descargar una imagen ya generada desde el Docker Hub (disponible en
   https://hub.docker.com/repository/docker/serbaf/xnf2edx_cli):
    
`docker image pull serbaf/xnf2edx_cli:latest`

2. Construir la imagen tú mismo usando el Dockerfile disponible en el proyecto
   (el último argumento del comando es la ruta al directorio del Dockerfile):
   
`docker build -t serbaf/xnf2edx .`

### Ejecutar el contenedor
Una vez la imagen ha sido construida o descargada, puedes ejecutar el script
dentro de ella corriendo como un contenedor. Para hacerlo, deberás llamar al
script usando su sintaxis normal (`python main.py some_xnf_file.xlsm`) pero
dentro de un contenedor en ejecución de la imagen xnf2edx (`docker run serbaf/xnf2edx_cli`)
y finalmente compartir los archivos de entrada y salida entre tu sistema de
archivos local y el del contenedor, lo cual se logra utilizando el sistema de
volúmenes (`-v /tu/ruta/local:/ruta/del/contenedor`).

La ruta de salida en el contenedor deberá ser siempre
`/xnf2edx_cli/data/output`, y la puedes mapear a cualquier directorio de tu
computadora. El archivo de entrada puede mapearse libremente, pero quizá lo más
sencillo sea simplemente colocarlo en el directorio `xnf2edx_cli` del
contenedor, ya que es el directorio de trabajo del mismo.

Un ejemplo de ejecución podría ser el siguiente:

```
docker run
-v /home/user/xnf2edx_cli/data/input/Termodinamica.xlsm:/xnf2edx_cli/Termodinamica.xlsm
-v /home/user/Downloads/test/:/xnf2edx_cli/data/output/
serbaf/xnf2edx_cli
python main.py Termodinamica.xlsm
```
En Windows:

```
docker run 
-v C:/Users/ndesp/Downloads/TemplateXNF.xlsm:/xnf2edx_cli/TemplateXNF.xlsm 
-v C:/Users/ndesp/Downloads/test:/xnf2edx_cli/data/output/ 
serbaf/xnf2edx_cli 
python main.py TemplateXNF.xlsm
```

## Forma tradicional
Este modo consiste en simplemente descargar el código fuente, preparar el
entorno Python y lanzar el script. Es muy sencillo, sin embargo, en algunos
entornos podrían aparecer errores inesperados debido al contexto, en cuyo caso
se recomienda usar el método Docker.

1. Clona el proyecto

    `git clone https://git.upv.es/serpucga/xnf2edx_cli.git`

2. Ve al directorio raíz del proyecto

    `cd xnf2edx_cli`

3. Crea un entorno virtual de python3 (3.6 o posterior):

    ```
    python -m venv .venv
    ```
    
4. Activa el entorno:
    
    - En Linux:
        `source .venv/bin/activate`

    - En Windows:
        `.\venv\Scripts\activate.bat`

5. Instala los requerimientos en el entorno virtual activo (usa dev.txt si
   necesitas las librerías de desarrollo/debug)

    `python -m pip install -r requirements/prod.txt`

6. Lanza el script pasándole el fichero XNF como único argumento

    `python main.py ~/Downloads/XNF.xlsm`

7. Encontrarás los ficheros de salida en el directorio
   **./data/output/{xnffilename}/**
    1. curso .tar.gz: **{coursecode}.tar.gz**
    2. Directorio del curso sin comprimir: **{coursecode}**
    3. Logs: **logs.html**
    4. Errores (no existirá fichero si todo ha salido OK): **errors.html**

# Plantillas y ficheros de prueba

En la carpeta assets encontrarás un archivo excel con una Plantilla en inglés y
otro con una Plantilla en español que puedes modificar para crear tus cursos y
un archivo de ejemplo con preguntas que se pueden importar a la pestaña
correspondiente llamando a la macro con control+ U desde la hoja de cálculo
(recuerde activar las macros al cargar la hoja de cálculo).

# Vídeos con instrucciones

Tienes una lista de vídeos con instrucciones sobre cómo usar la hoja en
https://media.upv.es/#/portal/channel/a2d0caed-721f-4ef6-bd0b-16cc2142c7c9

Estos vídeos se crearon para ayudar a los profesores de la UPV con el proceso,
con lo que hay alguna referencia a procesos internos que no os servirá
(principalmente a la extracción de los códigos de los vídeos del sistema de
media de la UPV, pero hemos creado un vídeo específico explicando cómo sacar
los datos de una lista de reproducción de Youtube).
