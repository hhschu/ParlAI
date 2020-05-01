import os
import json
import queue
import threading
import time
import uuid

import websocket

q = queue.Queue()

WS_PORT = os.environ.get("WS_PORT", "34596")


def _get_rand_id():
    return str(uuid.uuid4())


def on_message(ws, message):
    m = json.loads(message)
    q.put(m)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("Connection closed")


def _run(ws, id):
    ws.send(f'{{"id": "{id}", "text": "ping"}}')
    while True:
        x = input("Me: ")
        data = {"id": id, "text": x}
        json_data = json.dumps(data)
        ws.send(json_data)
        try:
            incoming_message = q.get(timeout=10)
        except queue.Empty:
            pass
        else:
            print("Bot: " + incoming_message['text'])
        if x == "bye":
            break
    ws.close()


def on_open(ws):
    id = _get_rand_id()
    threading.Thread(target=_run, args=(ws, id)).start()


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        f"ws://localhost:{WS_PORT}/websocket",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
