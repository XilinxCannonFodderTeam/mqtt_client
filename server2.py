import flask
import json
import time
from mqtt_client import device_interface as Server
from mqtt_client import get_topic_and_payload

server_id = "server"

server = Server(server_id)
app = flask.Flask(__name__)

@app.route("/upload")
def upload(pic_name, topic, time):
    print(pic_name)
    print(topic)
    print(time)

@app.route("./hello")
def hello():
    return "hello"

@app.route("/lock",methods=["GET","POST"])
def lock():
    for topic in server.topic["2device"]:
        server.publish(topic,"lock",2)
    return "0"
    

@app.route("/unlock",methods=["GET","POST"])
def unlock():
    for topic in server.topic["2device"]:
        server.publish(topic,"unlock",2)
    return "0"

@app.route("/test")
def lock_or_unlock():
    json_data = flask.request.form.get('data')
    json_data = json.loads(json_data)
    action = json_data[0]['name']
    if action is 'lock':
        print("get lock from mssage")
        return lock()
    elif action is 'unlock':
        print("get unlock from mssage")
        return unlock()
    print("get unkown meaage from app")
    return "1"

@app.route("./get_pic")
def get_pic():
    dir_path,filename = get_pic_path(None, None)

    return flask.send_from_directory(directory= dir_path, filename= filename)

def get_pic_url(topic, time):
    return "http://52.184.15.163:5000/get_pic"


def get_pic_path(topic, time):
    return "./","test.jpg"



@server.add_action2
def find_stranger(msg, client):
    topic, payload = get_topic_and_payload(msg)
    tmp = payload.split()
    topic_num = int(tmp[1])
    url = "http://52.184.15.163:5000/get_pic"
    localtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    payload_to_send = "find_stranger " + localtime +" " + url
    for i in range(topic_num):
        topic_to_send = tmp[i+2]
        if topic_to_send in client.topic_in_use:
            server.publish(topic_to_send, payload_to_send, server.qos)

server.add_action(lock)
server.add_action(unlock)
server.add2device_topic("todevice")
server.add2app_device_topic("toapp")



def add_device(msg):
    """
        从device发来的设备添加信息
    """
    pass

def add_app(msg):
    """
        从app发来的设备添加信息
    """
    pass

def add_rusult():
    pass

if __name__ == "__main__":
    host = "52.184.15.163"
    port = 1883
    server.run("345", host, port)
    server.add_subscribe(server.topic["2server"])
    app.run()
    loop_time = 1
    while True:
        print("loop time is ",loop_time)
        time.sleep(10)