from machine import Pin
import time

class relay:
  def __init__(self):

    self.turn = 0

    self.rele = Pin(0,Pin.OUT)
    self.rele.high()
  
    self.pulse = Pin(2,Pin.IN)
  
  def callback(self,p):
      #para as interrupcoes
      self.pulse = Pin(2,Pin.IN,Pin.PULL_UP)
      #debug
      print("Interrupt!")
      if self.turn == 1:
          val =  self.rele.value()
          if val > 0:
              self.rele.low()
          else:
              self.rele.high()
          self.turn = 0
      else:
          self.turn += 1
      time.sleep_ms(1000)
      self.pulse = Pin(2,Pin.IN)

  def start(self):  
    self.pulse.irq(trigger=Pin.IRQ_RISING,handler=self.callback)    
     
  
