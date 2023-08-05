import network
from .websockets import client
import json
from machine import Timer
import time
import uos
from io import BytesIO

sta_if = network.WLAN(network.STA_IF)
websocket = None

ON_REPL = False
DATA = {
    'id': 'SUPERSECRETID',
    'type': 'device',
}


# ----------------------------------------------------------------------
def register_in_server():
    """"""
    global websocket

    websocket = client.connect("ws://192.168.43.10:3200/ws")
    websocket.settimeout(2)

    data = DATA.copy()
    data['action'] = 'register'

    websocket.send(json.dumps(data))


# ----------------------------------------------------------------------
def connect_to_wifi():
    """"""
    global sta_if

    while not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('yeisonisapenguin', 'p1ngu1n0')
        time.sleep_ms(500)

    register_in_server()
    return True


# ----------------------------------------------------------------------
def run_on_exec(script):
    """"""
    compiled = compile(script + '\n', '<string>', 'exec')
    exec(compiled, locals(), locals())


# ----------------------------------------------------------------------
def espresso_repl(t):
    """"""
    global sta_if, websocket, ON_REPL, timer

    if ON_REPL:
        return

    ON_REPL = True
    timer.deinit()
    uos.chdir('/')

    if not sta_if.isconnected():
        connect_to_wifi()

    try:
        script = websocket.recv()
    except:
        script = None
        pass

    if script:

        espreso_stdout = BytesIO()
        uos.dupterm(espreso_stdout)

        try:
            run_on_exec(script)
            # run_on_file(script)

            out = espreso_stdout.getvalue().decode()
        except Exception as e:
            out = str(e)

        data = DATA.copy()
        data['action'] = 'stream'
        data['data'] = out

        websocket.send(json.dumps(data))

    ON_REPL = False
    timer.init(period=2000, mode=Timer.PERIODIC, callback=espresso_repl)


if connect_to_wifi():
    timer = Timer(-1)
    timer.init(period=2000, mode=Timer.PERIODIC, callback=espresso_repl)
