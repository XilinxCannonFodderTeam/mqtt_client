from test_add_action import client

@client.add_action2
def test1():
    print("hello from test1")

@client.add_action2
def test2():
    print("hello from test2")

print(client.action)
