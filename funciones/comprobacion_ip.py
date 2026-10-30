'''----------- OPCION MENU 1 -----------
Diseñar una función que lea el contenido de un archivo de texto que consiste en una serie de 
direcciones IP cada una de las cuales ocupa una línea de éste. La ruta y nombre del archivo de 
texto se preguntarán al usuario e inicialmente se mostrará el contenido de este por pantalla.
Finalmente lanzará un ping para cada una de las IP’s y determinará e informará sobre cuáles de 
las anteriores responden afirmativamente a este comando. 
'''
from pathlib import Path

# funcion para el submenú de comprobación de IP, nos permite seleccionar un archivo y mostrar su contenido
def menu_comprobacion_ip():

    opcion = ""

    while opcion != "0":
        print("\n----------- COMPROBACIÓN DE IP -----------")
        print("1. Seleccionar archivo de texto con direcciones IP")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            # pedimos al usuario el nombre y la ruta del archivo de texto
            nombre = input("Ingrese el nombre del archivo (.txt): ").strip()
            # si no se entra nada vamos a asumir la ruta "hardcodeada" más cómodo de momento
            if not nombre:
                nombre = "web_2026_1.txt"

            ubicacion = input("Ingrese la ruta del archivo: ").strip()
            # si no se entra nada vamos a asumir la ruta "hardcodeada" más cómodo de momento
            if not ubicacion:
                ubicacion = "."

            # creamos la ruta completa del archivo
            ruta = Path(ubicacion) / nombre

            try:
                # abrimos el archivo y leemos su contenido
                with open(ruta, "r") as archivo:
                    contenido = archivo.read()

            except (UnicodeError, OSError) as error:
                    print(f"Error: No se pudo abrir el archivo {error}.")

            else:                      
                # mostramos el contenido del archivo por pantalla (más adelante posible cambiar la forma de confirmación)
                print("\nContenido del archivo:")
                print(contenido)

        elif opcion == "0":
            print("Volviendo al menú principal...")

        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")