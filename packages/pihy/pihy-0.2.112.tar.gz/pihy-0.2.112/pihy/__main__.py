import schedule
import time
import json
import os
import sys

from pihy.x import joke
from pihy.AtlasI2C import AtlasI2C
import pihy.AtlasPH
import pihy.AtlasPump

storage_path_ph_long = "/var/www/raspberry_reactjs/logs/ph"
storage_path_ph_short = "/var/www/raspberry_reactjs/logs/ph_short"

storage_path_pumpBase = "/var/www/raspberry_reactjs/logs/pumpBase"
storage_path_pumpAcid = "/var/www/raspberry_reactjs/logs/pumpAcid"
storage_path_pump_run = "/var/www/raspberry_reactjs/logs/pump_run"

run = True
runPump = 0
pumpAcid = False

ph = pihy.AtlasPH.AtlasPH(address=99)
pumpAcid = pihy.AtlasPump.AtlasPump(address=11)
pumpBase = pihy.AtlasPump.AtlasPump(address=12)


def Log(storage, xVal, limit=-9):
  storage_today = storage + time.strftime("%Y-%m-%d") + ".json"
  storage_web = storage + ".json"
  
  data = None
  if os.path.exists(storage_today):
    with open(storage_today,'r') as f:
      try:
        data = json.load(f)
      except Exception as e:
        print("got %s on json.load()" % e)

  if data is None:
    print('Create new dataset')
    data = [ ]

  xTime = time.strftime("%Y-%m-%d %H:%M:%S")
  data.append({'time': xTime, 'value': xVal})

  if(limit>0):
    data = data[-limit:]

  with open(storage_today, 'w') as outfile:
    json.dump(data, outfile)
  
  with open(storage_web, 'w') as outfile:
    json.dump(data, outfile)

  return xTime

def PHLong():
  global runPump
  xVal = ph.GetPH()

  if xVal > 6.0:
    runPump = runPump + 1
  elif runPump and xVal>5.6 and xVal < 5.9:
    runPump = 0
  elif xVal < 5.5:
    runPump = runPump - 1

  Log(storage_path_ph_long, xVal)
  Log(storage_path_pump_run, runPump)

def PHShort():
  xVal = ph.GetPH()
  xTime = Log(storage_path_ph_short, xVal, 720)

  print("%s: pH %s" % (xTime, xVal))

def PumpBaseLong():
  data = None
  pumpVal = 0
  print("PUMP VALUE: %s" % runPump)
  
  if runPump < -20:
    print("PUMP BASE!!")
    phVal = ph.GetPH()
    if phVal<5.0:
      pumpVal = 5
    elif phVal<5.25:
      pumpVal = 5
    elif phVal<5.4:
      pumpVal = 3
    elif phVal<5.5:
      pumpVal = 2
    else:
      pumpVal = 1
    
  if pumpVal > 0:
    print("PUMPING: %s" % pumpVal)
    pumpBase.Pump(pumpVal)
  Log(storage_path_pumpBase,pumpVal)

def PumpAcidLong():
  data = None
  pumpVal = 0
  print("PUMP VALUE: %s" % runPump)
  
  if runPump > 20:
    print("PUMP ACID!!")
    phVal = ph.GetPH()
    if phVal>7.0:
      pumpVal = 15
    elif phVal>6.5:
      pumpVal = 10
    elif phVal>6.25:
      pumpVal = 5
    elif phVal>6.1:
      pumpVal = 3
    elif phVal>6.0:
      pumpVal = 2
    else:
      pumpVal = 1

  if pumpVal > 0:
    print("PUMPING: %s" % pumpVal)
    pumpAcid.Pump(pumpVal)
  Log(storage_path_pumpAcid,pumpVal)


def Goodbye():
  global run
  print("Goodbye")
  run = False


def main():
  print("Hello there")
  
  schedule.every(1).minutes.do(PHLong)
  schedule.every(30).minutes.do(PumpBaseLong)
  schedule.every(30).minutes.do(PumpAcidLong)
  schedule.every().day.at("23:55").do(Goodbye)
  
  try:
    while run:
      schedule.run_pending()
      time.sleep(1)
  except KeyboardInterrupt:     # catches the ctrl-c command, which breaks the loop above
    print("Continuous polling stopped")

if __name__ == '__main__':
  main()




