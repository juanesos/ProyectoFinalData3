import mysql.connector
from datetime import datetime

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root", 
    password="root",
    database="proyecto_final_database"
)

# Función para registrar un nuevo usuario
def registrar_usuario():
    cursor = conexion.cursor()

    print("\n--- Registro de nuevo usuario ---")
    
    # Información de dirección
    print("Ingrese los datos de su residencia:")
    pais = input("País: ")
    departamento = input("Departamento: ")
    ciudad = input("Ciudad: ")
    barrio = input("Barrio: ")
    nomenclatura = input("Nomenclatura de dirección: ")
    descripcion_direccion = input("Descripción adicional de la dirección: ")
    
    # Insertar en la tabla DIRECCION
    query_direccion = """
    INSERT INTO DIRECCION (PAIS, DEPARTAMENTO, CIUDAD, BARRIO, NOMENCLATURA, DESCRIPCION)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query_direccion, (pais, departamento, ciudad, barrio, nomenclatura, descripcion_direccion))
    conexion.commit()

    # Obtener el ID_DIRECCION recién insertado
    id_direccion = cursor.lastrowid
    
    # Información del cliente
    num_identificacion = int(input("Número de identificación: "))
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    genero = input("Género (M/F): ")
    edad = int(input("Edad: "))
    telefono = input("Teléfono: ")
    email = input("Correo electrónico: ")
    ocupacion = input("Ocupación: ")
    ingreso_mensual = float(input("Ingreso mensual: "))
    egreso_mensual = float(input("Egreso mensual: "))
    score = int(input("Score financiero: "))

    # Insertar en la tabla CLIENTE
    query_cliente = """
    INSERT INTO CLIENTE (NUM_IDENTIFICACION, NOMBRE, APELLIDO, GENERO, EDAD, TELEFONO, EMAIL, OCUPACION, INGRESO_MENSUAL, EGRESO_MENSUAL, SCORE, ID_DIRECCION)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query_cliente, (num_identificacion, nombre, apellido, genero, edad, telefono, email, ocupacion, ingreso_mensual, egreso_mensual, score, id_direccion))
    conexion.commit()

    print("Cliente registrado exitosamente.")

    # Registro de credenciales
    usuario = input("Cree su nombre de usuario: ")
    contraseña = input("Cree su contraseña: ")
    
    # Insertar en la tabla CREDENCIALES
    query_credenciales = """
    INSERT INTO CREDENCIALES (NUM_IDENTIFICACION, USUARIO, CONTRASEÑA, ULTIMA_CONEXION)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query_credenciales, (num_identificacion, usuario, contraseña, datetime.now()))
    conexion.commit()

    print("Usuario y credenciales creados exitosamente.\n")

# Función para consultar cuentas bancarias
def consultar_cuentas_bancarias(num_identificacion):
    cursor = conexion.cursor()

    print("\n--- Consulta de Cuentas Bancarias ---")
    
    query = """
    SELECT CC.NUMERO_OBLIGACION, CB.TIPO_CUENTA, CC.SALDO, CC.CUPO_SOBREGIRO, CC.FECHA_APERTURA, CC.TARJETA_FISICA, CC.TARJETA_VIRTUAL
    FROM CLIENTE_CUENTA CC
    JOIN CUENTAS_BANCARIAS CB ON CC.ID_CUENTA = CB.ID_CUENTA
    WHERE CC.NUM_IDENTIFICACION = %s
    """
    cursor.execute(query, (num_identificacion,))
    cuentas = cursor.fetchall()

    if cuentas:
        for cuenta in cuentas:
            print(f"Obligación: {cuenta[0]}, Tipo de cuenta: {cuenta[1]}, Saldo: {cuenta[2]}, Sobregiro: {cuenta[3]}, Fecha de apertura: {cuenta[4]}")
            print(f"Tarjeta física: {'Sí' if cuenta[5] else 'No'}, Tarjeta virtual: {'Sí' if cuenta[6] else 'No'}\n")
    else:
        print("No se encontraron cuentas bancarias.")

# Función para consultar tarjetas de crédito
def consultar_tarjetas_credito(num_identificacion):
    cursor = conexion.cursor()

    print("\n--- Consulta de Tarjetas de Crédito ---")
    
    query = """
    SELECT CT.NUMERO_OBLIGACION, TC.FRANQUICIA, CT.CUPO, CT.CUPO_DISPONIBLE, CT.FECHA_APERTURA, CT.FECHA_CORTE, CT.FECHA_PAGO, CT.ESTADO
    FROM CLIENTE_TARJETA_CREDITO CT
    JOIN TARJETAS_CREDITO TC ON CT.ID_TARJETA_CREDITO = TC.ID_TARJETA_CREDITO
    WHERE CT.NUM_IDENTIFICACION = %s
    """
    cursor.execute(query, (num_identificacion,))
    tarjetas = cursor.fetchall()

    if tarjetas:
        for tarjeta in tarjetas:
            print(f"Obligación: {tarjeta[0]}, Franquicia: {tarjeta[1]}, Cupo: {tarjeta[2]}, Cupo Disponible: {tarjeta[3]}")
            print(f"Fecha de Apertura: {tarjeta[4]}, Fecha de Corte: {tarjeta[5]}, Fecha de Pago: {tarjeta[6]}, Estado: {tarjeta[7]}\n")
    else:
        print("No se encontraron tarjetas de crédito.")

# Función para realizar transferencias o pagos
def realizar_transferencia_pago(num_identificacion):
    cursor = conexion.cursor()

    print("\n--- Realizar Transferencia o Pago ---")
    print("1. Transferencia entre cuentas bancarias")
    print("2. Pago de tarjeta de crédito")
    
    opcion = int(input("Seleccione una opción: "))

    if opcion == 1:
        # Transferencia entre cuentas bancarias
        print("\n--- Transferencia entre cuentas bancarias ---")
        id_cuenta_origen = int(input("Ingrese el ID de la cuenta de origen: "))
        id_cuenta_destino = int(input("Ingrese el ID de la cuenta de destino: "))
        monto = float(input("Ingrese el monto a transferir: "))

        # Verificar saldo de la cuenta de origen
        query_saldo_origen = """
            SELECT SALDO FROM CLIENTE_CUENTA 
            WHERE ID_CUENTA = %s AND NUM_IDENTIFICACION = %s
        """
        cursor.execute(query_saldo_origen, (id_cuenta_origen, num_identificacion))
        resultado_origen = cursor.fetchone()

        if resultado_origen:
            saldo_origen = resultado_origen[0]

            if saldo_origen >= monto:
                # Realizar la transferencia
                query_transferir_origen = """
                    UPDATE CLIENTE_CUENTA 
                    SET SALDO = SALDO - %s 
                    WHERE ID_CUENTA = %s AND NUM_IDENTIFICACION = %s
                """
                query_transferir_destino = """
                    UPDATE CLIENTE_CUENTA 
                    SET SALDO = SALDO + %s 
                    WHERE ID_CUENTA = %s
                """
                cursor.execute(query_transferir_origen, (monto, id_cuenta_origen, num_identificacion))
                cursor.execute(query_transferir_destino, (monto, id_cuenta_destino))
                conexion.commit()

                # Registrar la transacción en TRANSACCIONES_CUENTAS_BANCARIAS
                query_transaccion = """
                    INSERT INTO TRANSACCIONES_CUENTAS_BANCARIAS (TIPO_TRANSACCION, NUMERO_OBLIGACION, NUMERO_DESTINO, MONTO, FECHA_TRANSACCION, DESCRIPCION)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                descripcion = "Transferencia entre cuentas"
                cursor.execute(query_transaccion, ('Transferencia', id_cuenta_origen, id_cuenta_destino, monto, datetime.now(), descripcion))
                conexion.commit()

                print("Transferencia realizada exitosamente.")
            else:
                print("Saldo insuficiente para realizar la transferencia.")
        else:
            print("Cuenta de origen no encontrada o no pertenece al usuario.")

    elif opcion == 2:
        # Pago de tarjeta de crédito
        print("\n--- Pago de tarjeta de crédito ---")
        id_tarjeta = int(input("Ingrese el ID de la tarjeta de crédito: "))
        monto = float(input("Ingrese el monto a pagar: "))

        # Verificar saldo de la cuenta del usuario
        query_cupo_disponible = """
            SELECT CUPO, CUPO_DISPONIBLE FROM CLIENTE_TARJETA_CREDITO 
            WHERE ID_TARJETA_CREDITO = %s AND NUM_IDENTIFICACION = %s
        """
        cursor.execute(query_cupo_disponible, (id_tarjeta, num_identificacion))
        resultado_tarjeta = cursor.fetchone()
        if resultado_tarjeta:
            cupo_total, cupo_disponible = resultado_tarjeta

            if monto <= (cupo_total - cupo_disponible):
                # Realizar el pago
                query_pago = """
                    UPDATE CLIENTE_TARJETA_CREDITO 
                    SET CUPO_DISPONIBLE = CUPO_DISPONIBLE + %s 
                    WHERE ID_TARJETA_CREDITO = %s AND NUM_IDENTIFICACION = %s
                """
                cursor.execute(query_pago, (monto, id_tarjeta, num_identificacion))
                conexion.commit()

                # Registrar la transacción en TRANSACCIONES_CUENTAS_TARJETA_CREDITO
                query_transaccion = """
                    INSERT INTO TRANSACCIONES_CUENTAS_TARJETA_CREDITO (TIPO_TRANSACCION, NUMERO_OBLIGACION, MONTO, FECHA_TRANSACCION, DESCRIPCION)
                    VALUES (%s, %s, %s, %s, %s)
                """
                descripcion = "Pago de tarjeta de crédito"
                cursor.execute(query_transaccion, ('Pago', id_tarjeta, monto, datetime.now(), descripcion))
                conexion.commit()

                print("Pago realizado exitosamente.")
            else:
                print("El monto excede la deuda actual de la tarjeta.")
        else:
            print("Tarjeta de crédito no encontrada o no pertenece al usuario.")

    else:
        print("Opción no válida.")

