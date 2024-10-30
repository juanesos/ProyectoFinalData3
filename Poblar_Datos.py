import mysql.connector
import random
from faker import Faker

fake = Faker()

# Conexión a la base de datos
conexion = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    port='3306',
    database='proyecto_final_database'
)

cursor = conexion.cursor()

# Obtener IDs de clientes existentes
cursor.execute("SELECT NUM_IDENTIFICACION FROM CLIENTE")
clientes = cursor.fetchall()

# Obtener IDs de cuentas bancarias existentes
cursor.execute("SELECT ID_CUENTA FROM CUENTAS_BANCARIAS")
cuentas_bancarias = cursor.fetchall()

# Obtener IDs de tarjetas de crédito existentes
cursor.execute("SELECT ID_TARJETA_CREDITO FROM TARJETAS_CREDITO")
tarjetas_credito = cursor.fetchall()

# Limitar el número máximo de productos por cliente (cuentas + tarjetas)
for cliente in clientes:
    num_identificacion = cliente[0]
    
    # Número de productos a asignar al cliente (entre 1 y 3)
    num_productos = random.randint(1, 3)

    # Generar productos para el cliente
    productos_asignados = 0
    while productos_asignados < num_productos:
        # Decidir aleatoriamente si se asigna una cuenta o una tarjeta
        if productos_asignados < 2 and random.choice([True, False]):
            # Asignar una cuenta bancaria
            id_cuenta = random.choice(cuentas_bancarias)[0]
            saldo = round(random.uniform(5000, 20000), 2)
            cupo_sobregiro = None if random.choice([True, False]) else round(random.uniform(500, 2000), 2)
            
            query_cliente_cuenta = """
            INSERT INTO CLIENTE_CUENTA (NUMERO_OBLIGACION, ID_CUENTA, NUM_IDENTIFICACION, SALDO, CUPO_SOBREGIRO, FECHA_APERTURA, TARJETA_FISICA, TARJETA_VIRTUAL, FRANQUICIA)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_cliente_cuenta, (
                random.randint(1000, 9999),  # NUMERO_OBLIGACION
                id_cuenta,
                num_identificacion,
                saldo,
                cupo_sobregiro,
                fake.date_this_decade(),
                random.choice([True, False]),
                random.choice([True, False]),
                random.choice(['Visa', 'MasterCard', None])
            ))

            productos_asignados += 1
        else:
            # Asignar una tarjeta de crédito
            id_tarjeta_credito = random.choice(tarjetas_credito)[0]
            cupo = round(random.uniform(5000, 20000), 2)
            cupo_disponible = round(random.uniform(1000, cupo), 2)
            
            query_cliente_tarjeta = """
            INSERT INTO CLIENTE_TARJETA_CREDITO (NUMERO_OBLIGACION, ID_TARJETA_CREDITO, NUM_IDENTIFICACION, CUPO, CUPO_DISPONIBLE, FECHA_APERTURA, CUOTAS, FECHA_CORTE, FECHA_PAGO, ESTADO)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_cliente_tarjeta, (
                random.randint(1000, 9999),  # NUMERO_OBLIGACION
                id_tarjeta_credito,
                num_identificacion,
                cupo,
                cupo_disponible,
                fake.date_this_decade(),
                random.randint(1, 36),  # Cuotas
                fake.date_this_year(),
                fake.date_this_year(),
                'Activo'
            ))

            productos_asignados += 1

conexion.commit()
cursor.close()
conexion.close()
