import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

import digitalio
import board

class HID_Device():

  def __init__(self):

    self.running = True

    # Power LED on
    self.led = digitalio.DigitalInOut(board.LED)
    self.led.direction = digitalio.Direction.OUTPUT
    self.led.value = True

    # USB HID
    print("HID Keyboard Init")
    self.keyboard = Keyboard(usb_hid.devices)

    # Setup switches
    self.footswitches = {'a': {'pin': digitalio.DigitalInOut(board.GP13), 'last_state': -1, 'last_trigger': time.monotonic(), 'keycode': Keycode.F20}}
    for key, value in self.footswitches.items():
      value['pin'].switch_to_input(pull=digitalio.Pull.UP)

    # Watch the buttons
    self.switch_loop()

  def switch_loop(self):

    while self.running:

      # Check the switches
      for key, switch in self.footswitches.items():
        current_value = switch['pin'].value
        #print(str(current_value))

        # Only trigger on press
        if current_value == 0 and switch['last_state'] == 1 and switch['last_state'] != -1:

          # Debounce
          if time.monotonic() - switch['last_trigger'] > 0.1:
            print("Footswitch '" + key + '" triggered!, sending "' + str(switch['keycode']) + '"...')
            self.keyboard.send(switch['keycode'])
            switch['last_trigger'] = time.monotonic()

        switch['last_state'] = current_value


HID_Device()
