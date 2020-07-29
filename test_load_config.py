from mqtt_client import device_interface as Client

t = Client("ccc")
t.load_from_config()
t.save_to_config("./test_config.json")
print(t.action)