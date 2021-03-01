# coding: utf-8

# Archivo: ultrasonico.py

# Importar las funciones necesarias de los módulos RPi,
# y time.
import RPi.GPIO as GPIO
import time
import json
import requests

# Direccion del servidor web
SERVIDOR = "http://192.168.1.132/contenedores/registrarLectura.php"
# Pin GPIO donde está conectado el activador (entrada) del sensor HC-SR04.
TRIG = 23
TRIG2 = 17
# Pin GPIO donde está conectado el eco (salida) del sensor HC-SR04.
ECHO = 24
ECHO2 = 27
# Ientificador del contenedor
IDCONTENEDOR=21 
# Indicar que se usa el esquema de numeración de pines
# de BCM (Broadcom SOC channel), es decir los números de
# pines GPIO (General-Purpose Input/Output).
GPIO.setmode(GPIO.BCM)
# Establecer que TRIG es un canal de salida.
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(TRIG2, GPIO.OUT)

# Establecer que ECHO es un canal de entrada.
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(ECHO2, GPIO.IN)

print ("Medición de distancias en progreso")

try:
    # Ciclo infinito.
    # Para terminar el programa se debe presionar Ctrl-C.
    while True:

        # Apagar el pin activador y permitir un par de
        # segundos para que se estabilice.
        GPIO.output(TRIG, GPIO.LOW)
        GPIO.output(TRIG2, GPIO.LOW)
        print ("Esperando a que el sensor se estabilice")
        time.sleep(2)

        # Prender el pin activador por 10 microsegundos
        # y después volverlo a apagar.
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG, GPIO.LOW)
        # En este momento el sensor envía 8 pulsos
        # ultrasónicos de 40kHz y coloca su salida ECHO
        # en HIGH. Se debe detectar este evento e iniciar
        # la medición del tiempo.
        print ("Iniciando eco")
        while True:
            pulso_inicio = time.time()
            if GPIO.input(ECHO) == GPIO.HIGH:
                break

        # La salida ECHO se mantendrá en HIGH hasta recibir
        # el eco reflejado por el obstáculo. En ese momento
        # el sensor pondrá ECHO en LOW y se debe terminar
        # la medición del tiempo.
        while True:
            pulso_fin = time.time()
            if GPIO.input(ECHO) == GPIO.LOW:
                break

        # La medición del tiempo es en segundos.
        duracion = pulso_fin - pulso_inicio

        # Calcular la distancia usando la velocidad del
        # sonido y considerando que la duración incluye
        # la ida y vuelta.
        distancia = (34300 * duracion) / 2

        # Imprimir resultado.
        print ("Distancia1: %.2f cm" % distancia)

        # Prender el pin activador por 10 microsegundos
        # y después volverlo a apagar.
        GPIO.output(TRIG2, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG2, GPIO.LOW)

        # En este momento el sensor envía 8 pulsos
        # ultrasónicos de 40kHz y coloca su salida ECHO
        # en HIGH. Se debe detectar este evento e iniciar
        # la medición del tiempo.
        print ("Iniciando eco")
        while True:
            pulso_inicio = time.time()
            if GPIO.input(ECHO2) == GPIO.HIGH:
                break

        # La salida ECHO se mantendrá en HIGH hasta recibir
        # el eco reflejado por el obstáculo. En ese momento
        # el sensor pondrá ECHO en LOW y se debe terminar
        # la medición del tiempo.
        while True:
            pulso_fin = time.time()
            if GPIO.input(ECHO2) == GPIO.LOW:
                break

        # La medición del tiempo es en segundos.
        duracion2 = pulso_fin - pulso_inicio

        # Calcular la distancia usando la velocidad del
        # sonido y considerando que la duración incluye
        # la ida y vuelta.
        distancia2 = (34300 * duracion2) / 2

        # Imprimir resultado.
        print ("Distancia2: %.2f cm" % distancia2)
        # Creamos el objeto o el resultado
        lectura={"idcontenedor":IDCONTENEDOR,"lecturas":[{"idsensor":"1","tipo":"distancia","lectura":distancia*10},{"idsensor":"2","tipo":"distancia","lectura":distancia2*10}]}
        # Lo pasamos al servidor
        resp=requests.post(SERVIDOR,data=json.dumps(lectura))
        print ("Respuesta del servidor: "+resp.text)
        time.sleep(30)
        
finally:
    # Reiniciar todos los canales de GPIO.
    GPIO.cleanup()