"""
Control the onbard dotstar led using the aura led mood light remote
"""

import time
import adafruit_irremote
import board
import pulseio
import adafruit_dotstar as dotstar

ir_pin = board.D3  # pin connected to IR receiver.
dot_state = "boot"
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
dot.brightness = 0.0


fuzzyness = 0.2  # IR remote timing must be within 20% tolerance

button_presses = [
[9050, 4462, 603, 526, 597, 532, 601, 528, 596, 533, 600, 532, 591, 535, 599, 529, 605, 524, 599, 1629, 596, 1632, 604, 1624, 601, 1628, 598, 531, 602, 1626, 599, 1629, 597, 1631, 604, 1624, 601, 1628, 598, 534, 599, 526, 597, 531, 603, 526, 597, 531, 602, 526, 597, 531, 603, 525, 598, 1629, 596, 1632, 603, 1625, 601, 1627, 598, 1629, 596, 1632, 604],
[9053, 4461, 602, 527, 596, 533, 601, 528, 595, 533, 600, 528, 595, 534, 599, 529, 595, 533, 600, 1628, 597, 1631, 605, 1624, 602, 1627, 598, 531, 602, 1626, 600, 1628, 597, 1632, 603, 526, 598, 1630, 595, 533, 600, 529, 604, 525, 603, 525, 604, 525, 599, 529, 604, 1624, 601, 529, 594, 1634, 602, 1626, 599, 1630, 606, 1624, 602, 1626, 599, 1630, 608],
[9084, 4458, 606, 524, 599, 531, 602, 529, 608, 521, 599, 531, 602, 528, 605, 524, 599, 531, 603, 1625, 600, 1628, 597, 1632, 604, 1625, 600, 529, 604, 1624, 601, 1628, 597, 1632, 604, 525, 598, 531, 602, 1626, 599, 530, 614, 515, 598, 531, 602, 526, 597, 532, 601, 1626, 600, 1629, 596, 533, 600, 1628, 597, 1631, 605, 1624, 601, 1627, 605, 1624, 605],
[9100, 4459, 605, 527, 606, 526, 600, 542, 589, 531, 603, 529, 604, 527, 596, 535, 599, 532, 601, 1629, 607, 1624, 602, 1629, 607, 1624, 601, 532, 601, 1629, 607, 1624, 601, 1630, 610, 1621, 601, 531, 602, 1628, 597, 534, 599, 532, 602, 529, 604, 527, 596, 535, 599, 533, 601, 1630, 605, 526, 598, 1632, 603, 1628, 598, 1633, 603, 1627, 598, 1633, 603],
[9071, 4453, 601, 531, 602, 530, 604, 527, 606, 525, 598, 532, 602, 529, 604, 525, 598, 531, 602, 1626, 599, 1629, 596, 1633, 603, 1626, 600, 530, 603, 1626, 599, 1631, 605, 1625, 599, 532, 602, 1628, 607, 1623, 603, 530, 603, 529, 605, 526, 607, 524, 599, 532, 601, 1629, 607, 525, 598, 533, 600, 1630, 606, 1625, 600, 1634, 601, 1628, 598, 1633, 602],
[9099, 4455, 599, 533, 600, 531, 603, 531, 602, 526, 597, 533, 601, 530, 611, 519, 596, 535, 599, 1630, 605, 1625, 600, 1631, 605, 1625, 600, 531, 602, 1627, 599, 1632, 603, 1627, 609, 1622, 604, 1626, 599, 1632, 604, 528, 605, 526, 597, 534, 600, 531, 602, 529, 605, 526, 597, 533, 600, 530, 604, 1625, 600, 1630, 606, 1624, 601, 1629, 596, 1633, 603],
[9124, 4456, 608, 525, 608, 525, 598, 535, 599, 534, 599, 534, 600, 533, 600, 532, 602, 531, 602, 1630, 606, 1627, 608, 1624, 601, 1632, 604, 530, 603, 1629, 607, 1626, 599, 1633, 603, 534, 599, 531, 603, 529, 604, 528, 607, 530, 602, 526, 607, 525, 598, 535, 607, 1624, 603, 1629, 610, 1623, 599, 1633, 602, 1631, 605, 1628, 607, 1625, 601, 1632, 603],
[9097, 4456, 597, 535, 599, 533, 600, 531, 603, 527, 596, 535, 598, 532, 602, 528, 605, 525, 599, 1631, 604, 1626, 610, 1621, 604, 1626, 599, 531, 603, 1626, 599, 1631, 605, 1625, 600, 1630, 605, 526, 597, 533, 601, 529, 604, 526, 597, 533, 601, 529, 604, 526, 597, 533, 600, 1629, 597, 1633, 606, 1625, 596, 1634, 602, 1628, 597, 1633, 603, 1627, 598],
[9065, 4460, 604, 536, 591, 528, 602, 528, 605, 525, 599, 532, 601, 529, 605, 525, 598, 532, 601, 1630, 606, 1625, 601, 1630, 606, 1626, 600, 529, 605, 1626, 599, 1631, 605, 1626, 600, 1632, 604, 1627, 598, 1633, 603, 528, 605, 1627, 599, 532, 601, 530, 604, 527, 606, 526, 608, 523, 600, 532, 602, 1629, 607, 524, 599, 1633, 602, 1629, 607, 1625, 601],
]

