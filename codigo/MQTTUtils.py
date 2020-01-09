# MQTT utils

import paho.mqtt.client as mqtt # Import the MQTT library
import config
import utils

MQTTData = { 'initTime' : [utils.getStrDateTime() , utils.getStrDateTime()] }

# Our "on message" event
def checkMQTTSubscription (client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    MQTTData[topic] = [ utils.getStrDateTime() , message]
    utils.myLog('MQTT: '+utils.getStrDateTime() + ' ' +topic + ' - ' + message)

def on_log(client, userdata, level, buf):
    utils.myLog("mqtt-log: ",buf)

def initMQTT():
    ourClient = mqtt.Client("CBT_bot_mqtt") # Create a MQTT client object with this id
    ourClient.connect(config.MQTT_SERVER, 1883) # Connect to the test MQTT broker
    utils.myLog('Conectado a MQTT broker ' + config.MQTT_SERVER)
    ourClient.subscribe(config.BaseTopic_sub+'/#') # Subscribe to the topic 
    ourClient.on_message = checkMQTTSubscription # Attach the messageFunction to subscription
    ourClient.loop_start() # Start the MQTT client
    utils.myLog('MQTT client started')
    return ourClient

def publish(client,topic,message):
    mqttResult = client.publish(topic,message)
    utils.myLog(str(mqttResult))
    utils.myLog('Sent MQTT: '+topic+ ' '+message)
    if mqttResult.is_published():
       utils.myLog('Publicado')
    else:
       utils.myLog('No publicado')  
