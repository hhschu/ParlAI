import json
import os
import queue
import threading
import time

import websocket

WS_PORT = os.environ.get("WS_PORT", "35496")

chats = {}
contexts = {}


def on_message(ws, message):
    m = json.loads(message)
    contexts[ws.chat_id].bot.send_message(chat_id=ws.chat_id, text=m['text'])


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("Connection closed")


def _run(ws, username):
    while True:
        x = chats[ws.chat_id].get()
        if "bye" in x.lower():
            break
        data = {"id": username, "text": x}
        json_data = json.dumps(data)
        ws.send(json_data)

    del chats[ws.chat_id]
    ws.close()


def on_open(ws):
    threading.Thread(target=_run, args=(ws, ws.username)).start()


def connect_ws(chat_id, username):
    ws = websocket.WebSocketApp(
        f"ws://localhost:{WS_PORT}/websocket",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.send(f'{{"id": "{username}", "text": "ping"}}')
    time.sleep(1.5)
    ws.chat_id = chat_id
    ws.username = username
    ws.on_open = on_open
    ws.run_forever()