button_name = [
"on",
"off",
"red",
"green",
"blue",
"white",
"brightness up",
"brightness down",
"smooth"
]

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

def fuzzy_pulse_compare(received):
    # Did we receive a full IR code?
    # Should be 67 timings for this remote
    if len(received) == len(button_presses[0]):

        # compare received IR code with our stored button_press list
        # remote control button codes for : [0-3]
        for b_index, button_press in enumerate(button_presses):

            # compare individual timings for each IR code
            # confirm that every entry is within fuzzyness 20% accuracy
            for i, press in enumerate(button_press):

                threshold = int(press * fuzzyness)

                if abs(press - received[i]) < threshold:
                    match_count[b_index] += 1

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return (0, 0, 0)
    if (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

# Create pulse input and IR decoder.
pulses = pulseio.PulseIn(ir_pin, maxlen=200, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

# Loop waiting to receive pulses.
i = 0
while True:
    # total count of IR code matches for each button {0, 1, 2, 3}
    match_count = [0] * len(button_presses)

    # make sure pulses is empty
    pulses.clear()
    pulses.resume()
    time.sleep(.1)

    # Wait for a pulse to be detected.
    detected = decoder.read_pulses(pulses)
    fuzzy_pulse_compare(detected)

    # confirm that we know this button
    # received IR code compared with saved button_presses
    # 100% match (+/- fuzziness)
    # otherwise we don't know this button pressed
    if max(match_count) == len(button_presses[0]):
        remote_control_press = match_count.index(max(match_count))
        print(button_name[match_count.index(max(match_count))])
        action = button_name[match_count.index(max(match_count))]
        if dot_state == "off" or dot_state == "boot":
            if action == "on":
                dot.brightness = 0.2
                if dot_state == "boot":
                    dot[0] = WHITE
                dot_state = "on"
        else:
            if action == "red":
                dot[0] = RED
            elif action == "green":
                dot[0] = GREEN
            elif action ==  "blue":
                dot[0] = BLUE
            elif action == "white":
                dot[0] = WHITE
            elif action == "off":
                dot.brightness = 0.0
                dot_state = "off"
            elif action == "brightness up":
                if dot.brightness <= .9:
                    dot.brightness += .1
                    print("brightness increased to %.1f" % dot.brightness)
            elif action == "brightness down":
                if dot.brightness >= .1:
                    dot.brightness -= .1
                    print("brightness decreased to %.1f" % dot.brightness)
            elif action == "smooth":
                #need to figure out a way to keep the loop going until new input
                dot[0] = wheel(i & 255)
    else:
        print("unknown button")

    i = (i+1) % 256  # run from 0 to 255
