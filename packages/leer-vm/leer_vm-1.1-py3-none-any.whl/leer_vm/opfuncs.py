from .utils import ScriptException, ReturnException, StackData, StackBytes, StackPoint, itb
from typing import Dict, List, TYPE_CHECKING
from .opcodes import *
from secp256k1_zkp import Point
import hashlib

        


# There are a lot of code
# ```
# if isinstance ...:
#   ...  
# else:
#   raise ...
# ```
# While it goes against 'Easier to ask for forgiveness than permission'
# it is the only good enough workaround for mypy testing

def f_RETURN(stacks: List[List[StackData]], script: bytes) -> bytes:
  result = stacks[0].pop()
  if isinstance(result, StackBytes):
    raise ReturnException(value = result.to_bool())
  else:
    raise ScriptException("Bool casted to %s"%type(result))
  return script

def f_FALSE(stacks: List[List[StackData]], script: bytes) -> bytes:
  stacks[0].append(StackBytes(b"\x00"))
  return script

def f_TRUE(stacks: List[List[StackData]], script: bytes) -> bytes:
  stacks[0].append(StackBytes(b"\x01"))
  return script

def f_PUSHPOINT(stacks: List[List[StackData]], script: bytes) -> bytes:
  s_point, script = script[:33], script[33:]
  try:
    p =  Point(raw_point=s_point)
  except:
    raise ScriptException("Invalid point")
  stacks[0].append(StackPoint(p))
  return script

def f_PUSHBYTE(stacks: List[List[StackData]], script: bytes) -> bytes:
  s_byte, script = script[:1], script[1:]
  stacks[0].append(StackBytes(bytes(s_byte)))
  return script

def f_PUSH2BYTES(stacks: List[List[StackData]], script: bytes) -> bytes:
  s_bytes, script = script[:2], script[2:]
  stacks[0].append(StackBytes(bytes(s_bytes)))
  return script

def f_PUSH32BYTES(stacks: List[List[StackData]], script: bytes) -> bytes:
  s_bytes, script = script[:32], script[32:]
  stacks[0].append(StackBytes(bytes(s_bytes)))
  return script


def f_PUSHBYTES(stacks: List[List[StackData]], script: bytes) -> bytes:
  _len_element = stacks[0].pop()
  if isinstance(_len_element, StackBytes):
   _len = _len_element.to_int()
  else:
    raise ScriptException("Int casted to %s"%type(_len_element))
  if _len>1023:
    raise ScriptException("PUSHBYTES argument is too long: %d"%(_len))
  s_bytes, script = script[:_len], script[_len:]
  stacks[0].append(StackBytes(bytes(s_bytes)))
  return script

def f_BOOLINVERT(stacks: List[List[StackData]], script: bytes) -> bytes:
  result = stacks[0].pop()
  if isinstance(result, StackBytes):
    res = not result.to_bool()
    sb_res = StackBytes(itb(res))
    stacks[0].append(sb_res)
  else:
    raise ScriptException("Bool casted to %s"%type(result))
  return script

def f_INITIALIZESTACKS(stacks: List[List[StackData]], script: bytes) -> bytes:
  number_of_stacks = stacks[0].pop()
  if isinstance(number_of_stacks, StackBytes):
    number_of_stacks_int=number_of_stacks.to_int()
  else:
    raise ScriptException("Int casted to %s"%type(number_of_stacks))
  if number_of_stacks_int+len(stacks)>255:
    raise ScriptException("To much stacks: current %d, to activate %d"%(len(stacks), number_of_stacks_int))
  for i in range(number_of_stacks_int):
    stacks.append([])
  return script

def f_TOALTSTACK(stacks: List[List[StackData]], script: bytes) -> bytes:
  stack_index = stacks[0].pop()
  element = stacks[0].pop()
  if isinstance(stack_index, StackBytes):
    stack_index_int=stack_index.to_int()
  else:
    raise ScriptException("Int casted to %s"%type(stack_index))
  if stack_index_int>len(stacks)-1:
    raise ScriptException("Operation with inactivated stack %d"%(stack_index_int))
  stacks[stack_index_int].append(element)
  return script

def f_FROMALTSTACK(stacks: List[List[StackData]], script: bytes) -> bytes:
  stack_index = stacks[0].pop()
  if isinstance(stack_index, StackBytes):
    stack_index_int=stack_index.to_int()
  else:
    raise ScriptException("Int casted to %s"%type(stack_index))
  if stack_index_int>len(stacks)-1:
    raise ScriptException("Operation with unactivated stack %d"%(stack_index_int))
  element = stacks[stack_index_int].pop()
  stacks[0].append(element)
  return script



