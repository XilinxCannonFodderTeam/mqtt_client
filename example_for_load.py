from mqtt_client import device_interface as Client
import time
LOAD_FROM_FILE = True
config_file = "./example_for_load_config.json"


client = Client("device/1111")


def led_on():
    print("1234led_on")


def led_off():
    print("1234len_off")


if __name__ == "__main__":
    host = "52.184.15.163"
    port = 1883
    test_client = Client("device/2222")
    test_client.run("234", host, port)
    if LOAD_FROM_FILE:
        client.load_from_config(config_file)
    else:
        client.add_action(led_on)
        client.add_action(led_off)
        client.run("123", host, port)
        client.add_subscribe("test")
        client.save_to_config()
    while True:
        print("on running, time is "+str(time.localtime(time.time())))
        test_client.publish("test","led_off",2)
        time.sleep(10)
