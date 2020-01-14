# MQTT utils

import paho.mqtt.client as mqtt # Import the MQTT library
import config
import utils

v = '1.2'

MQTTData = { 'initTime' : [utils.getStrDateTime() , utils.getStrDateTime()] }

bUpdateCalderaStatus = False

# Our "on message" event
def checkMQTTSubscription (client, userdata, message):
    global bUpdateCalderaStatus
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    MQTTData[topic] = [ utils.getStrDateTime() , message]
    utils.myLog('MQTT< ' +topic + ' - ' + message)
    if topic == config.topicCalderaStatus:
        bUpdateCalderaStatus = True

def on_log(client, userdata, level, buf):
    utils.myLog("mqtt-log: ",buf)

def on_connect(client, userdata, flags, rc):
    utils.myLog("Connected with result code "+str(rc))
  

def initMQTT():
    ourClient = mqtt.Client("CBT_bot_mqtt"+config.TELEGRAM_API_TOKEN) # Create a MQTT client object with this id
    ourClient.on_message = checkMQTTSubscription # Attach the messageFunction to subscription
    ourClient.on_log = on_log
    ourClient.on_connect = on_connect
    ourClient.connect(config.MQTT_SERVER, 1883) # Connect to the test MQTT broker
    utils.myLog('Conectado a MQTT broker ' + config.MQTT_SERVER)
    ourClient.subscribe(config.BaseTopic_sub+'/#') # Subscribe to the topic 
    ourClient.loop_start() # Start the MQTT client
    utils.myLog('MQTT client started')
    return ourClient

def publish(client,topic,message):
    mqttResult = client.publish(topic,message)
    # utils.myLog(str(mqttResult))
    utils.myLog('MQTT> '+topic+ ' - '+message)
    #if mqttResult.is_published():
    #       utils.myLog('Publicado')
    #else:
    #   utils.myLog('No publicado')  

def getDataDate(topic):
    return MQTTData[topic][0]
       
def getDataValue(topic):
    return MQTTData[topic][1]

def getData(topic):
    return MQTTData[topic]

def deleteTopic(topic):
    if topic in MQTTData:
        utils.myLog('Borrado de ' + topic)
        del MQTTData[topic]

def getFullData():
    answer =''
    for item in MQTTData:
        if item.startswith(config.BaseTopic_sub):
            answer += '**'+item[len(config.BaseTopic_sub)+1:]+ '** '
        else:
            answer += item + ' ' 
        answer += getDataValue(item) + '\n'
    return answer
    
def getFullDataDate():
    answer =''
    for item in MQTTData:
        if item.startswith(config.BaseTopic_sub):
            answer += '**'+item[len(config.BaseTopic_sub)+1:]+ '** '
        else:
            answer += item + ' ' 
        answer += getDataDate(item) + ' '
        answer += getDataValue(item) + '\n'
    return answer
