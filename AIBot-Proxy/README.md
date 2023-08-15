# AIBot-Proxy


## How to start

### websocket server port: 8765
python3 wsserver.py

### httpsrever server port: 5000
python3 proxy.py runserver --host 0.0.0.0

### curl following apis

http://0.0.0.0:5000/
http://0.0.0.0:5000/init
http://0.0.0.0:5000/state
http://0.0.0.0:5000/reset
http://0.0.0.0:5000/action
