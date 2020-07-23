import paho.mqtt.client as mqtt
import datetime
import time
import threading
from config import *
import logging




class device_interface(mqtt.Client):
    """
        mqtt.Client的继承接口

        订阅消息，使用subscribe(topic,qos)接口

        发布消息，使用publish(topic,payload,qos)接口

        连接服务器使用run(device_type,host,port)接口

        topic：主题，主题可以订阅也可以发布，对于发布，所有订阅改主题的客户端均会收到发布的消息
        payload：发布的消息，为字符串，推荐长度不超过700字节
        qos：连接的质量等级，0为最低，2为最高，由于设备性能足够，所以2是可以接受的
        host：连接的broker主机
        port：连接的broker主机mqtt端口
        device_type：定义的设备类型，暂时无用
    """

    def __init__(self, client_id="test1", clean_session=None, 
            userdata=None,protocol=4, transport="tcp"):
        """
            client_id：客户端的id号，推荐以'device名称/MAC地址'格式命名
        """
        super(device_interface,self).__init__(
            client_id=client_id, clean_session=clean_session, 
            userdata=userdata,protocol=protocol, transport=transport
        )
        self.action = {}
        self.client = None
        self.url = ""
        self.port = 1883
        self.keepalive = 60
        self.topic_in_use = []
        self.topic = {"device2server":"","server2device":[],"server2app":[]}
        self._rc_mean = ["connect success","wrong proticol","unlegal client id","server can not use","unauthorized"]
        self.use_quick_search = False
        self.qos = 0
        self.__on_running = False

    
    def add_action(self,action,action_name=None):
        """
            一个接口的添加函数，其添加客户端执行的接口集合
            当客户端接收到消息时，会调用on_message回调，此回调请不要覆盖，其依据接收的消息调用
            self.action中的函数

            当满足msg.payload.split()[0]在self.action的keys中时，会调用此key对应的action函数

            action：添加的函数，目前没有专门设定函数的输入，请先默认不使用输入
            action_name：添加的键值，以此键值作为调用的依据，如果为None就使用函数本身的名字

            action要求：
                1.目前请不要使用参数
                2.返回值可以为空，但如果返回请使用str类型
                3.有返回值时，格式约定为\"topic 实际返回值\"，topic指定你发送的目标，实际返回值为你希望发送的信息

        """
        if action:
            action_name = action_name if action_name else action.__name__
            self.action[action_name] = action

    def send_ret2topic(self,ret):
        """
            此函数负责处理返回值发送，ret格式参考addAction给出的格式

            ret:Action函数返回的值，负责给指定topic发送信息

            如果指定的topic不在使用列表当中，此函数不会发送任何消息，目前topic列表还没有自动更新
        """
        topic = ret.split()[0]
        if topic in self.topic_in_use:
            self.publish(topic,ret[len(topic):],qos=self.qos)

    def search_exct_api_by_str(self,msg):
        """
            根据订阅topic返回的信息执行函数，此函数不应该被直接调用
            msg：mqtt返回的信息，包括topic和payload

            self.quick_search_for_api：
                1.True时，对于没有加空格的调用命令，也可以实现调用
                2.False时，必须严格的按照格式发送消息
                3.此变量推荐为False
                4.不要在添加Action后再修改此值，会出错
                5.功能暂未实现，请不要调用
        """
        print(1)
        payload = str(msg.payload,encoding="utf-8")
        if msg.topic in self.topic["server2device"]:
            print(2)
            if self.use_quick_search:
                self.quick_search_for_api(msg)
            else:
                print(3)
                if payload.split()[0] in self.action.keys():
                    print(4)
                    ret = self.action[payload.split()[0]]()
            if ret:
                self.send_ret2topic(ret)


    def build_quick_search(self,action,action_name=None):
        """
            使用quick_search_for_api的必要函数，构建查找表

            不应该被外部调用
        """
        pass
    
    def quick_search_for_api(self,msg):
        """
            利用查找表，提升查找速度，针对的是不严格的接口形式

            严格实现的接口至少和search_exct_api_by_str一样快
        """
        pass

    def on_connect(self, mqttc, obj, rc):
        """
            建立和broker连接后的回调

            rc==0时表示正确的连接，请不要修改此函数
        """
        if rc == 0:
            logging.info(self._rc_mean[rc])
        elif rc in [1,2,3,4,5]:
            logging.error(self._rc_mean[rc])
            raise BaseException(self._rc_mean[rc])
        else:
            logging.error("unKown rc value with rc="+ str(rc))
            raise BaseException("Unkown rc value")
        
 
    def on_publish(self, mqttc, obj, mid):
        """
            成功发布消息后的回调
        """
        logging.info("OnPublish, mid: "+str(mid))
    
    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        """
            成功订阅后的回调
        """
        logging.info("Subscribed: "+str(mid)+" "+str(granted_qos))
    
    def on_log(self, mqttc, obj, level, string):
        logging.info("Log:"+string)
    
    def on_message(self, mqttc, obj, msg):
        """
            获得订阅消息推送的回调函数，会依据消息执行函数

            msg:订阅的topic,以及订阅的消息payload

            请不要修改此函数
        """
        curtime = datetime.datetime.now()
        strcurtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
        print("12345")
        logging.info(strcurtime + ": " + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        self.search_exct_api_by_str(msg)

    def run(self,device_type,host,port):
        """
            客户端运行，其会新建一个线程，不会造成阻塞的问题
            请运行期间调用一次，不要多次调用
            device_type：设备的类型+命名，暂未使用
            host：连接的broker服务器
            port：连接的broker服务器的mqtt服务端口
        
        """
        # 设置账号密码（如果需要的话）
        #self.client.username_pw_set(username, password=password)
        if not self.__on_running:
            self.connect(host, port, self.keepalive)
            self.loop_start()
            self.__on_running = True
        else:
            logging.error("the mqtt client is on running")





if __name__ == '__main__':
    logging.basicConfig(filename="./test.log",format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)
    t = device_interface()
    t2 = device_interface("test2")
    host = "localhost"
    port = 1883
    t.run("123",host,port)
    t2.run("234",host,port)
    t.subscribe("test",2)
    
    time.sleep(1)
    t2.publish("test","this is a test.",2)
    time.sleep(1000)