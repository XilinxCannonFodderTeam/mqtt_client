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
    # print("current time       :{}".format(time.localtime(time.time())))
    print("get mssage payload :{}".format(str(msg.payload,encoding="utf-8")))
    print("get client arg type:{}".format(type(client)))

def time_test(msg):
    print("time_test:success,call by mqtt client")
    payload = str(msg.payload,encoding="utf-8")
    time1 = float(payload.split()[1])
    time2 = time.perf_counter()
    print("time use is :{}".format((time2-time1)*1000))


if __name__ == "__main__":
    topic = "test"
    clinet_id = "test1"
    host = "52.184.15.163"
    port = 1883
    t = Client(clinet_id)
    t.add2device_topic(topic)
    t.add_action(print_msg)
    t.add_action(print_msg2)
    t.add_action(print_msg3)
    t.add_action(time_test)
    # print(t.action_load)
    t.save_to_config()
    # print(t.action.keys())
    # print(type(t.action.keys()))
    # print("print_msg" in t.action.keys())
    # t.run("123",host,port)
    # t.subscribe("test",2)
    # print("set down")
    # t2 = Client("test3")
    # t2.run("234",host,port)
    # # for i in range(100):
    # #     t2.publish("test","time_test "+str(time.perf_counter()),2)
    # #     time.sleep(1)
    # time.sleep(1000)
    
