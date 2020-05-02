import os
import json
import queue
import threading
import time
import uuid

import websocket

WS_PORT = os.environ.get("WS_PORT", "34596")

chats = {}
contexts = {}

def _get_rand_id():
    return str(uuid.uuid4())


def on_message(ws, message):
    m = json.loads(message)
    contexts[ws.chat_id].bot.send_message(chat_id=ws.chat_id, text=m['text'])


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("Connection closed")


def _run(ws, id):
    ws.send(f'{{"id": "{id}", "text": "ping"}}')
    chats[ws.chat_id] = queue.Queue()
    while True:
        x = chats[ws.chat_id].get()
        if "bye" in x.lower():
            break
        data = {"id": id, "text": x}
        json_data = json.dumps(data)
        ws.send(json_data)

    del chats[ws.chat_id]
    ws.close()


def on_open(ws):
    id = _get_rand_id()
    threading.Thread(target=_run, args=(ws, id)).start()


def connect_ws(chat_id):
    ws = websocket.WebSocketApp(
        f"ws://localhost:{WS_PORT}/websocket",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.chat_id = chat_id
    ws.on_open = on_open
    ws.run_forever()
