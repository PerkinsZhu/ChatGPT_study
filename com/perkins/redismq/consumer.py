"""
Created by PerkinsZhu on 2023/8/22 13:49
"""
"""
It reads the REDIS STREAM events
Using the xread, it gets 1 event per time (from the oldest to the last one)

Usage:
  python consumer.py
"""
from os import environ
from redis import Redis
import json

# stream_key = environ.get("STREAM", "jarless-1")
stream_key = "111"
stream_key_result = "xxx"


def connect_to_redis():
    hostname = "111"
    port = 6379
    pw = "1111"

    r = Redis(hostname, port, password=pw, retry_on_timeout=True)
    return r


def get_data(redis_connection):
    last_id = 0
    sleep_ms = 5000
    while True:  # 循环监听数据
        try:
            resp = redis_connection.xread(
                {stream_key: last_id}, count=1, block=sleep_ms
            )
            if resp:
                key, messages = resp[0]
                last_id, data = messages[0]
                print("Received: {} - {}".format(key, data))
                print(data[b'payload'].decode())
                dataDict = json.loads(data[b'payload'].decode())
                # 接收到数据之后，获取图片二维码
                dataDict['qrcode'] = "img/base64;23423423423"
                json_data = json.dumps(dataDict)
                senddata = {"payload": json_data}
                # 封装需要的格式，并发送到结果队列
                send_data(redis_connection, senddata)
        except Exception as e:
            print("ERROR REDIS CONNECTION: {}".format(e))


def send_data(redis_connection, data):
    try:
        resp = redis_connection.xadd(stream_key_result, data)
        print(resp)
    except ConnectionError as e:
        print("ERROR REDIS CONNECTION: {}".format(e))


if __name__ == "__main__":
    connection = connect_to_redis()
    get_data(connection)
