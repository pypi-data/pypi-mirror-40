#!/usr/bin/python

import io         # used to create file streams
import fcntl      # used to access I2C parameters like addresses
  
import time       # used for sleep delay and timestamps
import string     # helps parse strings

class Log():
  default_storage = "/tmp/log"
  
  def __init__(self, storage=default_storage):
    self.storage_today = storage + time.strftime("%Y-%m-%d") + ".json"
    self.storage_web = storage + ".json"
  
    self.data = None
    if os.path.exists(self.storage_today):
      with open(self.storage_today,'r') as f:
        try:
          self.data = json.load(f)
        except Exception as e:
          print("got %s on json.load()" % e)

    if self.data is None:
      print('Create new dataset')
      self.data = [ ]
  
  def Add(xVal):
    xTime = time.strftime("%Y-%m-%d %H:%M:%S")
    self.data.append({'time': xTime, 'value': xVal})
    
  def Save():
    with open(storage_today, 'w') as outfile:
      json.dump(data, outfile)
    
    with open(storage_web, 'w') as outfile:
      json.dump(data, outfile)

