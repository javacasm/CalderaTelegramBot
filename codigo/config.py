# Configuration file

# Telegram Bot Authorization Token


TELEGRAM_API_TOKEN = 'PUT:HERE:YOUR:TOKEN'

MQTT_SERVER = "192.168.1.100"
MQTT_PORT = 1883

BaseTopic_sub = 'MeteoSalon'
topicCalderaStatus = BaseTopic_sub + '/calderaStatus'
topicLedRGB = BaseTopic_sub + '/ledRGB'
topic_subCalderaAction = BaseTopic_sub + '/caldera'
topic_subInitConsola = BaseTopic_sub + '/initConsola'
topic_subTemp = BaseTopic_sub + '/Temp'
topic_subHum = BaseTopic_sub + '/Hum'
topic_subPress = BaseTopic_sub + '/Press'
topic_subData = BaseTopic_sub + '/SensorData'
topic_subConsolaStatus = BaseTopic_sub + '/consolaStatus'
topic_subBotTest = BaseTopic_sub + "/BotMQTTTest"

msg_calderaOn = 'On'
msg_calderaOff = 'Off'

CALDERA_SERVER = "192.168.1.45"

ADMIN_USER = 11111111111111111111

ALLOWED_USERS = [ADMIN_USER] # , , ]

v = '1.3'
