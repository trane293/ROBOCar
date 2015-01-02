# AUTHOR - Anmol Sharma
# LANGUAGE - Python
# DATE CREATED - 1 March, 2013
# DATE LAST MODIFIED - 6 March 2013
# DESCRIPTION - A Working script for my project "ROBO Car", achieved using Raspberry Pi and controlled using
# Wii Mote's accelerometer
# LICENSE - The following code is released under GNU General Public License. You MAY use, reuse, edit, add, 
# ommit the code however you want. I just require you to respect the original efforts and give due credit to the 
# original author Anmol Sharma in your code, or in anywhere else where you may use or demonstrate your project 
# using this code snippet
 

import RPi.GPIO as GPIO #Used RPi.GPIO library as wiringpi didn't quite work well for me, wiringpi is easier
import time
import os
import cwiid #Main library for Wii Mote interfacing, don't forget to include this!
import time
prev_input = 0 #Use this variable to make sure the button press is registered only ONCE, not many times as it bounces
GPIO.setmode(GPIO.BOARD) #I use the GPIO.BOARD mode for pin numberings, you can use BCM as well
#----------------------------------------------------------------------------
#This is unnecessary code, use only for
#Troubleshooting purposes by attaching 4 buttons   
#to the four GPIO pins mentioned here
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Forward button  
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Right button   
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Left button    
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Reverse button
#All the inputs are PULLED DOWN INTERNALLY, NO EXTERNAL RESISTOR USED. RPI HAS ITS OWN INTERNAL PUD RESISTORS
#BE AWARE OF THIS FACT
#----------------------------------------------------------------------------
#Setting up Output pins to get the 3.3V logic output to feed to the L293D Motor Controller
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW) #IN1 
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW) #IN2
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW) #IN3
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW) #IN4
#Refer to the L293D motor controller Pinouts to know more about it's logic
button_delay = 0.1 #Just another variable

#Wii Mote connection code begins here
print 'Press 1 + 2 on your Wii Remote now ...' #Puts the Wii mote in bluetooth discoverable mode, don't change it.
time.sleep(1) #wait for a second
wii= None 
i=2
#Connect to the Wii Remote. If it times out
#then quit.
while not wii: #Check if its connected or not
 try:
  wii=cwiid.Wiimote() #Function call to know if Wii mote has connected or not
 except RuntimeError:
  if (i>10): #Attempt to connect to Wii mote 10 times because it may fail
   quit()
   break
  print "Error opening wiimote connection"
  print "attempt " + str(i)
  i +=1 
print 'Wii Remote connected...\n'
print 'Press some buttons!\n'
#Just another method to quit the script
print 'Press PLUS and MINUS together to disconnect and quit.\n'
#You can leave this out if you want
 
wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC #Report BOTH button presses as well as Accelerometer readings
 
while True: #Infinite Loop
 
  buttons = wii.state['buttons'] #Useless in my project, I didn't use any button input
 
  #If Plus and Minus buttons pressed
  #together then rumble and quit.
  #Again, you MAY leave this out
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
    print '\nClosing connection ...'
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    exit(wii)
  #Again, this code is for TROUBLESHOOTING purposes only, needed only if you intend to use 4 physical 
  #buttons to test the inputs from the Pi. Although this is very helpful and I recommend you SHOULD use this
  fow = GPIO.input(13)
  rit = GPIO.input(15)
  lef = GPIO.input(19)
  rev = GPIO.input(21)
  #Ofcourse the Initial states of the output pins are set to Low, to avoid any problems. 
  #Be SURE TO put this code INSIDE the infinite loop, as putting in outside will set the pins HIGH and THEY 
  #WILL REMAIN HIGH FOREVER 
  GPIO.output(26, GPIO.LOW)
  GPIO.output(24, GPIO.LOW)
  GPIO.output(22, GPIO.LOW)
  GPIO.output(18, GPIO.LOW)
  #I found out that the Wii Accelerometer centered at 125 when put on a flat desk, so [0] is x axis, [1] is y axis
  #I used 110 and 140 instead of 125 to make some room and to lower the senstivity, else if you use 125 on all
  #cases, the Wii mote will be ultra sensitive

  #Again, to understand the code below, you HAVE to be aware of the L293D motor controller's logic and schematics,
  #Do go through it if you haven't yet
  if (wii.state['acc'][0] < 110) :
     print("Forward Button pressed")
     GPIO.output(22, GPIO.HIGH)
     GPIO.output(24, GPIO.HIGH)
     time.sleep(0.05)
     time.sleep(button_delay)
  if (wii.state['acc'][1] > 140):
     print("Right button pressed")
     GPIO.output(24, GPIO.HIGH)
     GPIO.output(18, GPIO.HIGH)
     time.sleep(0.05)
     time.sleep(button_delay)
  if (wii.state['acc'][1] < 110):
     print("Left button pressed")
     GPIO.output(22, GPIO.HIGH)
     GPIO.output(26, GPIO.HIGH)
     time.sleep(0.05)
     time.sleep(button_delay)
  if (wii.state['acc'][0] > 140 ) :
     print("Reverse button pressed")
     GPIO.output(26, GPIO.HIGH)
     GPIO.output(18, GPIO.HIGH)
     time.sleep(0.05)
     time.sleep(button_delay)
  else:
     continue
