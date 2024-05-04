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
    ui = UInput.from_device(mouse)

    direction = ""
    prev_direction = ""
    last_time = 0

    for event in mouse.read_loop():
        if event.type == e.EV_REL and event.code == e.REL_WHEEL:
            now = time.time()
            duration = now - last_time

            if duration >= 1:
                direction = ""
                prev_direction = ""
                last_time = 0

            prev_direction = direction

            if event.value > 0:
                direction = "up"
            elif event.value < 0:
                direction = "down"

            if (prev_direction and direction) and (prev_direction != direction):
                if duration < 0.1:
                    direction = "up" if direction == "down" else "down"
                    value = 1 if direction == "up" else -1
                    ui.write(event.type, event.code, value)
                    ui.syn()
            else:
                last_time = now
        elif not e.EV_REL:
            ui.write(event.type, event.code, event.value)
            ui.syn()

event_number = get_event_number(device_name)

if event_number:
    try:
        start_listener(event_number)
    except KeyboardInterrupt:
        pass
else:
    print("Failed to find event number")