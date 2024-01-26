#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Raspberry Pi to Arduino Serial Communication
#
# Reference 
# arduino library
#     https://www.arduino.cc/reference/en/language/functions/communication/serial/
# pyserial 
#     https://pyserial.readthedocs.io/en/latest/pyserial.html

import serial
import time

def main() :
  ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
  ser.flush()
  print(ser.name)

  while True:
    ser.write(b'a')
    if ser.in_waiting > 0:
      line = ser.readline().decode('utf-8').rstrip()
      print(line)
      file1 = open("data.txt","a")
      line2 = str(line) + " \n"
      file1.write(line2)
      file1.close()
    time.sleep(1)

  ser.close()

if __name__ == '__main__':
  try:
    main()
  except (KeyboardInterrupt):
    pass
