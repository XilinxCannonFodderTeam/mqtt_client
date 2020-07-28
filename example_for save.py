from example_for_load import led_off,led_on,config_file
from mqtt_client import device_interface as Client

if __name__ == "__main__":
    host = "52.184.15.163"
    port = 1883
    client = Client("device/1111")
    client.qos = 2
    client.add_action(led_on)
    client.add_action(led_off)
    client.run("123", host, port)
    client.add_subscribe("test")
    client.save_to_config(config_file)