import subprocess
from evdev import InputDevice, list_devices, UInput, ecodes as e

def get_event_number(device_name) -> str:
    print("Getting device number...")
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if device.name == device_name:
            return device.path.split("/")[-1]

    print("Device not found:", device_name)
    return ""

device_name = "BTL Gaming Mouse Consumer Control"
event_number = get_event_number(device_name)

if event_number:
    print(f"Found: {event_number}")
    mouse_path = f"/dev/input/{event_number}"
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