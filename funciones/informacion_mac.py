'''----------- OPCION MENU 2 -----------
Informar sobre cuál/es son las MAC de los dispositivos adaptadores de red instalados 
en el sistema y almacene en un archivo informacion_local<Apellido1>.csv indicando la 
fecha y hora de creación.  Guardar el archivo y no borrar.
'''
import csv
import subprocess
from datetime import datetime
from pathlib import Path

def info_mac():
    # la función obtiene y muestra las MAC de los adaptadores instalados

    try:
        resultado = subprocess.run(
            ["getmac", "/v", "/fo", "csv", "/nh"], #(/v --> info detallada) (/fo csv --> presenta en csv) (/nh --> elimina la cabecera del comando)
            capture_output= True,
            text= True,
            encoding= "oem", # codificación de windows
            timeout= 10,
            check= True # código de salida != 0 --> CalledProcessError
        )

    except subprocess.TimeoutExpired:
        print(f"La consulta de las MAC superó el tiempo límite")

    except subprocess.CalledProcessError:
        print(f"getmac termino en un error")

    except OSError as error:
        print(f"No se ha podido ejecutar getmac: {error}")
        return

    # interpretamos la salida csv y guardamos las filas en una list
    adaptadores = list(csv.reader(resultado.stdout.splitlines())) # guardamos todas las lineas en formato csv de resultado

    if not adaptadores:
        print("No se han encontrado adaptadores")
        return

    # mostramos las direcciones MAC

    # el diseño de la salida se puede hacer comprobando como devuelve la salida mi pc utilizando
    # el própio comando de getmac /v /fo csv en la terminal

    print("\n ----------- DIRECCIONES MAC -----------")

    for fila in adaptadores:
        conexion = fila[0]
        adaptador = fila[1]
        mac = fila[2]

        # mostramos toda la info de cada dirección
        print(f"Conexión: {conexion}")
        print(f"Adaptador: {adaptador}")
        print(f"MAC: {mac}")

    # guardamos la fecha de creación del csv
    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # guardamos el informe en la carpeta principal del proyecto
    # en este caso será .parent.parent

    carpeta_proyecto = Path(__file__).resolve().parent.parent
    ruta_csv = carpeta_proyecto / "informacion_localSague.csv"

    try:
        with ruta_csv.open(
            "w", # utilizamos esta config que crea el archivo si no existe, y lo reemlaza su contenidosi ya existe
            newline= "", # nos permite que el csv.writer gestione los saltos de línea y evita filas adicionales vacías
            encoding= "utf-8-sig"
        ) as archivo:

            # creamos el objeto que nos escribirá los datos en csv
            escritor = csv.writer(archivo)

            # escribimos la primera fila
            escritor.writerow([
                "fecha_creacion",
                "conexion",
                "adaptador",
                "mac"
            ])

            # ahora escribimos una fila por adaptador
            for fila in adaptadores:
                escritor.writerow([
                    fecha_creacion,
                    fila[0],
                    fila[1],
                    fila[2]
                ])

    except OSError as error:
        print(f"No se ha podido guardar el informe: {error}")

    else:
        print(f"\nInforme guardado en: {ruta_csv}")
        print(f"Fecha y hora de generación: {fecha_creacion}")