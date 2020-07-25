from mqtt_client import device_interface as Client
import time

def print_msg():
    print("print_msg:success,call by mqtt client")
    print("*123*")

def print_msg2(msg):
    print("print_msg2:success,call by mqtt client")
    print(type(msg))
    print(msg)

def print_msg3(msg,client):
    print("print_msg3:success,call by mqtt client")
    print(msg)
    print("get mssage topic   :{}".format(msg.topic))
    print("get mssage payload :{}".format(str(msg.payload,encoding="utf-8")))
    print("get client arg type:{}".format(type(client)))


if __name__ == "__main__":
    topic = "test"
    clinet_id = "test1"
    host = "localhost"
    port = 1883
    t = Client(clinet_id)
    t.add2device_topic(topic)
    t.add_action(print_msg)
    t.add_action(print_msg2)
    t.add_action(print_msg3)
    # print(t.action.keys())
    # print(type(t.action.keys()))
    # print("print_msg" in t.action.keys())
    t.run("123",host,port)
    t.subscribe("test",2)
    print("set down")
    time.sleep(1000)
    
