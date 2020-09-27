import time
import board
import neopixel  # for neopixels
import digitalio  # for pir sensor


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.D6

# On a Raspberry pi, use this instead, not all pins are supported
# pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 30

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# PIR Sensor Setup
LED_PIN = board.D13  # Pin number for the board's built in LED.
PIR_PIN = board.D2   # Pin number connected to PIR sensor output wire.
LED_TIMEOUT = 10  # Number of seconds from time of last detection to turning off LEDs

# Setup digital input for PIR sensor:
pir = digitalio.DigitalInOut(PIR_PIN)
pir.direction = digitalio.Direction.INPUT

# Setup digital output for LED:
led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT

last_detection = time.monotonic()

old_value = pir.value


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


def ramp_up(final_color, ramp_length):
    # Ramp from (0, 0, 0) to a final color over the period specified in ramp_length
    
    # Find the ramp slopes for each color
    red_step_size = int(final_color[0]/ramp_length)
    green_step_size = int(final_color[1]/ramp_length)
    blue_step_size = int(final_color[2]/ramp_length)
    
    step_time = .05 # this is the pause between steps in seconds
    number_cycles = int(ramp_length/step_time)
    rgb_value = [0, 0, 0]
    for i in range(number_cycles):
        rgb_value[0] = rgb_value[0] + int(red_step_size * step_time)
        rgb_value[1] = rgb_value[1] + int(green_step_size * step_time)
        rgb_value[2] = rgb_value[2] + int(blue_step_size * step_time)
        pixels.fill(rgb_value)
        pixels.show()
        time.sleep(step_time)


while True:
    '''
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0, 0))
    pixels.show()
    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
    pixels.show()
    time.sleep(1)
    '''

    #rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step

    pir_value = pir.value
    if pir_value:
        # PIR is detecting movement! Turn on LED.
        led.value = True
        #pixels.fill((255, 0, 0))
        #pixels.show()
        ramp_up((255, 0, 0), 3)
        # Check if this is the first time movement was
        # detected and print a message!
        if not old_value:
            now = time.monotonic()
            time_since_detection = now - last_detection
            last_detection = now
            print('Motion detected! Time since last detection: {}s'.format(time_since_detection))
    else:
        now = time.monotonic()
        time_since_detection = now - last_detection
        if time_since_detection > LED_TIMEOUT:
            # PIR is not detecting movement. Turn off LED.
            led.value = False
            pixels.fill((0, 0, 0))
            pixels.show()
        # Again check if this is the first time movement
        # stopped and print a message.
        if old_value:
            print('Motion ended!')
    old_value = pir_value
