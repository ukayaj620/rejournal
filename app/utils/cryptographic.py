import base64

def encoder(input):
  string_bytes = input.encode("ascii")
  base64_bytes = base64.b64encode(string_bytes)
  base64_string = base64_bytes.decode("ascii")

  return base64_string

def decoder(input):
  base64_bytes = input.encode("ascii")
  string_bytes = base64.b64decode(base64_bytes)
  string = string_bytes.decode("ascii")

  return string

  