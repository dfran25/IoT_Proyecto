import paho.mqtt.client as mqtt
import time
import random
import json

# Configuración del broker MQTT
broker = "test.mosquitto.org"
port = 1883
topic = "sensor/temperatura_humedad_simulado"

# Callback cuando se conecta al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT!")
    else:
        print(f"Error de conexión con código {rc}")

# Crear cliente MQTT
cliente = mqtt.Client()
cliente.on_connect = on_connect
cliente.connect(broker, port, 60)
cliente.loop_start()

# Simular datos de temperatura y humedad
try:
    while True:
        temperatura = round(random.uniform(20.0, 30.0), 2)
        humedad = round(random.uniform(40.0, 60.0), 2)
        datos = {
            "temperatura": temperatura,
            "humedad": humedad
        }
        mensaje = json.dumps(datos)
        cliente.publish(topic, mensaje)
        print(f"Datos enviados: {mensaje}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Deteniendo la simulación...")
finally:
    cliente.loop_stop()
    cliente.disconnect()