"""
Control the onbard dotstar led using the aura led mood light remote
"""

import time
import adafruit_irremote
import board
import pulseio
import adafruit_dotstar as dotstar
import auraremote_buttonmap as aura

ir_pin = board.D3  # pin connected to IR receiver.
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
dot.brightness = 0.0
dot_state = False

fuzzyness = 0.2  # IR remote timing must be within 20% tolerance
ir_length = 67   # Length of IR signal sequence. Should be 67 timings for this aura remote

def fuzzy_pulse_compare(received):
    # total count of IR code matches for each button {0, 1, 2, 3..23}
    match_count = [0] * len(aura.buttons)
    # Did we receive a full IR code?
    if len(received) == ir_length:
        # compare received IR code with our stored buttons list
        for b_index, button_press in enumerate(aura.buttons.values()):
            # compare individual timings for each IR code
            # confirm that every entry is within fuzzyness 20% accuracy
            for i, press in enumerate(button_press):
                threshold = int(press * fuzzyness)
                if abs(press - received[i]) < threshold:
                    match_count[b_index] += 1
    if max(match_count) == ir_length:
        return get_button_name(list(aura.buttons.values())[match_count.index(max(match_count))])

def get_button_name(received):
    for name,code in aura.buttons.items():
        if received == code:
            return name

# Create pulse input and IR decoder.
pulses = pulseio.PulseIn(ir_pin, maxlen=200, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

# Loop waiting to receive pulses.
i = 0
while True:
    # total count of IR code matches for each button {0, 1, 2, 3..23}
    match_count = [0] * len(aura.buttons)

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
    if action in aura.buttons:
        if not dot_state:
            if action == "on":
                dot.brightness = 0.2
                dot[0] = aura.colors["white"]
                dot_state = True
                print("power on with color=white and brightness=%.1f" % dot.brightness)
        else:
            if action == "brightness up":
                if dot.brightness <= .9:
                    dot.brightness += .1
                    print("brightness increased to %.1f" % dot.brightness)
            elif action == "brightness down":
                if dot.brightness >= .1:
                    dot.brightness -= .1
                    print("brightness decreased to %.1f" % dot.brightness)
            elif action == "on":
                #if already on, turn off instead
                dot.brightness = 0.0
                dot_state = False
                print("power off")
            elif action == "flash" or action == "strobe" or action == "fade" or action == "smooth":
                print("%s not implemented" % action)
            else:
                print(action)
                dot[0] = aura.colors[action]
    else:
        print("unknown or not implemented button")

    i = (i+1) % 256  # run from 0 to 255
