def GetPacketCount(dev_name):
  '''Return (received_packets, transmitted_packets) for network device dev_name'''
  with open('/proc/net/dev') as fp:
    for line in fp:
      line = line.split()
      if line[0].startswith(dev_name):
        
          return "%s\n R:%i T:%i" %(line[0], int(line[2]), int(line[10]))

if __name__ == '__main__':
  import sys
  print GetPacketCount(sys.argv[1])
