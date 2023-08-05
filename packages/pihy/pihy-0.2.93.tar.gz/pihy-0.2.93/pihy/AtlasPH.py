#!/usr/bin/python

import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses
  
import time       # used for sleep delay and timestamps
import string     # helps parse strings

import pihy.AtlasI2C

class AtlasPH(pihy.AtlasI2C.AtlasI2C):
  default_bus = 1           # the default bus for I2C on the newer Raspberry Pis, certain older boards use bus 0
  default_address = -99       # the default address for the sensor
  current_addr = default_address
  is_sensor = True
  
  def __init__(self, address=default_address, bus=default_bus):
    self.current_addr = address
    pihy.AtlasI2C.AtlasI2C.__init__(self, address, bus)
  
  def GetPH(self):
    if self.current_addr == -99:
      val = 7.0
    else:
      val = float(self.query("R"))
    
    return val
    

def test():
  a = AtlasPH();
  print(a.GetPH())

if __name__ == '__main__':
  test()

