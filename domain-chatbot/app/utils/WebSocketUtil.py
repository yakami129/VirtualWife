import sys
import threading
import urllib.parse

import websocket

"""
    初始化websocket连接
"""
def init_connection(url):
    ws = websocket.WebSocketApp(url, on_open=ClientThread.on_open, on_message=ClientThread.on_message,
                                on_close=ClientThread.on_closed, on_error=ClientThread.on_error)
    # 异步监听返回结果
    client = ClientThread(ws=ws)
    client.start()
    return client


"""
    初始化websocket连接, 并附带相关参数
"""
def init_connection_with_params(url, params):
    url_prams_builder = urllib.parse.urlencode(params)
    url = url + '?' + url_prams_builder
    return init_connection(url)


"""
    发送text message
"""
def send_text_message(ws, message):
    ws.send(message)
    print("send text message: " + message)


"""
    发送binary message
"""
def send_binary_message(ws, message):
    ws.send(message, websocket.ABNF.OPCODE_BINARY)
    print("send binary message length: " + str(len(message)))


class ClientThread(threading.Thread):
    def __init__(self, ws):
        threading.Thread.__init__(self)
        self.ws = ws
        ws.is_connect = False

    def run(self):
        self.ws.run_forever()

    def return_is_connect(self):
        return self.ws.is_connect

    def on_message(ws, message):
        print("received message: " + message)
        # 该判断方式仅用作demo展示, 生产环境请使用json解析
        if "\"errorCode\":\"0\"" not in message:
            sys.exit()

    def on_open(ws):
        print("connection open")
        ws.is_connect = True

    def on_closed(ws, close_status_code, close_msg):
        if not close_status_code:
            close_status_code = 'None'
        if not close_msg:
            close_msg = 'None'
        print("connection closed, code: " + close_status_code + ", reason: " + close_msg)

    def on_error(ws, error):
        print(error)