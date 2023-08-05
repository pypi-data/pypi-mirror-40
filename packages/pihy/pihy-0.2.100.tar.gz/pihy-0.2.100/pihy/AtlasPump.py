#!/usr/bin/python

import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses
  
import time       # used for sleep delay and timestamps
import string     # helps parse strings

import pihy.AtlasI2C

class AtlasPump(pihy.AtlasI2C.AtlasI2C):
  default_bus = 1           # the default bus for I2C on the newer Raspberry Pis, certain older boards use bus 0
  default_address = -99       # the default address for the sensor
  
  def __init__(self, address=default_address, bus=default_bus):
    pihy.AtlasI2C.AtlasI2C.__init__(self, address, bus)
  
  def Hello():
    print("HELLO")

  def Pump(self, val):
    if not self.current_addr == -99:
      self.query("D,"+str(val))

def test():
  print("Hello there")
  
  a = AtlasPump();
  #a.Hello()

if __name__ == '__main__':
  test()
