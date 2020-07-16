# Caldera Telegram Bot - CBT


## Instalación

Instalamos el módulo base 

```
pip install python-telegram-bot --upgrade
```


Creamos nuestro bot usando @BotFather

1. Iniciamos un chat con @BotFather
2. Solicitamos la creación de un nuevo Bot con

```
/newbot
```

Ahora @BotFather nos irá pidiendo datos y damos un nombre (puede ser cualquier cosa) y un nombre de bot que tiene que terminar en 'bot' y que ha de ser distinto a todos los existentes. Supongo que es MegaHiperbot

Ahora tenemos que entrar en la versión web de telegram [**web.telegram.org**](http://web.telegram.org) en la máquina donde vamos a usarla (por ejemplo en la raspberry) y validamos nuestro inicio de sesión validándolo con el código que se nos enviará 

Ahora que tenemos acceso podemos **sustituir nuestro token del canal en el código**

Vamos a empezar por el ejemplo echoBot, que repite lo que le decimos. He modificado lévemente el codigo para que en caso de que el mensaje sea "hi" conteste con un mensaje especial usando el nombre del usuario 

[echobot](./codigo/echobot.py)

## Integrando MQTT

Usaremos MQTT para relacionarnos con los otros dispositivos

Comenzamos instalando la librería **paho** que permite interaccionar con MQTT desde python

```
pip3 install paho-mqtt
```

[Ejemplo de uso conexión con MQTT](./codigo/mqtt_paho_test.py) tomado de [aquí](https://www.digikey.com/en/maker/blogs/2019/how-to-use-mqtt-with-the-raspberry-pi)

```python
import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays

# Our "on message" event
def messageFunction (client, userdata, message):
	topic = str(message.topic)
	message = str(message.payload.decode("utf-8"))
	print(topic + message)

ourClient = mqtt.Client("makerio_mqtt") # Create a MQTT client object with this id
ourClient.connect("ServerID", 1883) # Connect to the test MQTT broker
ourClient.subscribe("AC_unit") # Subscribe to the topic AC_unit
ourClient.on_message = messageFunction # Attach the messageFunction to subscription
ourClient.loop_start() # Start the MQTT client

# Main program loop
while(1):
	ourClient.publish("AC_unit", "on") # Publish message to MQTT broker
	time.sleep(1) # Sleep for a second
```


## [Código](./codigo)


Basado en https://python-telegram-bot.org/
