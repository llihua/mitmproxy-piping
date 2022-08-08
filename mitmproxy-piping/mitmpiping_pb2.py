# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mitmpiping.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10mitmpiping.proto\x12\nmitmpiping\x1a\x1bgoogle/protobuf/empty.proto\"\x8d\x01\n\x15MitmproxyStartRequest\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\x12\x14\n\x0c\x63\x61llbackAddr\x18\x03 \x01(\t\x12\x14\n\x0c\x63\x61llbackPort\x18\x04 \x01(\x05\x12\x15\n\rincludeUrlPat\x18\x05 \x01(\t\x12\x15\n\rexcludeUrlPat\x18\x06 \x01(\t\"F\n\x0eResultResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x12\n\nresultCode\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\")\n\nMitmHeader\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"d\n\x0bMitmRequest\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x0e\n\x06method\x18\x02 \x01(\t\x12\'\n\x07headers\x18\x03 \x03(\x0b\x32\x16.mitmpiping.MitmHeader\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\x0c\"\x86\x01\n\x0cMitmResponse\x12(\n\x07request\x18\x01 \x01(\x0b\x32\x17.mitmpiping.MitmRequest\x12\'\n\x07headers\x18\x02 \x03(\x0b\x32\x16.mitmpiping.MitmHeader\x12\x12\n\nstatusCode\x18\x03 \x01(\x05\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\x0c\x32\x99\x01\n\x0fMitmProxyBroker\x12H\n\x05start\x12!.mitmpiping.MitmproxyStartRequest\x1a\x1a.mitmpiping.ResultResponse\"\x00\x12<\n\x04stop\x12\x16.google.protobuf.Empty\x1a\x1a.mitmpiping.ResultResponse\"\x00\x32\xa0\x01\n\x11MitmProxyCallback\x12\x43\n\ronMitmRequest\x12\x17.mitmpiping.MitmRequest\x1a\x17.mitmpiping.MitmRequest\"\x00\x12\x46\n\x0eonMitmResponse\x12\x18.mitmpiping.MitmResponse\x1a\x18.mitmpiping.MitmResponse\"\x00\x62\x06proto3')



_MITMPROXYSTARTREQUEST = DESCRIPTOR.message_types_by_name['MitmproxyStartRequest']
_RESULTRESPONSE = DESCRIPTOR.message_types_by_name['ResultResponse']
_MITMHEADER = DESCRIPTOR.message_types_by_name['MitmHeader']
_MITMREQUEST = DESCRIPTOR.message_types_by_name['MitmRequest']
_MITMRESPONSE = DESCRIPTOR.message_types_by_name['MitmResponse']
MitmproxyStartRequest = _reflection.GeneratedProtocolMessageType('MitmproxyStartRequest', (_message.Message,), {
  'DESCRIPTOR' : _MITMPROXYSTARTREQUEST,
  '__module__' : 'mitmpiping_pb2'
  # @@protoc_insertion_point(class_scope:mitmpiping.MitmproxyStartRequest)
  })
_sym_db.RegisterMessage(MitmproxyStartRequest)

ResultResponse = _reflection.GeneratedProtocolMessageType('ResultResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESULTRESPONSE,
  '__module__' : 'mitmpiping_pb2'
  # @@protoc_insertion_point(class_scope:mitmpiping.ResultResponse)
  })
_sym_db.RegisterMessage(ResultResponse)

MitmHeader = _reflection.GeneratedProtocolMessageType('MitmHeader', (_message.Message,), {
  'DESCRIPTOR' : _MITMHEADER,
  '__module__' : 'mitmpiping_pb2'
  # @@protoc_insertion_point(class_scope:mitmpiping.MitmHeader)
  })
_sym_db.RegisterMessage(MitmHeader)

MitmRequest = _reflection.GeneratedProtocolMessageType('MitmRequest', (_message.Message,), {
  'DESCRIPTOR' : _MITMREQUEST,
  '__module__' : 'mitmpiping_pb2'
  # @@protoc_insertion_point(class_scope:mitmpiping.MitmRequest)
  })
_sym_db.RegisterMessage(MitmRequest)

MitmResponse = _reflection.GeneratedProtocolMessageType('MitmResponse', (_message.Message,), {
  'DESCRIPTOR' : _MITMRESPONSE,
  '__module__' : 'mitmpiping_pb2'
  # @@protoc_insertion_point(class_scope:mitmpiping.MitmResponse)
  })
_sym_db.RegisterMessage(MitmResponse)

_MITMPROXYBROKER = DESCRIPTOR.services_by_name['MitmProxyBroker']
_MITMPROXYCALLBACK = DESCRIPTOR.services_by_name['MitmProxyCallback']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MITMPROXYSTARTREQUEST._serialized_start=62
  _MITMPROXYSTARTREQUEST._serialized_end=203
  _RESULTRESPONSE._serialized_start=205
  _RESULTRESPONSE._serialized_end=275
  _MITMHEADER._serialized_start=277
  _MITMHEADER._serialized_end=318
  _MITMREQUEST._serialized_start=320
  _MITMREQUEST._serialized_end=420
  _MITMRESPONSE._serialized_start=423
  _MITMRESPONSE._serialized_end=557
  _MITMPROXYBROKER._serialized_start=560
  _MITMPROXYBROKER._serialized_end=713
  _MITMPROXYCALLBACK._serialized_start=716
  _MITMPROXYCALLBACK._serialized_end=876
# @@protoc_insertion_point(module_scope)