# Función para iniciar sesión
def iniciar_sesion():
    cursor = conexion.cursor()

    print("\n--- Inicio de Sesión ---")
    usuario = input("Ingrese su usuario: ")
    contraseña = input("Ingrese su contraseña: ")

    query = "SELECT NUM_IDENTIFICACION FROM CREDENCIALES WHERE USUARIO = %s AND CONTRASEÑA = %s"
    cursor.execute(query, (usuario, contraseña))
    resultado = cursor.fetchone()

    if resultado:
        num_identificacion = resultado[0]
        print("Inicio de sesión exitoso.")

        # Actualizar la última conexión
        query_ultima_conexion = "UPDATE CREDENCIALES SET ULTIMA_CONEXION = %s WHERE USUARIO = %s"
        cursor.execute(query_ultima_conexion, (datetime.now(), usuario))
        conexion.commit()

        return num_identificacion
    else:
        print("Usuario o contraseña incorrectos.")
        return None

# Función principal de la interfaz de usuario
def interfaz_usuario():
    while True:
        print("\n--- Menú de Usuario ---")
        print("1. Registrarse")
        print("2. Consultar cuentas bancarias")
        print("3. Consultar tarjetas de crédito")
        print("4. Realizar transferencia o pago")
        print("5. Salir")
        
        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            registrar_usuario()
        elif opcion == 2:
            num_identificacion = iniciar_sesion()
            if num_identificacion:
                consultar_cuentas_bancarias(num_identificacion)
        elif opcion == 3:
            num_identificacion = iniciar_sesion()
            if num_identificacion:
                consultar_tarjetas_credito(num_identificacion)
        elif opcion == 4:
            num_identificacion = iniciar_sesion()
            if num_identificacion:
                realizar_transferencia_pago(num_identificacion)
        elif opcion == 5:
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción correcta.")

# Iniciar la interfaz de usuario
if __name__ == "__main__":
    interfaz_usuario()

# Cerrar la conexión cuando se termine
conexion.close()
