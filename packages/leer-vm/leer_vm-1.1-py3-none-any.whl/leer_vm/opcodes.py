#Stack machine has 2 types in it:
# points on elliptic curve
# bytes

#There are implicit casts:
# bytes -> numbers (big endian)
# numbers -> bytes (big endian)
# bytes -> bools (nonzero bytes -> true, anythin else ->false) 
# points -> bytes (serialization)
# bytes -> points (deserialization)
# bools -> bytes (true -> 0x01, false ->0x00)
# no chains of casts: points will not be casted to number or bool

# If there is not enough elements on stack, return false
# If there wrong type of element on stack, return false
# If note enough bytes in script for load opcode, return false
# If element on stack is not 33 bytes long or can not be casted to valid point and implicit cast is required, return False
# If 33 bytes after OP_PUSH_POINT can not be treated as valid point serialization, return false
# Any unknown opcode has "immediately return true" effect
# If execution is finished and no value was returned, cast last element to bool and return (in this specific case any valid point will be casted to true), if no elements on main stack return False

OP_RETURN = 0x00 # Remove element from stack, cast it to bool and return
OP_TRUE = 0x01 # Push true to stack
OP_FALSE = 0x02 # Push false to stack
OP_PUSHPOINT = 0x03 # Get next 33 bytes, deserialize it as point, push to stack
OP_PUSHBYTE = 0x04 # Get next byte, push to stack
OP_PUSH2BYTES = 0x05 # Get next 2 bytes, push to stack
OP_PUSH32BYTES = 0x06 # Get next 32 bytes, push to stack

OP_PUSHBYTES = 0x07 # Remove element _n_ from stack, cast to number, get next _n_ bytes, push to stack as one element. _n_ should be less than than 1024

OP_BOOLINVERT = 0x08 # Remove element, cast to bool, invert, push to stack

#flow controls
OP_IF = 0x09 # Remove 3 elements from stack _x_, _n1_, _n2_. Remove _n1_ bytes from script (first part), and then _n2_ bytes from script (second part). Cast _x_ to bool, if true push first part to script, else second one. If _n1_+_n2_ greater than script length return false

OP_POINTSSUM = 0x0a  # Remove two elements from stack _p1_, _p2_, cast to points, push sum to stack
OP_POINTMULT = 0x0b # Remove two elements from stack _x_, _p1_, cast _x_ to integer (mod curve order), cast _p1_ to points, push _x_*_p1_ to stack

#stack
OP_INITIALIZESTACKS = 0x0c # Remove element _n_ from stack, cast to number, initialise _n_ additional stacks. _n_ should be less than 255. Number of initialized stacks during script should be less than 255
#Stack numeration starts from 0 where 0th stack is main stack and 1th and higher stacks - explicitly initialised stacks.
OP_TOALTSTACK = 0x0d #Remove two elements _n_, (arbitraty)_data_ from stack, cast _n_ to number, push _data_ to n-th stack.
OP_FROMALTSTACK = 0x0e #Remove element from main stack _n_, cast to number, remove element from nth stack, push to main stack

OP_DUP = 0x0f #Duplicate element on stack
OP_DEPTH = 0x10 #Push number of elements in main stack to stack
OP_ALTDEPTH = 0x11 #Remove element from main stack _n_, cast to number, push number of elements in _n_th stack to main stack
OP_TYPEOF = 0x12 # Push type of top element in stack to stack: bytes -> 0x01, point ->0x02

OP_DROP = 0x13 #Drop element from stack
OP_SWAP = 0x14 #Swap two top elements
OP_ARBITRARYSWAP = 0x15 #Remove  two elements from stack _n1_, _n2_, cast to number, swap n1th and n2th elements
OP_PICK = 0x16 #Remove element from stack _n_, cast to number, push copy of nth element to stack
OP_ROLL = 0x17 #Remove element from stack _n_, cast to number, remove nth element from stack and push to stack

OP_SIZE = 0x18 #Push size of element (implicit cast to bytes) in stack to stack

OP_EQUAL = 0x19 #Remove two elements from stack, cast to numbers, check if equal (Thus b'\x00\x03' will be equal b'\x03')
OP_STRICTEQUAL = 0x1a #Remove two elements from stack, cast to bytes (two bytes string are equal if identical)

OP_INCREMENT = 0x1b # Remove element from stack _n_, cast to number, add 1, push to stack
OP_DECREMENT = 0x1c # Remove element from stack _n_, cast to number, subtract 1, push to stack
OP_ADD = 0x1d # Remove two elements from stack _n1_, _n2_, cast to numbers, push summ to stack
OP_SUBTRACT = 0x1e # Remove two elements from stack _n1_, _n2_, cast to numbers, push (n1-n2)>0? (n1-n2):0 to stack
OP_LESSTHAN = 0x1f # Remove two elements from stack _n1_, _n2_, cast to numbers, push bool(n1<n2) to stack
OP_LESSTHANOREQUAL = 0x20 # Remove two elements from stack _n1_, _n2_, cast to numbers, push bool(n1<=n2) to stack
OP_MIN = 0x21 # Remove element from stack _n_, cast to number, push to stack minimal element from n top elements on stack (elements are compared as number, leading zeroes will be removed)
OP_MAX = 0x22 # Remove element from stack _n_, cast to number, push to stack maximal element from n top elements on stack (elements are compared as number, leading zeroes will be removed)
OP_MULTIDROP =0x23 #Remove element from stack _n_, cast to number, remove n elements from stack


OP_SHA256 = 0x24 #Remove element from stack, cast to bytes, push hash256 to stack
OP_SHA3 = 0x25 #Remove element from stack, cast to bytes, push hash3 to stack

# lookups
OP_FINDEXCESS = 0x26 #Remove 2 elements from stack _pubkey_, _hash_, check that set of excesses after transaction generation contains excess with this public key and signed sha256 hash of message, put message to stack, if there is no such excess - halt execution and return false


OP_OUTPUTORHASH = 0x27 #Remove 2 elements from stack _commitment_, _pubkey_ check that set of outputs contains commitment or set of excesses  contains excess with this public key and signed script "0x0100"+serialized_commitment. If both checks were failed - halt execution and return false. Note that there is exterior condition for script which contains OP_OUTPUTORHASH to be valid: if branch `set of outputs contains commitment` is used, output with this commitment should contain hash256 of this script in authorized burden field.

OP_2BYTESOPS = 0x28 # After this opcode 2bytes per OP is activated

OP_EVAL = 0x29 # Get element from stack, insert to begining of script. Note, while number of OP_EVAL instructions is not limited, number of inserted bytes during all operations is limited by 1024 bytes.

OP_BNGT = 0x30 # Get element from stack _n_, cast to number, get height of previous block _h_, check that _n_<=_h_ and put _h_-_n_ on stack, otherwise halt execution and return false

OP_TIMEGT = 0x31 # Get element from stack _n_, cast to number, get UNIX timestamp of previous block _t_, check that _n_<=_t_ and put _h_-_n_ on stack, otherwise halt execution and return false

OP_NOTHING = 0x32 # Do nothing.

OP_CONCAT = 0x33 # Concat two bytes arrays
