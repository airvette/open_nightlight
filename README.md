# open_nightlight
A nightlight that senses the environment and provides light when it is needed.

How to use code
- Lacking a more sophisticated method, overwrite the code.py file on the Circuit Python board with [code.py](https://github.com/airvette/open_nightlight/blob/master/code.py)
- Make sure to check out the [Adafruit page on the Mu editor](https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code) if you don't know how to navigate Circuit Python

Uses the Adafruit Metro M0 Express
- Seeks to integrate a Circuit Python capable board, PIR sensor, NeoPixel strip, photodiode and other components to produce a helpful and somewhat environment-aware light.

To Do
- [ ] Clean up code by getting rid of dead code
- [ ] Integrate photodiode
- [x] Create a ramp_up function for the light to increase nicely
- [ ] Create a ramp_down function for the light to decrease nicely
- [ ] On/off power toggle switch
- [ ] Produce a fritzing file that captures what a standalone package would look like (not the prototyping layout)
- [ ] Introde a mode selector switch to enable different modes of operation
