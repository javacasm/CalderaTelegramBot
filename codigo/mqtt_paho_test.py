import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays
import datetime

# Our "on message" event
def messageFunction (client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    print(str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f "))+ topic + message)

ourClient = mqtt.Client("makerio_mqtt") # Create a MQTT client object with this id
ourClient.connect("192.168.1.200", 1883) # Connect to the test MQTT broker
ourClient.subscribe("MeteoSalon/#") # Subscribe to the topic AC_unit
ourClient.on_message = messageFunction # Attach the messageFunction to subscription
ourClient.loop_start() # Start the MQTT client

# Main program loop
last_pub = int(round(time.time() * 1000))
while(1):
    now = int(round(time.time() * 1000))
    if (now - last_pub) > 30000: # 30 segundos
        ourClient.publish("MeteoSalon/Test", "Just Testing") # Publish message to MQTT broker
        last_pub = now
    time.sleep(0.1) # Sleep for a second

