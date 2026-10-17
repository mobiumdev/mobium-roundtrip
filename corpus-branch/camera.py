"""The branch case: a client script with a conditional a test file cannot hold.

MobiumApp's Dialog Demo asks for the camera. Android shows its prompt only
while the permission is not yet decided, so the script answers the prompt if
it comes and goes on if it does not, then asserts the app was granted it.
The device's state picks the path: `mobium reset-permissions` gives the
prompt, `mobium grant ... camera` does not. On iOS the prompt's yes is
"Allow"; on Android, "While using the app".

usage: python3 camera.py TRACE.zip [DEVICE]   (MOBIUM_BIN_PATH names the binary;
       DEVICE defaults to emulator-5554, and a simulator's UDID means iOS)
"""
import sys
import time

from mobium import start

APP = "dev.mobium.mobiumapp"
DEVICE = sys.argv[2] if len(sys.argv) > 2 else "emulator-5554"
IOS = DEVICE.count("-") == 4
ALLOW = "Allow" if IOS else "While using the app"

with start(platform="ios" if IOS else "android", device=DEVICE, app=APP) as device:
    device.trace_start(name="camera.py › the camera is granted, asked or not")
    try:
        device.terminate(APP)
        device.launch(APP)
        device.tap("label=Dialog Demo")
        device.tap("testid=cameraBtn")
        # The prompt comes a moment after the tap, if it comes at all.
        end = time.time() + 3
        while time.time() < end:
            if device.alert():
                device.press_alert_button(ALLOW)
                break
            time.sleep(0.25)
        # The outcome is at the top of the list, scrolled away by the tap.
        device.scroll_to("testid=dialogOutcome", direction="up")
        device.wait_for("testid=dialogOutcome", condition="text", text="camera: granted", exact=True)
    finally:
        device.trace_stop(sys.argv[1])
