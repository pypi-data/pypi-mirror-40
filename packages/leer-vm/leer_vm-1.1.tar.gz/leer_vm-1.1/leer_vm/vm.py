from .opcodes import *
from .opfuncs import *
from .utils import ScriptException, ReturnException, StackData, StackBytes, StackPoint, itb
from typing import Dict, List, Callable, Union, Any, Tuple


def execute(script: bytes, \
            prev_block_props: Dict[str, int], \
            excess_lookup: Callable[[Any, bytes],Union[bool,bytes]], \
            output_lookup: Callable[[Any],Union[bool]], \
            burden: List[Tuple], #TODO
            execution_metadata: Dict[str,Any]={}):
  regime = "1 byte"
  evaluated_bytes = 0
  #stacks : List[List[StackData]] = [[]]
  stacks = [[]] # type: ignore   #We can not specify type for python<3.6
  last_op = None
  try:
    while len(script):
      if regime == "1 byte":
        op, script = script[0], script[1:] #Note op is integer, not byte
      elif regime == "2 byte":
        op, script = int.from_bytes(script[0:2], "big"), script[2:]
      last_op = op
      if not op in special_ops:
        f = op_func_dict.get(op, f_UNASSIGNED)
        script = f(stacks, script)
      elif op==OP_EVAL: 
        data = stacks[0].pop().to_bytes()
        if len(data)+evaluated_bytes>1024:
          raise ScriptException("Summary length of eval'ed bytes greater than 1024: requested evaluation of %d bytes, already evaluated %d bytes"%(len(data), evaluated_bytes))
        else:
          evaluated_bytes += len(data)
          script = data+script
      elif op==OP_2BYTESOPS:
        regime = "2 byte"
      elif op==OP_FINDEXCESS:
        pubkey = stacks[0].pop().to_point()
        _hash = stacks[0].pop().to_bytes()
        preimage = excess_lookup(pubkey=pubkey, _hash=_hash) #excess_lookup returns preimage or false if cant find anything
        if isinstance(preimage, bytes):
          stacks[0].append(StackBytes(preimage))
        else:
          if preimage == False:
            raise ScriptException("Excess with pubkey %s and hash(message) %s not found"%(str(pubkey), _hash))
          else:
            raise ScriptException("Unexpected excess_lookup(%s,%s) result: %s (Type:%s)"%(str(pubkey), _hash, preimage, type(preimage)))
      elif op==OP_OUTPUTORHASH:
        commitment = stacks[0].pop().to_point()
        pubkey = stacks[0].pop().to_point()
        commitment_existence = output_lookup(commitment=commitment)        
        if commitment_existence:
          burden.append((commitment, pubkey)) #Note burden would be imposed only if script return True
        else:
          preimage = excess_lookup(pubkey=pubkey, _hash=sha256("\x01\x00"+commitment.to_bytes()) )
          if isinstance(preimage, bool):
            if preimage==False:
              raise ScriptException("Excess with pubkey %s and hash(message) %s not found"%(str(pubkey), _hash))          
            else:
              raise ScriptException("Unexpected excess_lookup(%s,%s) result from inside OUTPUTORHASH : %s"%(str(pubkey), _hash, preimage))
      elif op==OP_BNGT:
        block_threshold = stacks[0].pop().to_int()
        if block_threshold > prev_block_props["height"]:
          raise ScriptException("Block threshold %d is not met: height %d"%( block_threshold, prev_block_props["height"]))
        stacks[0].append( StackBytes(itb(prev_block_props["height"]-block_threshold)) )
      elif op==OP_TIMEGT:
        timestamp_threshold = stacks[0].pop().to_int()
        if timestamp_threshold > prev_block_props["timestamp"]:
          raise ScriptException("Timestamp threshold %d is not met: height %d"%( timestamp_threshold, prev_block_props["timestamp"]))
        stacks[0].append( StackBytes(itb(prev_block_props["timestamp"]-timestamp_threshold)) )
      else: #TODO
        pass
  except ReturnException as e:
    execution_metadata["stacks"] = stacks
    execution_metadata["regime"] = regime
    execution_metadata["evaluated bytes"] = evaluated_bytes
    execution_metadata["last op"] = last_op
    execution_metadata["script residue"] = script
    return e.value
  except ScriptException as e:
    execution_metadata["stacks"] = stacks
    execution_metadata["exception"] = e.error_message
    execution_metadata["regime"] = regime
    execution_metadata["evaluated bytes"] = evaluated_bytes
    execution_metadata["last op"] = last_op
    execution_metadata["script residue"] = script
    return False
  except IndexError as e:
    execution_metadata["stacks"] = stacks
    execution_metadata["exception"] = "Not enought elements on stack or bytes on script"
    execution_metadata["regime"] = regime
    execution_metadata["evaluated bytes"] = evaluated_bytes
    execution_metadata["last op"] = last_op
    execution_metadata["script residue"] = script
    return False

  execution_metadata["stacks"] = stacks
  execution_metadata["regime"] = regime
  execution_metadata["evaluated bytes"] = evaluated_bytes
  execution_metadata["last op"] = last_op

  #No exception, get last element and cast it to bool
  if len(stacks[0]):
    element = stacks[0][-1]
    if isinstance(element, StackPoint):
      return True
    else:
      return element.to_bool()
  else:
    return False
