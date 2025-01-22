# THE SOWER
---
## Requisitos
El manual de construccion del robot se encuentra en formato .docx y .pdf en la siguiente carpeta de Google drive. Ahi se describe en detalle todo el hardware requerido para ejecutar este proyecto.

## Instalacion
Este proyecto corre en una maquina Linux sin excepcion, pues la comunicacion con la camara se realiza a traves del firmware V4L2 (Video4Linux2) y un sistema de archivos estilo Unix. Adicionalmente el archivo `install.sh` se ejecuta en bash.

### 1.- Clona el repositorio
En una terminal abierta en la carpeta en donde quieras guardar el archivo ejecuta:

```
git clone git@github.com:ernstmv/theSower.git
```

### 2.- Ejecuta el instalador
Muevete al repositorio clonado theSower con `cd`. Una vez ahi encontraras una archivo `.sh`. Ejecutalo usando:

```
sh install.sh
```

O con `chmod +x install.sh` seguido de `./install.sh`. Recibiras un mensaje que diga "Installation finished" cuando la instalacion se halla terminado sin errores.

### 3.- Activa el entorno virtual

En el directorio actual encontraras un directorio `virtualenv`, para ejecutar este entorno virtual haz:

```
source virutalenv/bin/activate
```
Podrias necesitar usuar otro formato de archivo `activate` si usas fish u otro shell.

### 4.- Ejecuta el archivo

La ultima version del codigo se encuentra en el directorio `stage2/`. Para ejecutarlo muevete nuevamente a esta carpeta con `cd` y ejecuta:

```
python3 main.py
```

El programa deberia ejecutarse sin problemas.
