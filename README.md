# Caldera Telegram Bot - CBT


## Instalación

Instalamos el módulo base 

```
pip install python-telegram-bot --upgrade
```


Creamos nuestro bot usando @BotFather

1. Iniciamos un chat con @BotFather
2. Solicitamos la creación de un nuebo Bot con

```
/newbot
```

Ahora @BotFather nos irá pidiendo datos y damos un nombre (puede ser cualquier cosa) y un nombre de bot que tiene que terminar en 'bot' y que ha de ser distinto a todos los existentes. Supongo que es MegaHiperbot

Ahora tenemos que entrar en la versión web de telegram [**web.telegram.org**](http://web.telegram.org) en la máquina donde vamos a usarla (por ejemplo en la raspberry) y validamos nuestro inicio de sesión validándolo con el código que se nos enviará 

Ahora que tenemos acceso podemos sustituir el token en el código

Vamos a empezar por el ejemplo echoBot, que repite lo que le decimos. He modificado lévemente el codigo para que en caso de que el mensaje sea "hi" conteste con un mensaje especial usando el nombre del usuario 

[echobot](./codigo/)

## [Código](./codigo)


Basado en https://python-telegram-bot.org/