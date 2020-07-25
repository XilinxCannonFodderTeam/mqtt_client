from mqtt_client import device_interface as Client
import flask
import json

host = ""
port = 1883
app = flask.Flask(__name__)
client = Client("server")
client.run("server",host,port)

msg_queen = {}
def add_to_queen(msg, client):
    topic = str(msg.topic,encoding="utf-8")
    payload = str(msg.payload,encoding="utf-8")
    if topic in msg_queen.keys():
        msg_queen[topic].append(payload)
    else:
        msg_queen[topic] = [payload]
    print("**************************")
    print("get topic  :"+topic)
    print("get payload:"+payload)
    print("**************************")


client.default_func = add_to_queen

@app.route("/lock",methods=["GET","POST"])
def lock():
    for topic in client.topic["2device"]:
        client.publish(topic,"lock",2)
    return 0
    

@app.route("/unlock",methods=["GET","POST"])
def unlock():
    for topic in client.topic["2device"]:
        client.publish(topic,"lock",2)
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

app.run()