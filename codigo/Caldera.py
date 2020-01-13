
import config
import httpUtils
import MQTTUtils

v = '1.1'

URL_caldera = 'http://' + config.CALDERA_SERVER 
MQTT_caldera = config.BaseTopic_sub + '/caldera'
MQTT_caldera_Status = config.BaseTopic_sub + '/calderaStatus'

def calderaWebOn():
    urlOn = URL_caldera + '/?rele=on'
    # print(urlOn)
    response = httpUtils.get_url(urlOn)
    # print(response)
    if 'Calefaccion: <strong>ON' in response:
        return 'ON'
	
def calderaMQTTOn(client):
    MQTTUtils.publish(client, MQTT_caldera, 'On')
	
def calderaWebOff():
    urlOff = URL_caldera + '/?rele=off'
    # print(urlOff)
    response = httpUtils.get_url(urlOff)
    # print(response)
    if 'Calefaccion: <strong>OFF' in response:
        return 'OFF'
	
def calderaMQTTOff(client):
       MQTTUtils.publish(client, MQTT_caldera,'Off')
