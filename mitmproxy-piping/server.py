'''
Created on 2022年7月20日

@author: luolihua
'''
from concurrent import futures
import functools
#from asyncio import futures
import uuid
import base64
import time
import grpc
#from grpc.experimental import aio
import threading
import traceback
import asyncio
import logging

from mitmproxy import proxy,options,flowfilter,ctx,http
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.script import concurrent

#from mitmproxy.addons import upstream_auth

#import mitmpiping_pb2
#import mitmpiping_pb2_grpc
from mitmpiping_pb2 import MitmproxyStartRequest, ResultResponse
from mitmpiping_pb2_grpc import MitmProxyBrokerServicer, add_MitmProxyBrokerServicer_to_server
from mitmproxyflowpiping import MitmproxyFlowPiping


# Coroutines to be invoked when the event loop is shutting down.
_cleanup_coroutines = []

# 实现 proto 文件中定义的 MitmProxyBrokerServicer
# 双向服务：（作为Server）接受启动、停止mitmproxy的指令；（作为Client）传递flow到java回调函数，得到修改后的结果
class DZFMitmProxyBrokerServicer(MitmProxyBrokerServicer):
    """MitmProxyBroker负责启动mitmproxy和通知回调client端
    """
    def __init__(self):
        # mitmproxy的DumpMaster
        self.mDumpMaster = None
        #self.locker = threading.Lock()

    def startMitmproxy(self, host="0.0.0.0", port=8866, callbackAddr = None, callbackPort = None, includeUrlPat = None, excludeUrlPat = None):
        if self.mDumpMaster:
            print("Mitmproxy is already running.")
            return
        #print("Starting the Mitmproxy.", host, port)

        # see source mitmproxy/master.py for details
        # loop =  asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)

        opts = options.Options(listen_host=host, listen_port=port)
        #upstream = "http://http-dyn.abuyun.com:9020"
        #upstreamAuth = "H88QO221HIVO10MD:62769571795BDB48"
        # if upstream:
        #     opts.add_option("mode", str, "upstream:" + upstream, "")#设置上游代理
        #     print("set upstream", upstream)
        opts.add_option("ssl_insecure", bool, True, "") #不验证上游代理证书
        # pconf = proxy.config.ProxyConfig(opts)
        # mDumpMaster = DumpMaster(opts)
        # mDumpMaster.server = proxy.server.ProxyServer(pconf)
        mDumpMaster = self.mDumpMaster = DumpMaster(
            opts,
            with_termlog=False,
            with_dumper=False,
        )
        
        # if upstream and upstreamAuth: #坑啊
        #     upstreamAuthAddon:upstream_auth.UpstreamAuth = mDumpMaster.addons.get("upstreamauth")
        #     upstreamAuthAddon.auth = upstream_auth.parse_upstream_auth(upstreamAuth)
        #     print("set upstreamAuth", upstreamAuthAddon.auth)

        # addons添加回调处理类
        #await MitmproxyFlowTransfer.create(callbackAddr, callbackPort)
        mDumpMaster.addons.add(MitmproxyFlowPiping(callbackAddr, callbackPort, includeUrlPat, excludeUrlPat)) #, mitmproxyId

        # 异步启动 mitmproxy
        #await mDumpMaster.run()
        #asyncio.run(mDumpMaster.run())

        # https://docs.python.org/3/library/asyncio-dev.html#asyncio-multithreading

        #方式1.把协程转为标准任务(Task)，在当前上下文及event loop中异步执行
        #future:asyncio.futures.Future = asyncio.ensure_future(mDumpMaster.run())
        runTask = asyncio.create_task(mDumpMaster.run())
        # master.run()退出时提示Mitmproxy已关闭
        runTask.add_done_callback(lambda f: print("Mitmproxy shut down.")) #functools.partial(print, "Mitmproxy shut down.")

        #方式2.把运行mitmproxy的协程直接放到主线程的event loop去运行
        #future:futures.Future = asyncio.run_coroutine_threadsafe(mDumpMaster.run(), asyncio.get_event_loop())
        
        #方式3.在一个独立线程中异步执行函数
        #asyncio.to_thread(mDumpMaster.run)

        print("Mitmproxy started on {}:{}".format(host, port))

    async def start(self, request: MitmproxyStartRequest, context: grpc.aio.ServicerContext) -> ResultResponse:
        """启动mitmproxy的命令
        """
        host = request.host
        port = request.port
        #mitmproxyId = str(uuid.uuid4())
        callbackAddr = request.callbackAddr
        callbackPort = request.callbackPort
        # upstream = request.upstream
        # upstreamAuth = request.upstreamAuth
        includeUrlPat = request.includeUrlPat
        excludeUrlPat = request.excludeUrlPat

        #启动mitmproxy的4个参数分别是 mitmproxy服务器的IP、端口，java callback server的IP、端口："127.0.0.1", 8866, "127.0.0.1", 60061

        #没必要新建线程来启动mitmproxy
        # thead_one = threading.Thread(target=self.startMitmproxy, args=(host, port, callbackAddr, callbackPort))
        # thead_one.start()
        self.startMitmproxy(host, port, callbackAddr, callbackPort, includeUrlPat, excludeUrlPat)

        return ResultResponse(success=True, resultCode="200", message="操作成功!")

    async def stop(self, request, context: grpc.aio.ServicerContext) -> ResultResponse:
        """停止mitmproxy的命令
        """
        mDumpMaster = self.mDumpMaster
        #mitmproxyId = request.mitmproxyId
        #mDumpMaster:DumpMaster = self.tmitmproxy.get(mitmproxyId)
        try:
            #self.locker.acquire()
            if mDumpMaster:
                #del self.tmitmproxy[mitmproxyId]
                #print("del mitmproxy", mitmproxyId)
                mDumpMaster.shutdown()
        except:
            traceback.print_exc()
        finally:
           self.mDumpMaster = None

        return ResultResponse(success=True, resultCode="200", message="操作成功!")

