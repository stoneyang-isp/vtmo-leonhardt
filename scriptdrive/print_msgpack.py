import msgpack

if __name__ == "__main__":
  filename = "/Volumes/Daten/EXR/Untitled.vtmo"
  with open(filename, 'r') as f:
      data = msgpack.unpack(f)

  print data