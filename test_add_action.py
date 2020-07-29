from mqtt_client import device_interface as Client
from mqtt_client import _load_python_file

client = Client("12333")



if __name__ == "__main__":
    paths = "C:\\Users\\sl1729\\Documents\\Xilinx_summer_school_project\\face_s_server_project\\test_add_action2.py"
    print(type(client))
    client.__init__("12333")
    print(dir(client))
    module = client.load_python_module(paths)
    client2 = getattr(module, "client")
    print(client2 == client)

    # for func in dir(module):
    #     if func.startswith("_"):
    #         continue
    #     func = getattr(module, func)
    #     if callable(func):
    #         func()
    print(client.action)