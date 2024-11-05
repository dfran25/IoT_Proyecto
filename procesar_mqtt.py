import paho.mqtt.client as mqtt
import psycopg2  # Para la conexión a la base de datos PostgreSQL
import json
from dotenv import load_dotenv
import os
import time

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración del broker MQTT
broker = "test.mosquitto.org"
port = 1883
topic = "sensor/temperatura_humedad_simulado"

# Configuración de la base de datos en Azure usando variables de entorno
server = os.getenv("AZURE_DB_SERVER")
database = os.getenv("AZURE_DB_NAME")
username = os.getenv("AZURE_DB_USER")
password = os.getenv("AZURE_DB_PASSWORD")

# Conectar a la base de datos
def conectar_bd():
    try:
        conn = psycopg2.connect(
            host=server,
            dbname=database,
            user=username,
            password=password,
            port=5432
        )
        print("Conectado a la base de datos en Azure.")
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Guardar datos en la base de datos
def almacenar_datos_bd(conn, temperatura, humedad):
    try:
        cursor = conn.cursor()
        # Cambiar los nombres en la consulta para que coincidan con la base de datos
        query = "INSERT INTO datos_sensor (temperature, humidity, fecha) VALUES (%s, %s, NOW())"
        cursor.execute(query, (temperatura, humedad))
        conn.commit()
        print(f"Datos guardados en la base de datos: Temperatura={temperatura}, Humedad={humedad}")
    except psycopg2.Error as e:
        print(f"Error al guardar datos en la base de datos: {e}")

# Callback cuando se conecta al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT para procesar datos.")
        client.subscribe(topic)
    else:
        print(f"Error de conexión con código {rc}")

# Callback cuando se recibe un mensaje
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        datos = json.loads(payload)
        temperatura = datos.get("temperatura")
        humedad = datos.get("humedad")
        print(f"Recibido: Temperatura={temperatura}, Humedad={humedad}")
        if conexion_bd:
            almacenar_datos_bd(conexion_bd, temperatura, humedad)
        else:
            print("Conexión a la base de datos no disponible, no se guardaron los datos.")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el mensaje: {e}")
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")

# Crear cliente MQTT
cliente = mqtt.Client()
cliente.on_connect = on_connect
cliente.on_message = on_message

# Conectar al broker
try:
    cliente.connect(broker, port, 60)
except Exception as e:
    print(f"Error al conectar al broker MQTT: {e}")
    exit()

# Conectar a la base de datos
conexion_bd = conectar_bd()

# Iniciar el loop
cliente.loop_start()

try:
    while True:
        time.sleep(5)  # Mantener el script corriendo con un retraso
except KeyboardInterrupt:
    print("Deteniendo el procesamiento de MQTT...")
finally:
    cliente.loop_stop()
    cliente.disconnect()
    if conexion_bd:
        conexion_bd.close()
        print("Conexión a la base de datos cerrada.")
