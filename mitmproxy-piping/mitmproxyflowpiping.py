import asyncio
import re
import sys
import grpc
import base64
import mitmpiping_pb2
import mitmpiping_pb2_grpc
import threading
from mitmproxy import proxy,options,flowfilter,ctx,http
from mitmproxy.script import concurrent

from mitmpiping_pb2 import MitmHeader, MitmRequest, MitmResponse

# mitmproxy监控流量addon，处理和java callback server的转接
class MitmproxyFlowPiping:
    # #async版本的初始化
    # @classmethod
    # async def create(cls,callbackAddr,callbackPort):
    #     self = MitmproxyFlowTransfer()
    #     self.callbackAddr = callbackAddr
    #     self.callbackPort = callbackPort
    #     #self.mitmproxyId = mitmproxyId
    #     self.includeUrlPat = r".baidu\.com" #"_print/"
    #     self.excludeUrlPat = None #r"www\."
    #     #运行时channel一直开着不关
    #     self._channel = None
    #     self._stub = None

    #     # 设置gRPC客户端存根
    #     #self.getClientStub()
    #     await self.getClientStub_aio()
    #     return self

    def __init__(self,callbackAddr,callbackPort,includeUrlPat,excludeUrlPat):
        self.callbackAddr = callbackAddr
        self.callbackPort = callbackPort
        #self.mitmproxyId = mitmproxyId
        #TODO: 传过来
        self.includeUrlPat = includeUrlPat #r".baidu\.com" #"_print/"
        self.excludeUrlPat = excludeUrlPat #None #r"www\."
        #运行时channel一直开着不关
        self._channel = None
        self._stub = None

        # 设置gRPC客户端存根
        self.getClientStub_aio()

    #使用aio channel，可以异步调用java gRPC服务
    def getClientStub_aio(self):
        if not self._stub:
            if not self.callbackAddr or not self.callbackPort:
                print("no callback info.")
                return
            #127.0.0.1:60061
            notifyServerAddr = self.callbackAddr + ":"+ str(self.callbackPort)
            #创建异步channel
            #async with grpc.aio.insecure_channel(notifyServerAddr) as channel:
            self._channel = grpc.aio.insecure_channel(notifyServerAddr)
            self._stub = mitmpiping_pb2_grpc.MitmProxyCallbackStub(self._channel)
            print("callback grpc client >>> ", notifyServerAddr)

    def createMitmRequest(self, req:http.Request):
        mitmHeaders = [MitmHeader(name=h[0],value=h[1]) for h in req.headers.fields]
        mitmRequest = MitmRequest(url=req.url, method=req.method, headers=mitmHeaders, content=req.content)
        return mitmRequest

    def createMitmResponse(self, req:http.Request, resp:http.Response):
        mitmHeaders = [MitmHeader(name=h[0],value=h[1]) for h in resp.headers.fields]
        mitmResponse = MitmResponse(request=self.createMitmRequest(req), headers=mitmHeaders, content=resp.content, statusCode=resp.status_code)
        return mitmResponse

    # 监控请求，转接到java callback gRPC server
    async def request(self, flow: http.HTTPFlow) -> None:
        req:http.Request = flow.request

        # 条件：通用包含规则+排除名单
        url = req.url
        """
        if (not self.excludeUrlPat or re.search(self.excludeUrlPat, url)) \
            and (not self.includeUrlPat or not re.search(self.includeUrlPat, url)):
            return
        """
        if self.excludeUrlPat and re.search(self.excludeUrlPat, url) \
            or self.includeUrlPat and not re.search(self.includeUrlPat, url):
            return

        # 传递flow到java回调函数，得到修改后的结果
        newRequest = await self._stub.onMitmRequest(self.createMitmRequest(req))

        # 用回调结果更新request
        req.url = newRequest.url
        req.method = newRequest.method

        # 更新header，并删除已被删除的header。也可以清空后添加全部
        newHeaderMap = {h.name:h.value for h in newRequest.headers}
        for k in req.headers.keys():
            if k in newHeaderMap:
                req.headers[k] = newHeaderMap[k]
            else:
                del req.headers[k]
        
        #修改请求体
        if newRequest.content != req.content:
            req.content = newRequest.content
    
    # 监控响应，转接到java callback gRPC server
    async def response(self, flow: http.HTTPFlow) -> None:
        req:http.Request = flow.request
        resp:http.Response = flow.response

        # 条件：通用忽略规则+监控名单
        url = req.url
        """
        if (not self.excludeUrlPat or re.search(self.excludeUrlPat, url)) \
            and (not self.includeUrlPat or not re.search(self.includeUrlPat, url)):
            return
        """
        if self.excludeUrlPat and re.search(self.excludeUrlPat, url) \
            or self.includeUrlPat and not re.search(self.includeUrlPat, url):
            return

        # 传递flow到java回调函数，得到修改后的结果
        newResponse: MitmResponse = await self._stub.onMitmResponse(self.createMitmResponse(req, resp))

        # 用回调结果更新response

        # 更新header，并删除已被删除的header。也可以清空后添加全部
        newHeaderMap = {h.name:h.value for h in newResponse.headers}
        for k in resp.headers.keys():
            if k in newHeaderMap:
                resp.headers[k] = newHeaderMap[k]
            else:
                del resp.headers[k]

        resp.content = newResponse.content
        resp.status_code = newResponse.statusCode
    
