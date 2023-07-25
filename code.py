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
    self.footswitches = {'a': {'pin': digitalio.DigitalInOut(board.GP13), 'last_state': -1, 'last_trigger': time.monotonic_ns(), 'keycode': Keycode.F20, 'blocked': False}}
    for key, value in self.footswitches.items():
      value['pin'].switch_to_input(pull=digitalio.Pull.UP)

    # Watch the buttons
    self.switch_loop()

  def switch_loop(self):

    while self.running:

      # Check the switches
      for key, switch in self.footswitches.items():
        current_value = switch['pin'].value
#        print(str(current_value))

        # If the switch opens unblock
        if current_value == 1 and switch['last_state'] == 0:
          switch['blocked'] = False

        # If the switch closes start the debounce timer
        if current_value == 0 and switch['last_state'] == 1 and switch['last_state'] != -1 and not switch['blocked']:
          switch['last_trigger'] = time.monotonic_ns()

        # If pin state is now stable 
        if (time.monotonic_ns() - switch['last_trigger'] > (20 * 1000000)) and current_value == 0 and not switch['blocked']:
          print("Footswitch '" + key + '" triggered!, sending "' + str(switch['keycode']) + '"...')
          self.keyboard.send(switch['keycode'])
          switch['blocked'] = True

        switch['last_state'] = current_value

HID_Device()
