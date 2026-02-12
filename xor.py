import itertools
def cycled_xor(input: str = "", keys: str = "") -> bytes:
  result = ""
  for i in range(len(input)):
    byte = input[i].encode('utf-8')
    xKey = keys[i % len(keys)].encode('utf-8')
    result += chr(byte[0] ^ xKey[0])
  return result
def singular_xor (input: str = "", key: int = 11) -> str:
  result = ""
  for i in range(len(input)):
    byte = ord(input[i])
    result += chr(byte ^ key)
  return result