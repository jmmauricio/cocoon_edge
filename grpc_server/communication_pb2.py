# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: communication.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x63ommunication.proto\"T\n\x0eNumbersRequest\x12\x0f\n\x07number1\x18\x01 \x01(\x02\x12\x0f\n\x07number2\x18\x02 \x01(\x02\x12\x0f\n\x07number3\x18\x03 \x01(\x02\x12\x0f\n\x07number4\x18\x04 \x01(\x02\"\"\n\x0fNumbersResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2E\n\rCommunication\x12\x34\n\x0bSendNumbers\x12\x0f.NumbersRequest\x1a\x10.NumbersResponse\"\x00(\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'communication_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_NUMBERSREQUEST']._serialized_start=23
  _globals['_NUMBERSREQUEST']._serialized_end=107
  _globals['_NUMBERSRESPONSE']._serialized_start=109
  _globals['_NUMBERSRESPONSE']._serialized_end=143
  _globals['_COMMUNICATION']._serialized_start=145
  _globals['_COMMUNICATION']._serialized_end=214
# @@protoc_insertion_point(module_scope)