def f_DUP(stacks: List[List[StackData]], script: bytes) -> bytes:
  element = stacks[0].pop()
  stacks[0].append(element)
  stacks[0].append(element)
  return script

def f_DEPTH(stacks: List[List[StackData]], script: bytes) -> bytes:
  stacks[0].append(StackBytes(data=itb(len(stacks[0])) ))
  return script

def f_ALTDEPTH(stacks: List[List[StackData]], script: bytes) -> bytes:
  stack_index = stacks[0].pop()
  if isinstance(stack_index, StackBytes):
    stack_index_int=stack_index.to_int()
  else:
    raise ScriptException("Int casted to %s"%type(stack_index))
  if stack_index_int>len(stacks)-1:
    raise ScriptException("Operation with unactivated stack %d"%(stack_index_int))
  stacks[0].append(StackBytes(data=itb(len(stacks[stack_index_int])) ))
  return script

def f_TYPEOF(stacks: List[List[StackData]], script: bytes) -> bytes:
  element = stacks[0].pop()
  stacks[0].append(element)
  if isinstance(element, StackBytes):   
    stacks[0].append(StackBytes(b"\x01"))
  if isinstance(element, StackPoint):   
    stacks[0].append(StackBytes(b"\x02"))
  return script

def f_DROP(stacks: List[List[StackData]], script: bytes) -> bytes:
  return script

def f_SWAP(stacks: List[List[StackData]], script: bytes) -> bytes:
  element1 = stacks[0].pop()
  element2 = stacks[0].pop()
  stacks[0].append(element1)
  stacks[0].append(element2)
  return script

def f_ARBITRARYSWAP(stacks: List[List[StackData]], script: bytes) -> bytes:
  n1 = stacks[0].pop()
  n2 = stacks[0].pop()
  l = len(stacks[0])
  if isinstance(n1, StackBytes) and isinstance(n2, StackBytes):
    n1_int,n2_int = l-n1.to_int(), l-n2.to_int()
  else:
    raise ScriptException("Int casted to %s and %s"%(type(n1), type(n2)))
  swap_var = stacks[0][n2_int]
  stacks[0][n2_int] = stacks[0][n1_int]
  stacks[0][n1_int] = swap_var
  return script

def f_PICK(stacks: List[List[StackData]], script: bytes) -> bytes:
  n = stacks[0].pop()
  l = len(stacks[0])
  if isinstance(n, StackBytes):
    n_int = l-n.to_int()
  else:
    raise ScriptException("Int casted to %s"%(type(n)))
  element = stacks[0][n_int]
  stacks[0].append(element)
  return script

def f_ROLL(stacks: List[List[StackData]], script: bytes) -> bytes:
  n = stacks[0].pop()
  l = len(stacks[0])
  if isinstance(n, StackBytes):
    n_int = l-n.to_int()
  else:
    raise ScriptException("Int casted to %s"%(type(n)))
  element = stacks[0].pop(n_int)
  stacks[0].append(element)
  return script


def f_SIZE(stacks: List[List[StackData]], script: bytes) -> bytes:
  l = len(stacks[0])
  stacks[0].append(StackBytes(itb(l)))
  return script

def f_EQUAL(stacks: List[List[StackData]], script: bytes) -> bytes:
  n1 = stacks[0].pop()
  n2 = stacks[0].pop()
  if isinstance(n1, StackBytes) and isinstance(n2, StackBytes):
    ser1, ser2 = n1.to_bytes(), n2.to_bytes()
    n1_int, n2_int = int.from_bytes(ser1, "big"), int.from_bytes(ser2, "big")
  else:
    raise ScriptException("Implicit chain of casts ->bytes->int is prohibited.  %s and %s"%(type(n1), type(n2)))
  if n1_int==n2_int:
    stacks[0].append(StackBytes(b"\x01"))
  else:
    stacks[0].append(StackBytes(b"\x00"))
  return script

def f_STRICTEQUAL(stacks: List[List[StackData]], script: bytes) -> bytes:
  n1 = stacks[0].pop()
  n2 = stacks[0].pop()
  ser1, ser2 = n1.to_bytes(), n2.to_bytes()
  if ser1==ser2:
    stacks[0].append(StackBytes(b"\x01"))
  else:
    stacks[0].append(StackBytes(b"\x00"))
  return script


def f_INCREMENT(stacks: List[List[StackData]], script: bytes) -> bytes:
  element = stacks[0].pop()
  if isinstance(element, StackBytes):
    n = element.to_int() + 1
    stacks[0].append( StackBytes( itb(n) ) )
  else:
    raise ScriptException("Implicit chain of casts ->bytes->int is prohibited. %s"%(type(element)))
  return script

