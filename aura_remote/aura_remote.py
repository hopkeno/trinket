"""
Control the onbard dotstar led using the aura led mood light remote
"""

import time
import adafruit_irremote
import board
import pulseio
import adafruit_dotstar as dotstar
import auraremote_buttonmap

ir_pin = board.D3  # pin connected to IR receiver.
dot_state = "boot"
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
dot.brightness = 0.0

fuzzyness = 0.2  # IR remote timing must be within 20% tolerance
ir_length = 67   # Length of IR signal sequence. Should be 67 timings for this aura remote
buttons = auraremote_buttonmap.init()

def fuzzy_pulse_compare(received):
    # total count of IR code matches for each button {0, 1, 2, 3..23}
    match_count = [0] * len(buttons)
    # Did we receive a full IR code?
    if len(received) == ir_length:
        # compare received IR code with our stored buttons list
        for b_index, button_press in enumerate(buttons.values()):
            # compare individual timings for each IR code
            # confirm that every entry is within fuzzyness 20% accuracy
            for i, press in enumerate(button_press):
                threshold = int(press * fuzzyness)
                if abs(press - received[i]) < threshold:
                    match_count[b_index] += 1
    if max(match_count) == ir_length:
        return get_button_name(list(buttons.values())[match_count.index(max(match_count))])

def get_button_name(received):
    for name,code in buttons.items():
        if received == code:
            return name

# Create pulse input and IR decoder.
pulses = pulseio.PulseIn(ir_pin, maxlen=200, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

# Loop waiting to receive pulses.
i = 0
while True:
    # total count of IR code matches for each button {0, 1, 2, 3..23}
    match_count = [0] * len(buttons)

    # make sure pulses is empty
    pulses.clear()
    pulses.resume()
    time.sleep(.1)

    # Wait for a pulse to be detected.
    detected = decoder.read_pulses(pulses)
    action = fuzzy_pulse_compare(detected)

    # confirm that we know this button
    # received IR code compared with saved button_presses
    # 100% match (+/- fuzziness)
    # otherwise we don't know this button pressed
    if action:
        print(action)
        if dot_state == "off" or dot_state == "boot":
            if action == "on":
                dot.brightness = 0.2
                if dot_state == "boot":
                    dot[0] = (255,255,255)
                dot_state = "on"
        else:
            if action == "brightness up":
                if dot.brightness <= .9:
                    dot.brightness += .1
                    print("brightness increased to %.1f" % dot.brightness)
            elif action == "brightness down":
                if dot.brightness >= .1:
                    dot.brightness -= .1
                    print("brightness decreased to %.1f" % dot.brightness)
            elif action == "off":
                dot.brightness = 0.0
                dot_state = "off"
            elif action == "red":
                dot[0] = (255,0,0)
            elif action == "green":
                dot[0] = (0,255,0)
            elif action ==  "blue":
                dot[0] = (0,0,255)
            elif action == "white":
                dot[0] = (255,255,255)
            elif action == "duke blue":
                dot[0] = (0,83,155)
            elif action == "orange":
                dot[0] = (205,102,0)
            elif action == "carolina blue":
                dot[0] = (123,175,233)
            elif action == "purple":
                dot[0] = (82,45,128)
            else:
                if action in buttons.keys():
                    print("%s not yet implemented" % action)
                else:
                    print("unknown button")

    i = (i+1) % 256  # run from 0 to 255