async def serve() -> None:
    # def loop_in_thread():
    #     time.sleep(1)
    #     #loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)  #_set_running_loop
    #     # m.run_loop(loop.run_forever)
    #     l = asyncio.get_running_loop()
    #     if not l:
    #         pass
    #     time.sleep(10)

    # # loop = asyncio.new_event_loop()
    # loop = asyncio.get_event_loop()
    # m = 1
    # #await asyncio.to_thread(loop_in_thread)
    # t = threading.Thread( target=loop_in_thread, args=(loop, m) )
    # t.start()
    # time.sleep(10)
    # m = 2
    # time.sleep(10)

    # # 启动 rpc 服务
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    # mitmpiping_pb2_grpc.add_MitmProxyBrokerServicer_to_server(BothwayMitmServer(), server)
    # server.add_insecure_port('[::]:60051')
    # print("serve on 0.0.0.0:60051")
    # server.start()
    # try:
    #     while True:
    #         time.sleep(1) # one day in seconds
    # except KeyboardInterrupt:
    #     server.stop(0)

    #手工启动mitmproxy
    #startMitmProxyManually("127.0.0.1", 8866, "127.0.0.1", 60061)

    # 启动 rpc 服务
    #非aio方式：server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=40), options=[
        ('grpc.so_reuseport', 0),
        ('grpc.max_send_message_length', 100 * 1024 * 1024),
        ('grpc.max_receive_message_length', 100 * 1024 * 1024),
        ('grpc.enable_retries', 1),
    ])
    add_MitmProxyBrokerServicer_to_server(DZFMitmProxyBrokerServicer(), server)  # 加入服务
    server.add_insecure_port('[::]:60051')
    #logging.info("Starting server on %s", listen_addr)
    print("serve on 0.0.0.0:60051")
    await server.start()

    # since server.start() will not block, a sleep-loop is added to keep alive
    # try:
    #     await server.wait_for_termination()
    # except KeyboardInterrupt:
    #     await server.stop(None)

    # 支持优雅关闭，关闭时等待最多50秒。在等待期间不再接收新连接，但已有的rpc调用可继续执行
    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
        await server.stop(50)

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    #如果没有优雅关闭等要求，直接使用 asyncio.run(serve()) 即可
    #asyncio.run(serve())

    loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait([serve()]))
    # loop.close()
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
