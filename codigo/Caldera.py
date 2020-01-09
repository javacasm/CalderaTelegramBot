
import config
import httpUtils

URL_caldera = 'http://' + config.CALDERA_SERVER 

def calderaOn():
    urlOn = URL_caldera + '/?rele=on'
    # print(urlOn)
    response = httpUtils.get_url(urlOn)
    # print(response)
    if 'Calefaccion: <strong>ON' in response:
        return 'ON'
	
def calderaOff():
    urlOff = URL_caldera + '/?rele=off'
    # print(urlOff)
    response = httpUtils.get_url(urlOff)
    # print(response)
    if 'Calefaccion: <strong>OFF' in response:
        return 'OFF'