def f_DECREMENT(stacks: List[List[StackData]], script: bytes) -> bytes:
  element = stacks[0].pop()
  if isinstance(element, StackBytes):
    n= element.to_int() -1
  else:
    raise ScriptException("Implicit chain of casts ->bytes->int is prohibited. %s"%(type(element)))
  if n<0:
    n=0
  stacks[0].append( StackBytes(itb(n)) )
  return script

def f_ADD(stacks: List[List[StackData]], script: bytes) -> bytes:
  n1 = stacks[0].pop()
  n2 = stacks[0].pop()
  if isinstance(n1, StackBytes) and isinstance(n2, StackBytes):
    n1_int,n2_int = n1.to_int(), n2.to_int()
  else:
    raise ScriptException("Int casted to %s and %s"%(type(n1), type(n2)))
  stacks[0].append( StackBytes(itb(n1_int+n2_int)) )
  return script

def f_SUBTRACT(stacks: List[List[StackData]], script: bytes) -> bytes:
  n1 = stacks[0].pop()
  n2 = stacks[0].pop()
  if isinstance(n1, StackBytes) and isinstance(n2, StackBytes):
    n1_int,n2_int = n1.to_int(), n2.to_int()
  else:
    raise ScriptException("Int casted to %s and %s"%(type(n1), type(n2)))
  result = n1_int-n2_int
  if result<0:
    result = 0
  stacks[0].append( StackBytes(itb(result)) )
  return script

def f_LESSTHAN(stacks: List[List[StackData]], script: bytes) -> bytes:
  n1 = stacks[0].pop()
  n2 = stacks[0].pop()
  if isinstance(n1, StackBytes) and isinstance(n2, StackBytes):
    n1_int,n2_int = n1.to_int(), n2.to_int()
  else:
    raise ScriptException("Int casted to %s and %s"%(type(n1), type(n2)))
  result = int(n1_int<n2_int)
  stacks[0].append( StackBytes(itb(result)) )
  return script

def f_LESSTHANOREQUAL(stacks: List[List[StackData]], script: bytes) -> bytes:
  n1 = stacks[0].pop()
  n2 = stacks[0].pop()
  if isinstance(n1, StackBytes) and isinstance(n2, StackBytes):
    n1_int,n2_int = n1.to_int(), n2.to_int()
  else:
    raise ScriptException("Int casted to %s and %s"%(type(n1), type(n2)))
  result = int(n1_int<=n2_int)
  stacks[0].append( StackBytes(itb(result)) )
  return script

def f_MIN(stacks: List[List[StackData]], script: bytes) -> bytes:
  num = stacks[0].pop()
  if isinstance(num, StackBytes):
    num_int = num.to_int()
  else:
    raise ScriptException("Int casted to %s"%(type(num)))
  m = []
  for i in range(num_int):
    element = stacks[0].pop()
    if isinstance(element, StackBytes):
      element_int = element.to_int()
    else:
      raise ScriptException("Int casted to %s"%(type(element)))
    m.append(element_int)
  stacks[0].append( StackBytes(itb(min(m))) )    
  return script


def f_MAX(stacks: List[List[StackData]], script: bytes) -> bytes:
  num = stacks[0].pop()
  if isinstance(num, StackBytes):
    num_int = num.to_int()
  else:
    raise ScriptException("Int casted to %s"%(type(num)))
  m = []
  for i in range(num_int):
    element = stacks[0].pop()
    if isinstance(element, StackBytes):
      element_int = element.to_int()
    else:
      raise ScriptException("Int casted to %s"%(type(element)))
    m.append(element_int)
  stacks[0].append( StackBytes(itb(max(m))) )    
  return script

def f_MULTIDROP(stacks: List[List[StackData]], script: bytes) -> bytes:
  n = stacks[0].pop()
  if isinstance(n, StackBytes):
    n_int = n.to_int()
  else:
    raise ScriptException("Int casted to %s"%(type(n)))
  for i in range(n_int):
    stacks[0].pop()
  return script

def f_IF(stacks: List[List[StackData]], script: bytes) -> bytes:
  condition =  stacks[0].pop()
  n1 = stacks[0].pop()
  n2 = stacks[0].pop()
  if isinstance(condition, StackBytes) and isinstance(n1, StackBytes) and isinstance(n2, StackBytes):
    condition_bool = condition.to_bool()
    n1_int = n1.to_int()
    n2_int = n2.to_int()
  else:
    raise ScriptException("Bool casted to %s or Int casted to %s or %s"%(type(condition),type(n1), type(n2)))
  if n1_int+n2_int>len(script):
    raise ScriptException("if expressions lengths are too big")  
  _if, _else, script = script[:n1_int], script[n1_int:n1_int+n2_int], script[n1_int+n2_int:]
  script = (_if if condition_bool else _else) + script
  return script

