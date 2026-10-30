'''----------- OPCION MENU 2 -----------
Informar sobre cuál/es son las MAC de los dispositivos adaptadores de red instalados 
en el sistema y almacene en un archivo informacion_local<Apellido1>.csv indicando la 
fecha y hora de creación.  Guardar el archivo y no borrar.
'''
import csv
import subprocess

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