import time

import adafruit_irremote
import board
import pulseio

IR_PIN = board.D3  # Pin connected to IR receiver.

print('IR listener')
print()
# Create pulse input and IR decoder.
pulses = pulseio.PulseIn(IR_PIN, maxlen=200, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

aura_map = (
"brightness up",
"brightness down",
"off",
"on",
"red",
"green",
"blue",
"white",
"red-orange",
"light green",
"duke blue",
"flash",
"orange",
"carolina blue",
"purple",
"strobe",
"light orange",
"turquiose",
"light purple",
"fade",
"yellow",
"sea green",
"pink",
"smooth"
)

remote_map = {}

# Loop waiting to receive pulses.
for button in aura_map:
    # make sure pulses is empty
    # small delay for cleaner results
    pulses.clear()
    pulses.resume()
    time.sleep(.1)

    print("Please press %s key" % button)
    # Wait for a pulse to be detected.
    detected = decoder.read_pulses(pulses)

    # print the number of pulses detected
    # note: pulse count is an excellent indicator as to the quality of IR code
    # received.
    #
    # If you are expecting 67 each time (Adafruit Mini Remote Control #389)
    # and only receive 57 this will result in a incomplete listener

    if len(detected) == 67:
        remote_map[button] = detected

for button in remote_map:
    print("%s: %s," % (button,remote_map[button]))
