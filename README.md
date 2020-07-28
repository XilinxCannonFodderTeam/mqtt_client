# 项目说明
这个是对paho_mqtt的一个简单的包装类，主要是为了方便的进行开发。
主要添加了功能有两个，如下：

1. 增加配置的保存与导入
2. 增加函数的回调添加，允许对`func_name msg`格式的payload进行响应，其会查找函数表，调用func_name对应的函数

# 使用案例
## 配置的保存
参考`example_for_save.py`的案例，运行其，会保存配置文件到`example_for_load_config.json`文件下。

这里的客户端会自动设定自己的id为device/1111，然后订阅名为`test`的topic，同时调用led_on和led_off的函数，注意此函数并没有真的点led，只是打印信息
## 配置的导入
参考`example_for_load.py`的案例，运行其，会使用配置文件`example_for_load_config.json`。

同时其会新建一个测试的客户端，其每隔10s对led_off进行调用

# 计划新增功能
考虑进一步添加的功能
1. 允许上传python函数，然后自动添加到回调的支持当中
2. 设备和app对的添加，而非手工加入
3. 支持自动重启，当出现错误推出时直接重启
4. 对回调的异步调用，使用线程池进行优化