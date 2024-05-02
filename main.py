from evdev import InputDevice, UInput, ecodes as e
from time import sleep

mouse_path = "/dev/input/event4"
mouse = InputDevice(mouse_path)
cap = {e.EV_KEY: [e.KEY_ESC, e.KEY_LEFTMETA, e.KEY_LEFTCTRL, e.KEY_SPACE]}
ui = UInput(cap, name="virtual-device")
mouse.grab()
print("Started")

try:
    for event in mouse.read_loop():
        if event.type == e.EV_KEY:
            if event.code == 115 and event.value == 1:
                ui.write(e.EV_KEY, e.KEY_LEFTMETA, 1)
                ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 1)
                ui.write(e.EV_KEY, e.KEY_SPACE, 1)
                ui.syn()

                ui.write(e.EV_KEY, e.KEY_SPACE, 0)
                ui.write(e.EV_KEY, e.KEY_LEFTCTRL, 0)
                ui.write(e.EV_KEY, e.KEY_LEFTMETA, 0)
                ui.syn()
            elif event.code == 114:
                ui.write(e.EV_KEY, e.KEY_ESC, event.value)
                ui.syn()
except KeyboardInterrupt:
    pass