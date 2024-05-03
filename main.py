import subprocess
from evdev import InputDevice, list_devices, UInput, ecodes as e

device_name_1 = "BTL Gaming Mouse"
device_name_2 = "BTL Gaming Mouse Consumer Control"

def get_input_number(device_name) -> str:
    devices = subprocess.run("xinput list", shell=True, capture_output=True).stdout.decode().split("\n")

    for device in devices:
        if device_name in device:
            return device.split("id=")[-1].split("\t")[0]

    print("Device not found:", device_name)
    return ""

def get_event_number(device_name) -> str:
    devices = [InputDevice(path) for path in list_devices()]

    for device in devices:
        if device.name == device_name:
            return device.path.split("/")[-1]

    print("Device not found:", device_name)
    return ""

def start_listener(num):
    print(f"Starting listener ({num})")
    mouse_path = f"/dev/input/{num}"
    mouse = InputDevice(mouse_path)
    cap = {e.EV_KEY: [e.KEY_ESC, e.KEY_LEFTMETA, e.KEY_LEFTCTRL, e.KEY_SPACE]}
    ui = UInput(cap, name="virtual-device")
    mouse.grab()

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

def setup_buttons(num):
    print(f"Setting up buttons ({num})")
    cmd = f"xinput set-button-map {num} 3 2 1 4 5 6 7 8 9"
    subprocess.run(cmd, shell=True)

input_number = get_input_number(device_name_1)

if input_number:
    setup_buttons(input_number)
else:
    print("Failed to find input number")

event_number = get_event_number(device_name_2)

if event_number:
    start_listener(event_number)
else:
    print("Failed to find event number")