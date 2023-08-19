# AIBot-Proxy


## How to start

### websocket server port: 8765

python3 wsserver.py

### httpsrever server port: 5000

python3 proxy.py runserver --host 0.0.0.0

### curl following apis

* http://0.0.0.0:5000/
* http://0.0.0.0:5000/init
* http://0.0.0.0:5000/state
* http://0.0.0.0:5000/reset
* http://0.0.0.0:5000/action

### how to config

```
[config]
# ws server location
remoteUri = ws://localhost:8765
# flask server key
secretKey = benxiwan
# flask server listen to 
listen = 0.0.0.0
port = 5000
# type of wss client payload: 0: str 1: bytes
binary = 0


[route]
init = []
action = []
reset = []
state = [1017,4096,4993]
```