def f_UNASSIGNED(stacks: List[List[StackData]], script: bytes) -> bytes:
  raise ReturnException(True)
  return script

def f_NOTHING(stacks: List[List[StackData]], script: bytes) -> bytes:
  return script

def f_SHA256(stacks: List[List[StackData]], script: bytes) -> bytes:
  preimage = stacks[0].pop()
  preimage_bytes = preimage.to_bytes()
  m = hashlib.sha256()
  m.update(preimage_bytes)
  image = StackBytes(m.digest())
  stacks[0].append(image)
  return script

def f_SHA3(stacks: List[List[StackData]], script: bytes) -> bytes:
  if not "sha3_256" in hashlib.algorithms_available:
    import sha3
  preimage = stacks[0].pop()
  preimage_bytes = preimage.to_bytes()
  m = hashlib.sha3_256() #type: ignore    #sha3 will monkey-patch if python version <3.6
  m.update(preimage_bytes)
  image = StackBytes(m.digest())
  stacks[0].append(image)
  return script

def f_POINTSSUM(stacks: List[List[StackData]], script: bytes) -> bytes:
  sp1 = stacks[0].pop()
  sp2 = stacks[0].pop()
  p1, p2 = sp1.to_point(), sp2.to_point()
  stacks[0].append(StackPoint(p1+p2))
  return script

def f_POINTMULT(stacks: List[List[StackData]], script: bytes) -> bytes:
  n = stacks[0].pop()
  sp1 = stacks[0].pop()
  if isinstance(n, StackBytes):
    num=n.to_int()
  else:
    raise ScriptException("Implicit chain of casts ->bytes->int is prohibited. %s"%(type(n)))
  p1 = sp1.to_point()
  stacks[0].append(StackPoint(p1*num))
  return script



def f_CONCAT(stacks: List[List[StackData]], script: bytes) -> bytes:
  sp1 = stacks[0].pop()
  sp2 = stacks[0].pop()
  p1, p2 = sp1.to_bytes(), sp2.to_bytes()
  stacks[0].append(StackBytes(p1+p2))
  return script


op_func_dict = {OP_RETURN: f_RETURN, OP_TRUE: f_TRUE, OP_FALSE: f_FALSE, OP_PUSHPOINT: f_PUSHPOINT, OP_PUSHBYTE: f_PUSHBYTE, OP_PUSH2BYTES: f_PUSH2BYTES, OP_PUSH32BYTES: f_PUSH32BYTES, OP_PUSHBYTES: f_PUSHBYTES, OP_BOOLINVERT: f_BOOLINVERT, OP_INITIALIZESTACKS: f_INITIALIZESTACKS, OP_TOALTSTACK: f_TOALTSTACK, OP_FROMALTSTACK: f_FROMALTSTACK, OP_DUP: f_DUP, OP_DEPTH: f_DEPTH, OP_ALTDEPTH: f_ALTDEPTH, OP_TYPEOF: f_TYPEOF, OP_DROP: f_DROP, OP_SWAP: f_SWAP, OP_ARBITRARYSWAP: f_ARBITRARYSWAP, OP_PICK: f_PICK, OP_ROLL: f_ROLL, OP_SIZE: f_SIZE, OP_EQUAL: f_EQUAL, OP_STRICTEQUAL: f_STRICTEQUAL, OP_INCREMENT: f_INCREMENT, OP_DECREMENT: f_DECREMENT, OP_ADD: f_ADD, OP_SUBTRACT: f_SUBTRACT, OP_LESSTHAN: f_LESSTHAN, OP_LESSTHANOREQUAL: f_LESSTHANOREQUAL, OP_MIN: f_MIN, OP_MAX: f_MAX, OP_MULTIDROP: f_MULTIDROP, OP_IF: f_IF, OP_SHA256: f_SHA256, OP_SHA3: f_SHA3, OP_POINTSSUM: f_POINTSSUM, OP_POINTMULT: f_POINTMULT, OP_NOTHING: f_NOTHING, OP_CONCAT: f_CONCAT}

special_ops = [OP_EVAL, OP_2BYTESOPS, OP_FINDEXCESS, OP_OUTPUTORHASH, OP_BNGT, OP_TIMEGT] # Special operations which processed directly in VM processor
