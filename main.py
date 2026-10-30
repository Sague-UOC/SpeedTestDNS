# --- MENÚ PRINCIPAL ---
from funciones.comprobacion_ip import menu_comprobacion_ip

def menu_principal():

    # inicializa la variable de opción
    opcion = ""

    # bucle principal del menú con salida cuando el usuario ingresa "0"
    while opcion != "0":
        print("\n----------- MENÚ PRINCIPAL -----------")
        print("1. Comprobación de IP")
        print("2. Información de MAC")
        print("3. Configuración de Red")
        print("0. Salir")

        # lee la opción del usuario
        opcion = input("Seleccione una opción: ").strip()

        # llama a la función correspondiente según la opción seleccionada
        if opcion == "1":
            menu_comprobacion_ip()
        elif opcion == "2":
            print("información de MAC")
        elif opcion == "3":
            print("configuración de red")
        else:
            if opcion != "0":
                print("Opción inválida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    menu_principal()
