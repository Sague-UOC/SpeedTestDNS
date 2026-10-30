'''----------- OPCION MENU 1 -----------
Diseñar una función que lea el contenido de un archivo de texto que consiste en una serie de 
direcciones IP cada una de las cuales ocupa una línea de éste. La ruta y nombre del archivo de 
texto se preguntarán al usuario e inicialmente se mostrará el contenido de este por pantalla.
Finalmente lanzará un ping para cada una de las IP’s y determinará e informará sobre cuáles de 
las anteriores responden afirmativamente a este comando. 
'''
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