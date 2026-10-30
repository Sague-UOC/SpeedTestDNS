'''----------- OPCION MENU 1 -----------
Diseñar una función que lea el contenido de un archivo de texto que consiste en una serie de 
direcciones IP cada una de las cuales ocupa una línea de éste. La ruta y nombre del archivo de 
texto se preguntarán al usuario e inicialmente se mostrará el contenido de este por pantalla.
Finalmente lanzará un ping para cada una de las IP’s y determinará e informará sobre cuáles de 
las anteriores responden afirmativamente a este comando. 
'''
import subprocess
from ipaddress import IPv4Address
from pathlib import Path

def obtener_ruta(nombre, ubi):
    # creamos la ruta completa del archivo
    return Path(ubi) / nombre

def guarda_ip_lista(archivo):
    # retorna la lista con todas las ip
    ip_list = []

    for linea in archivo: # vamos a tener que hacer más funciones para la obtención de archivo en opcion1()
        ip = linea.strip()         
        if ip:
            ip_list.append(ip)

    return ip_list

def comprobar_ping_ip(ip_list):
     # está funcion ejecuta un ping por cada ip que haya en la lista (ip_list)
     # vamos a tener en cuenta que vamos a trabajar con IPv4 así que debemos importar IPv4Address
     # también vamos a utilizar subprocess.run() --> esto nos va a permitir ejecutar un programa, esperar a que termine y obtener sus resultados

     # comprobamos que la list no esté vacía
     if not ip_list:
        print("No hay direcciones para comprobar")
        return

     # procedemos a ejecutar los ping de todas las ip y mostrar los resultados

     print("\n--- RESULTADOS DE LOS PINGS ---")

     for ip in ip_list:
        try:
            # comprobación de que la ip és válida
            IPv4Address(ip)

            # ejecución y almacenamiento de la salida de los pings
            resultado = subprocess.run(
               ["ping", "-4", "-n", "1", "-w", "1000", ip], # (-4 --> IPv4) (-n 1 --> envía 1 petición) (-w 1000 --> espera 1000 milisegundos para una respuesta)
               capture_output= True,
               text= True,
               timeout= 5 # le ponemos un tiempo máximo de ejecución al subprocess
            )

        # añadimos el control de errores con los except
        except ValueError:
            print(f"{ip} dirección IPv4 no válida")

        except subprocess.TimeoutExpired:
            print(f"{ip} el comando superó el tiempo límite")

        except OSError as error:
            print(f"No se ha podido ejecutar ping: {error}")
            return

        else:
            # comprobamos que ip responden al ping y cuales no
            responde = (
                resultado.returncode == 0 and "ttl=" in resultado.stdout.lower() # utilizamos el .returncode para ver si el código con el que ha terminado es = 0, y el stdout para ver el texto que ha mostrado en el comando
            )

            if responde:
                print(f"{ip} responde al ping")

            else:
                print(f"{ip} sin respuesta positiva")



def opcion1():
    # pedimos al usuario el nombre y la ruta del archivo de texto
                nombre = input("Ingrese el nombre del archivo (.txt): ").strip()
                # si no se entra nada vamos a asumir la ruta "hardcodeada" más cómodo de momento
                if not nombre:
                    nombre = "web_2026_1.txt"
    
                ubicacion = input("Ingrese la ruta del archivo: ").strip()
                # si no se entra nada vamos a asumir la ruta "hardcodeada" más cómodo de momento
                if not ubicacion:
                    ubicacion = "."
    
                ruta = obtener_ruta(nombre, ubicacion)
    
                try:
                    # abrimos el archivo y leemos su contenido
                    with ruta.open("r") as archivo:
                        print("\n Contenido del archivo: ")

                        ip_list = guarda_ip_lista(archivo)

                        # muestra todas las ip almacenadas
                        for ip in ip_list:
                            print(ip)
    
                except (UnicodeError, OSError) as error:
                        print(f"Error: No se pudo abrir el archivo {error}.")

                else:
                    print() # linea vacía para mejora visual 
                    comprobar_ping_ip(ip_list)


# funcion para el submenú de comprobación de IP, nos permite seleccionar un archivo y mostrar su contenido
def menu_comprobacion_ip():

    opcion = ""

    while opcion != "0":
        print("\n----------- COMPROBACIÓN DE IP -----------")
        print("1. Seleccionar archivo de texto con direcciones IP")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            opcion1()

        elif opcion == "0":
            print("Volviendo al menú principal...")

        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")