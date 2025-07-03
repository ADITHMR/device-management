# import machine
# try:
#     uart = machine.UART(0, baudrate=111284, bits=8)
# except:
#     pass
from machine import Pin

from drivers.oled import oled_log, oled_two_data
import gc

# Define touch pins
TOUCH1 = Pin(14, Pin.IN)
TOUCH2 = Pin(15, Pin.IN)

# Flags
is_AP = False
is_Server = False
is_update_proj = False

try:
    if TOUCH1.value() and TOUCH2.value():
        is_AP = True
        oled_two_data(1, 2, "Starting", "Access Point")
        
    elif TOUCH1.value() and not TOUCH2.value():
        is_Server = True
        oled_two_data(2, 2, "Starting", "Server")
    elif not TOUCH1.value() and TOUCH2.value():
        is_update_proj = True
        oled_two_data(2, 2, "Project", "Updating")

    

except Exception as e:
    print("Error Starting getting touch inputs() --import files error:", e)

gc.collect()  # Free memory after initialization
import json
import time

from drivers.oled import oled_log, oled_two_data
from local_host.connect_wifi import connect_wifi
from local_host.esp_as_AP import runAP
from local_host.webServer import runWebServer
from ota_update import run_update
from process.save_html import save_html



try:
    if TOUCH1.value() and TOUCH2.value():
        print("1")
        is_AP = True
        oled_two_data(1, 1, "Starting", "Access Point")
        print("2")
    elif TOUCH1.value() and not TOUCH2.value():
        is_Server = True
        oled_two_data(1, 2, "Starting", "Server")
    elif not TOUCH1.value() and TOUCH2.value():
        is_update_proj = True
        oled_two_data(1, 1, "Project", "Update")
    else:
        oled_two_data(1, 1, "System", "Booting")

except Exception as e:
    print("Error boot() --import files error:", e)

gc.collect()  # Free memory after initialization

# Start Access Point Mode if required
if is_AP:
    try:
        runAP()
    except Exception as e:
        print("Error RUNAP() RunAP:", e)

# Connect to Wi-Fi
wifi_connected = connect_wifi()

# Start Web Server if required
if is_Server and wifi_connected:
    oled_two_data(1, 1, "Web server", "Mode")
    oled_log("Web Server")
    runWebServer()

# Update Project if required
if is_update_proj and wifi_connected:
    gc.collect()

    from process.api import Api  # Import only when needed

    api = Api()
    if api.user_login():
        oled_two_data(1, 1, "User", "Logged in")
        oled_two_data(1, 1, "Aquiring", "Projects")
        api.get_projects()
        oled_two_data(1, 1, "Aquire", "Completed")
    else:
        oled_two_data(1, 1, "Login", "Failed")

    gc.collect()
    oled_two_data(1, 1, "Updating", "Pages")
    save_html()

gc.collect()  # Free memory before reading large files

# Check for software updates
if wifi_connected:
    try:
        with open('schema.dat', 'r') as f:
            update_flag = json.load(f).get("update_flag", "False")
        print("update_status=", update_flag)

        if update_flag == "True":
            oled_two_data(1, 1, "Starting", "Update")
            run_update()

    except Exception as e:
        print("Error reading update flag:", e)

oled_two_data(1, 1, "Starting", "Activities")

gc.collect()  # Final memory cleanup
