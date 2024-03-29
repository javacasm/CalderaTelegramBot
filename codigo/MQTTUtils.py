# MQTT utils

import paho.mqtt.client as mqtt # Import the MQTT library
import config
import utils

v = '1.2.8'

MQTTData = { 'initTime' : [utils.getStrDateTime() , utils.getStrDateTime()] }

bUpdateCalderaStatus = False
bEsperandoRespuestaCaldera = False
bInitConsola = False

dumbTopics = (config.topicLedRGB, config.topic_subData, config.topic_subTemp,
              config.topic_subHum, config.topic_subPress, config.topic_subConsolaStatus,
              config.topic_subBotTest)

# Our 'on message' event
def checkMQTTSubscription (client, userdata, message):
    global bUpdateCalderaStatus, bEsperandoRespuestaCaldera, bInitConsola
    topic = str(message.topic)
    message = str(message.payload.decode('utf-8'))
    MQTTData[topic] = [ utils.getStrDateTime() , message]
    logmsg = 'MQTT < ' +topic + ' - ' + message
    utils.myLog(logmsg)
    if topic == config.topicCalderaStatus:
        bUpdateCalderaStatus = True
    elif topic == config.topic_subCalderaAction:
        bEsperandoRespuestaCaldera = True
    elif topic == config.topic_subInitConsola:
        bInitConsola = True
        utils.myLog('got initconsole')
    elif topic in dumbTopics:
        pass
    else:
        utils.myLog('Unknown msg: ' + logmsg)
        
def on_log(client, userdata, level, buf):
    utils.myLog('mqtt-log: ',buf)

def on_connect(client, userdata, flags, rc):
    utils.myLog('Connected with result code '+str(rc))
  

def initMQTT(clientID='CBT_bot_mqtt'+config.TELEGRAM_API_TOKEN,topic2Subscribe = config.BaseTopic_sub+'/#',mqttServer=config.MQTT_SERVER,mqttPort = config.MQTT_PORT):
    ourClient = mqtt.Client(clientID) # Create a MQTT client object with this id
    ourClient.on_message = checkMQTTSubscription # Attach the messageFunction to subscription
    ourClient.on_log = on_log
    ourClient.on_connect = on_connect
    ourClient.connect(mqttServer, mqttPort) # Connect to the test MQTT broker
    utils.myLog('Conectado a MQTT broker ' + config.MQTT_SERVER)
    if topic2Subscribe != '':
        print(topic2Subscribe)
        ourClient.subscribe(topic2Subscribe) # Subscribe to the topic 
    ourClient.loop_start() # Start the MQTT client
    utils.myLog('MQTT client started')
    return ourClient

def publish(client,topic,message):
    try:
        utils.myLog('MQTT > ' + str(topic)+ ':' + str(message.decode('utf-8')))   
        mqttResult = client.publish(topic,message)
        utils.myLog(str(mqttResult))
        """
        if mqttResult.is_published():
            utils.myLog('Publicado')
        else:
            utils.myLog('No publicado')
        """
    except KeyboardInterrupt:
        pass        
    except Exception as e:
        utils.myLog('Not Publish>' + str(e))

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
