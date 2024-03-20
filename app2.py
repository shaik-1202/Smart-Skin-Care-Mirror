import serial
import cv2

ser=serial.Serial('COM3',9600,timeout=0.5)
while True:
  while(ser.inWaiting()>0):
    val=ser.read()
    val=val.decode('utf-8')
    if val == "1":
      pass
      vid=cv2.VideoCapture(0)
      while(True): 
          ret, frame = vid.read() 
          cv2.imshow('frame', frame) 
          if cv2.waitKey(3) & 0xFF == ord('q'): 
              break
      vid.release() 
      cv2.destroyAllWindows() 