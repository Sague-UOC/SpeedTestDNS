'''----------- OPCION MENU 3 -----------
Diseñar una función cuya funcionalidad que muestre los adaptadores de 
red de la máquina local. Se mostrará y almacenará en un archivo adaptador<Apellido1>.txt 
la información para un adaptador de red; él cual, se preguntará previamente al usuario 
(elegido por el usuario) su IP, máscara, y puerta de enlace. El resto de configuraciones 
de red no se han de mostrar esta información. Para realizar lo anterior la función 
lanzará un comando de dos que le proporcionará la información que necesita junto con 
otra que no se considera relevante, y será capaz de extraer y mostrar la que se ha 
detallado.
'''
import subprocess
from ipaddress import IPv4Address
from pathlib import Path

def obtener_adaptadores():
    # obtiene los adaptadores y extrae su configuración IPv4.
    # interpretamos la salida de ipconfig de mi pc que es la de Windows en español.

    try:
        resultado = subprocess.run(
            ["ipconfig"],
            capture_output= True,
            text= True,
            encoding= "oem",
            errors= "replace",
            timeout= 10,
            check= True
        )

    except subprocess.TimeoutExpired:
        print("La consulta ha superado el tiempo máximo")
        return []

    except subprocess.CalledProcessError:
        print("El dominio ipconfig terminó con un error")
        return []

    except OSError as error:
        print(f"No se ha podido ejecutar ipconfig: {error}")
        return []

    # inicializamos la list de adaptadores
    adaptadores = []

    # inicializamos un diccionario para el adaptador en que estamos
    adaptador_actual = None

    # inicializamos una variable para saber si debemos buscar la puerta de enlace, ya que en nuestra
    # versión del ipconfig la puerta de enlace se encuentra debajo de la línea de este modo:
    # Puerta de enlace predeterminada . . . . . : fe80::a28a:6ff:fea3:c980%9
    #                                   192.168.1.1
    # como estamos trabajando con IPv4 deberemos recoger 192.168.1.1 en este caso
    leyendo_puerta = False

    for linea in resultado.stdout.splitlines():
        texto = linea.strip()

        # cada encabezado inicia un nuevo adaptador
        # inicializamos todos los campos como no asig, ya que se asignarán más adelante
        if texto.startswith("Adaptador ") and texto.endswith(":"):
            adaptador_actual = {
                "nombre": texto[:-1], # conserva el encabezado quitando los : finales
                "ip": "no asig",
                "mascara": "no asig",
                "puerta_enlace": "no asig"
            }

            # actualizamos la lista de adaptadores guardando el actual
            adaptadores.append(adaptador_actual)
            leyendo_puerta = False
            continue

        # ignoramos las líneas vacías y al primer adaptador (inicialización)
        if not texto or adaptador_actual is None:
            continue

        # inicializamos todos los campos buscando uno por uno en el texto
        # texto.split(":", 1)[1].strip() --> esto nos obtiene el primer valor después de : y elimina espacios
        if "Dirección IPv4" in texto:
            adaptador_actual["ip"] = texto.split(":", 1)[1].strip()
            leyendo_puerta = False

        elif "Máscara de subred" in texto:
            adaptador_actual["mascara"] = texto.split(":", 1)[1].strip()
            leyendo_puerta = False

        elif "Puerta de enlace predeterminada" in texto:
            leyendo_puerta = True
            texto = texto.split(":", 1)[1].strip()

        elif ":" in texto:
            # otra propiedad indica que ha terminado el campo anterior.
            leyendo_puerta = False

        # la puerta IPv4 puede aparecer en su própia línea o en la siguiente, con lo que debemos buscarla
        if leyendo_puerta:
            try:
                puerta = IPv4Address(texto) # comprobamos si el texto es un puerto IPv4

            except ValueError:
                continue

            else:
                adaptador_actual["puerta_enlace"] = str(puerta) # guardamos la puerta cuando la encontramos

    return adaptadores


def informe_adaptador():
    # nos permite seleccionar un adaptador y mostrar sus datos
    # dispone de un submenú para la selección

    adaptadores = obtener_adaptadores()

    # retorna si no hay adaptadores disponibles para mostrar
    if not adaptadores:
        print("No hay adaptadores disponibles")
        return

    # mostrar adaptadores y selección de adaptador
    print("\n--- SELECCIÓN DE ADAPTADOR ---")

    for num, adaptador in enumerate(adaptadores, start= 1):
        print(f"{num}. {adaptador["nombre"]}")

    print("0. Volver al menú principal")

    # repetimos hasta obtener una selección válida del usuario
    while True:
        try:
            opcion = int(input("Selecciona un adaptador: ").strip())

        except ValueError:
            print("Introduce un número válido")
            continue

        # volvemos al menú
        if opcion == 0:
            return

        # guardamos la opción seleccionada (1 hasta len(adaptadores - 1))
        if 1 <= opcion <= len(adaptadores):
            seleccionado =  adaptadores[opcion - 1]
            break

        print("No existe un adaptador con ese número, prueba de nuevo")

    # preparamos el informe que se va a mostrar del adaptador elegido
    informe = (
        f"Adaptador: {seleccionado["nombre"]}\n"
        f"IPv4: {seleccionado["ip"]}\n"
        f"Máscara: {seleccionado["mascara"]}\n"
        f"Puerta de enlace: {seleccionado["puerta_enlace"]}\n"
    )

    # mostramos el informe del adaptador seleccionado
    print("\n--- CONFIGURACIÓN DEL ADAPTADOR ---")
    print(informe)

    # guardamos el documento formato adaptador<apellido1>.txt de la misma forma que hemos
    # guardado antes el csv en la carpeta principal del proyecto
    carpeta_proyecto = Path(__file__).resolve().parent.parent
    ruta_txt = carpeta_proyecto / "adaptadorSague.txt"

    try:
        with ruta_txt.open(
            "w", # utilizamos esta config que crea el archivo si no existe, y lo reemlaza su contenidosi ya existe
            encoding= "utf-8"
        ) as archivo:

            # escribimos el informe en el archivo .txt creado
            archivo.write(informe)

    except OSError as error:
        print(f"No se ha podido guardar el informe: {error}")

    else:
        print(f"Informe guardado en: {ruta_txt}")