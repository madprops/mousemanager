import time
from evdev import InputDevice, list_devices, UInput, ecodes as e

device_name = "BTL Gaming Mouse"

def get_event_number(name) -> str:
    devices = [InputDevice(path) for path in list_devices()]

    for device in devices:
        if device.name == name:
            return device.path.split("/")[-1]

    print("Device not found:", name)
    return ""

def start_listener(num):
    print(f"Starting listener ({num})")
    mouse_path = f"/dev/input/{num}"
    mouse = InputDevice(mouse_path)
    direction = ""
    last_direction = 0
    ui = UInput()

    for event in mouse.read_loop():
        if event.type == e.EV_REL and event.code == e.REL_WHEEL:
            if event.value > 0:
                if direction == "down":
                    if last_direction:
                        if (time.time() - last_direction) < 0.1:
                            continue

                direction = "up"
                last_direction = time.time()
            elif event.value < 0:
                if direction == "up":
                    if last_direction:
                        if (time.time() - last_direction) < 0.1:
                            continue

                direction = "down"
                last_direction = time.time()
        else:
            ui.write(event.type, event.code, event.value)
            ui.syn()

event_number = get_event_number(device_name)

if event_number:
    start_listener(event_number)
else:
    print("Failed to find event number")