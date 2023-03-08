from sense_hat import SenseHat
import time

"""

  Sense HAT Sensors Display
  
  Select Temperature, Pressure, or Humidity  with the Joystick
  to visualize the current sensor values on the LED.
  
  Note: Requires sense_hat 2.2.0 or later

"""

sense = SenseHat()

green = (0, 51, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
rose = (210,85,219)
black = (0,0,0)

ime = "Moji leukociti rastu!"

def moje_ime(ime,bg_colour,text_colour):
    for slovo in ime:
      sense.show_letter(slovo, back_colour = bg_colour, text_colour = text_colour)
      time.sleep(.5)

def update_screen(mode):
  bg_colour = red
  txt_colour = green

  if mode == "temp":
    temp = sense.temp
    
    if temp > 90:
        bg_colour = rose
        txt_colour = black
    elif temp > 60:
        bg_colour = green
        txt_colour = white
    elif temp > 20:
        bg_colour = blue
        txt_colour = white
    else:
        bg_colour = white
        txt_colour = blue
        
  elif mode == "pressure":
    pressure = sense.pressure
    

  elif mode == "humidity":
    humidity = sense.humidity


####
# Intro Animation
####

  moje_ime(ime, bg_colour, txt_colour)

update_screen("temp")

index = 0
sensors = ["temp", "pressure", "humidity"]

####
# Main game loop
####

while True:
  selection = False
  events = sense.stick.get_events()
  for event in events:
    # Skip releases
    if event.action != "released":
      if event.direction == "left":
        index -= 1
        selection = True
      elif event.direction == "right":
        index += 1
        selection = True
      if selection:
        current_mode = sensors[index % 3]
        update_screen(current_mode, show_letter = True)
  
  if not selection:      
    current_mode = sensors[index % 3]
    update_screen(current_mode)


# ISPISATI IME POMICANJEM JOISTICKA:

####
# Using the joystick
####
sense.clear()



def ispisi_slovo(slovo):
      sense.show_letter(slovo, back_colour = green, text_colour = white)
      sleep(.5)
      
ime = "IVANA"
index = 0 

while True:
  for event in sense.stick.get_events():
    print(event.direction, event.action)
    #for slovo in ime:
    # Check if the joystick was pressed
    
    if event.action == "pressed":
        
        # Check which direction
        if event.direction == "up":
          index += 1
          #sense.show_letter(index)      # Up arrow
        elif event.direction == "down":
          index -= 1
          #sense.show_letter(index)      # Down arrow
        elif event.direction == "left": 
          index -= 2
          #sense.show_letter(ime[2])      # Left arrow
        elif event.direction == "right":
          index += 2
          #sense.show_letter(ime[3])      # Right arrow
        elif event.direction == "middle":
          index = 0
          #sense.show_letter("M")      # Enter key
        
        # Wait a while and then clear the screen
        sleep(0.3)
        index = index%len(ime)
        ispisi_slovo(ime[index])
        
        sense.clear()
  ispisi_slovo(ime[index])
  