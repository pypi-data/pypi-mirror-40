from typing import TypeVar, Type
from secp256k1_zkp import Point

class ScriptException(Exception):
  def __init__(self, error_message):
    self.error_message = error_message

class ReturnException(Exception):
  def __init__(self, value):
    self.value = value

class StackData:
  def to_bytes(self) -> bytes:
    raise NotImplemented #Should be overwrited in subclass
    return b""
  def to_point(self) -> Point:
    raise NotImplemented #Should be overwrited in subclass
    return Point()

StackBytesType = TypeVar('StackBytesType', bound='StackBytes')
StackPointType = TypeVar('StackPointType', bound='StackPoint')

class StackBytes(StackData):
  def __init__(self: StackBytesType, data: bytes):
    self.data = data

  def to_int(self: StackBytesType) -> int:
    return int.from_bytes(self.data,'big')

  def to_bool(self: StackBytesType) -> bool:
    return bool(self.to_int())

  def to_bytes(self: StackBytesType) -> bytes:
    return self.data

  def __repr__(self: StackBytesType) -> str:
    if len(self.data)<2:
      return "StackBytes(%s: %s)"%(repr(self.data), int.from_bytes(self.data, "big"))    
    return "StackBytes(%s...)"%(repr(self.data[:6]))

  def to_point(self: StackBytesType) -> Point: 
    try:
      return Point(raw_point=self.data)
    except:
      raise ScriptException("Invalid point")

class StackPoint(StackData):
  def __init__(self: StackPointType, point: Point):
    self.point = point

  def to_bytes(self: StackPointType) -> bytes:
    return bytes(self.point.serialize())

  def to_point(self: StackPointType) -> Point: 
    return self.point




def itb(i: int) -> bytes:
    return i.to_bytes(max((i.bit_length() + 7) // 8, 1), 'big')


