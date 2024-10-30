import mysql.connector
from datetime import datetime

# Conectar a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root", 
    password="root",
    database="proyecto_final_database"
)
# Función para agregar un cliente
def agregar_cliente():
    cursor = conexion.cursor()

    # Ingresar información de la dirección
    print("\n--- Registro de Dirección ---")
    pais = input("País: ")
    departamento = input("Departamento: ")
    ciudad = input("Ciudad: ")
    barrio = input("Barrio: ")
    nomenclatura = input("Nomenclatura: ")
    descripcion = input("Descripción (Opcional): ")

    # Insertar en la tabla DIRECCION
    query_direccion = """
        INSERT INTO DIRECCION (PAIS, DEPARTAMENTO, CIUDAD, BARRIO, NOMENCLATURA, DESCRIPCION)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query_direccion, (pais, departamento, ciudad, barrio, nomenclatura, descripcion))
    conexion.commit()

    id_direccion = cursor.lastrowid  # Obtener el ID de la dirección recién insertada

    # Ingresar información del cliente
    print("\n--- Registro de Cliente ---")
    num_identificacion = int(input("Número de Identificación: "))
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    genero = input("Género (M/F): ")
    edad = int(input("Edad: "))
    telefono = input("Teléfono: ")
    email = input("Email: ")
    ocupacion = input("Ocupación: ")
    ingreso_mensual = float(input("Ingreso Mensual: "))
    egreso_mensual = float(input("Egreso Mensual: "))
    score = int(input("Score de Crédito: "))

    # Insertar en la tabla CLIENTE
    query_cliente = """
        INSERT INTO CLIENTE (NUM_IDENTIFICACION, NOMBRE, APELLIDO, GENERO, EDAD, TELEFONO, EMAIL, OCUPACION, INGRESO_MENSUAL, 
        EGRESO_MENSUAL, SCORE, ID_DIRECCION)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query_cliente, (num_identificacion, nombre, apellido, genero, edad, telefono, email, ocupacion, ingreso_mensual, 
                                   egreso_mensual, score, id_direccion))
    conexion.commit()

    print("Cliente agregado exitosamente.")

