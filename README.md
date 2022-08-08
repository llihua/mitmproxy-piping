# mitmproxy-piping
The Python mitmproxy-piping plugin passes http flows to Java callback interface via gRPC.
You should implement your own Java callback gRPC service to communicate with the Python mitmproxy-piping plugin.

参考了如下项目：  
mitmproxy-hub (https://github.com/CreditTone/mitmproxy-hub)  
mitmproxy-java (https://github.com/CreditTone/mitmproxy-java)  
重写了Python端的代码，以支持asyncio异步。

使用步骤：  

1、安装gRPC-python  
```
pip install grpcio
pip install protobuf
pip install grpcio-tools
```

2、安装mitmproxy-python  
```
pip install mitmproxy
```
通过mitmproxy访问https网站时，需要安装证书  
```
certutil -addstore root mitmproxy-ca-cert.cer
```

3、python端启动mitmproxy-piping(gRPC)  
进入项目的 resource/python/mitmproxy-piping 目录下，启动服务  
```
cd mitmproxy-piping
python server.py
```

4、Java端启动Java回调服务(gRPC)、发指令启动python端的mitmproxy，请参考java中的测试代码。  
