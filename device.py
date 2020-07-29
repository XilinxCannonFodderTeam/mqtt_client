from mqtt_client import _load_python_file,_save_input_py_file
from mqtt_client import device_interface as Client
import time
import requests

def get_topic_and_payload(msg):
    if not msg:
        return
    topic = msg.topic
    payload = str(msg.payload, encoding="utf-8")
    return topic,payload

def print_msg(msg, client):
    topic,payload = get_topic_and_payload(msg)
    print(topic)
    print(payload)

def find_stranger(topics):
    if isinstance(topics, str):
        payload = "find_stranger 1 "+ topics + " "
    else: 
        payload = "find_stranger " + str(len(topics)) +" " + " ".join(topics) + " "
    localtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    payload = payload + localtime
    # print(payload)
    client.publish(client.topic["2server"], payload, client.qos)
    
def upload_pic(frame):
    pass



device_id = "device"
device_topic_sub = "todevice"
client = Client(device_id)
client.add_subscribe(device_topic_sub)
client.add_action(_load_python_file)
client.add_action(_save_input_py_file)


find_stranger(["123","234"])
find_stranger("123")