# Función para agregar credenciales del cliente
def agregar_credenciales(num_identificacion):
    cursor = conexion.cursor()

    print("\n--- Registro de Credenciales ---")
    usuario = input("Nombre de Usuario: ")
    contraseña = input("Contraseña: ")

    # Insertar en la tabla CREDENCIALES
    query_credenciales = """
        INSERT INTO CREDENCIALES (NUM_IDENTIFICACION, USUARIO, CONTRASEÑA, ULTIMA_CONEXION)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query_credenciales, (num_identificacion, usuario, contraseña, datetime.now()))
    conexion.commit()

    print("Credenciales del cliente agregadas exitosamente.")

# Función para actualizar un cliente
def actualizar_cliente():
    cursor = conexion.cursor()

    num_identificacion = int(input("Ingrese el número de identificación del cliente que desea actualizar: "))

    # Consultar si el cliente existe
    query = "SELECT * FROM CLIENTE WHERE NUM_IDENTIFICACION = %s"
    cursor.execute(query, (num_identificacion,))
    resultado = cursor.fetchone()

    if resultado:
        print("\n--- Actualizar Información del Cliente ---")
        nombre = input("Nuevo Nombre (o dejar en blanco para mantener): ")
        apellido = input("Nuevo Apellido (o dejar en blanco para mantener): ")
        telefono = input("Nuevo Teléfono (o dejar en blanco para mantener): ")
        email = input("Nuevo Email (o dejar en blanco para mantener): ")
        ocupacion = input("Nueva Ocupación (o dejar en blanco para mantener): ")
        ingreso_mensual = input("Nuevo Ingreso Mensual (o dejar en blanco para mantener): ")
        egreso_mensual = input("Nuevo Egreso Mensual (o dejar en blanco para mantener): ")

        # Actualizar los campos solo si se ingresaron valores
        query_update = "UPDATE CLIENTE SET "
        fields = []
        values = []

        if nombre:
            fields.append("NOMBRE = %s")
            values.append(nombre)
        if apellido:
            fields.append("APELLIDO = %s")
            values.append(apellido)
        if telefono:
            fields.append("TELEFONO = %s")
            values.append(telefono)
        if email:
            fields.append("EMAIL = %s")
            values.append(email)
        if ocupacion:
            fields.append("OCUPACION = %s")
            values.append(ocupacion)
        if ingreso_mensual:
            fields.append("INGRESO_MENSUAL = %s")
            values.append(float(ingreso_mensual))
        if egreso_mensual:
            fields.append("EGRESO_MENSUAL = %s")
            values.append(float(egreso_mensual))

        if fields:
            query_update += ", ".join(fields) + " WHERE NUM_IDENTIFICACION = %s"
            values.append(num_identificacion)

            cursor.execute(query_update, values)
            conexion.commit()
            print("Cliente actualizado exitosamente.")
        else:
            print("No se realizaron cambios.")
    else:
        print("Cliente no encontrado.")

# Función para eliminar un cliente
def eliminar_cliente():
    cursor = conexion.cursor()

    num_identificacion = int(input("Ingrese el número de identificación del cliente que desea eliminar: "))

    # Eliminar las credenciales del cliente primero
    query_credenciales = "DELETE FROM CREDENCIALES WHERE NUM_IDENTIFICACION = %s"
    cursor.execute(query_credenciales, (num_identificacion,))
    conexion.commit()

    # Luego eliminar el cliente
    query_cliente = "DELETE FROM CLIENTE WHERE NUM_IDENTIFICACION = %s"
    cursor.execute(query_cliente, (num_identificacion,))
    conexion.commit()

    print("Cliente eliminado exitosamente.")

# Función para consultar un cliente
def consultar_cliente():
    cursor = conexion.cursor()

    num_identificacion = int(input("Ingrese el número de identificación del cliente que desea consultar: "))

    query = "SELECT * FROM CLIENTE WHERE NUM_IDENTIFICACION = %s"
    cursor.execute(query, (num_identificacion,))
    resultado = cursor.fetchone()

    if resultado:
        print(f"\n--- Información del Cliente ---")
        print(f"Número de Identificación: {resultado[0]}")
        print(f"Nombre: {resultado[1]} {resultado[2]}")
        print(f"Género: {resultado[3]}")
        print(f"Edad: {resultado[4]}")
        print(f"Teléfono: {resultado[5]}")
        print(f"Email: {resultado[6]}")
        print(f"Ocupación: {resultado[7]}")
        print(f"Ingreso Mensual: {resultado[8]}")
        print(f"Egreso Mensual: {resultado[9]}")
        print(f"Score de Crédito: {resultado[10]}")
        print(f"ID Dirección: {resultado[11]}")
        print(f"Fecha de Registro: {resultado[12]}")
        print(f"Estado: {resultado[13]}")
    else:
        print("Cliente no encontrado.")

# Función principal de la interfaz de administrador
def interfaz_administrador():
    while True:
        print("\n--- Menú de Administrador ---")
        print("1. Agregar Cliente")
        print("2. Actualizar Cliente")
        print("3. Eliminar Cliente")
        print("4. Consultar Cliente")
        print("5. Salir")

        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            agregar_cliente()
            num_identificacion = int(input("Ingrese el número de identificación del cliente para agregar credenciales: "))
            agregar_credenciales(num_identificacion)
        elif opcion == 2:
            actualizar_cliente()
        elif opcion == 3:
            eliminar_cliente()
        elif opcion == 4:
            consultar_cliente()
        elif opcion == 5:
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción correcta.")

# Iniciar la interfaz de administrador
if __name__ == "__main__":
    interfaz_administrador()

# Cerrar la conexión cuando se termine
conexion.close()
