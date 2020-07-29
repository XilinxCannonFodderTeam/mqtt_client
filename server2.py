import flask
import json
from mqtt_client import device_interface as Server


server_id = "server"

server = Server(server_id)
app = flask.Flask(__name__)

@app.route("/upload")
def upload(pic_name, topic, time):
    print(pic_name)
    print(topic)
    print(time)

@app.route("/lock",methods=["GET","POST"])
def lock():
    for topic in server.topic["2device"]:
        server.publish(topic,"lock",2)
    return 0
    

@app.route("/unlock",methods=["GET","POST"])
def unlock():
    for topic in server.topic["2device"]:
        server.publish(topic,"lock",2)
    return 0

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
    return 1

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