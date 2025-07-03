import gc
from utils import url_decode, put_jsonvalue_to_file, set_wifi_credentials
from time import sleep
from drivers.display import disp_scroll_str
from machine_id import get_serial_no
from drivers.oled import *
import json

try:
    import usocket as socket
except ImportError:
    import socket

import picoweb
import network
import time

from local_host.connect_wifi import connect_wifi

app = picoweb.WebApp(__name__)
REPLACE_FOR_SPACE = "@@!##"

def enable_AP():
    oled_log('Access point')
    oled_log('Please wait...')
    disp_scroll_str('Access point')

    sleep(1)

    ssid = get_serial_no()
    password = '123456789'

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    ap.ifconfig(('192.168.10.1', '255.255.255.0', '192.168.1.1', '192.168.1.1'))
    
    sleep(1)
    while not ap.active():
        pass
    
    ip_addr = ap.ifconfig()[0]
    disp_scroll_str(f'IP-{ip_addr.replace(".","-")}')
    oled_log('Connect to "Prosol AP"')
    oled_log(f'IP-> {ip_addr}')
    
    print(f'Connection successful: {ip_addr}')
    
    gc.collect()  # Free up memory

@app.route("/")
def index(req, resp):
    if req.method == "GET":
        try:
            with open("local_host/credentials.html", 'r') as f:
                yield from picoweb.start_response(resp)
                while True:
                    chunk = f.read(512)  # Read in small chunks
                    if not chunk:
                        break
                    yield from resp.awrite(chunk)
        except Exception as e:
            print("Error loading index page:", e)
        finally:
            gc.collect()

@app.route("/submit")
def submit(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
        data = req.form
        data_str = json.dumps(data).replace("'", '"')
        json_data = json.loads(data_str)

        wifi_ssid = json_data.get("ssid", "")
        wifi_password = json_data.get("wifi-password", "")
        username = json_data.get("email", "")
        userpassword = json_data.get("password", "")

        set_wifi_credentials(wifi_ssid, wifi_password)
        put_jsonvalue_to_file("schema.dat", "username", username)
        put_jsonvalue_to_file("schema.dat", "password", userpassword)

        yield from picoweb.start_response(resp, content_type="text/html")
        
        # Stream response instead of storing it in memory
        yield from resp.awrite("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Submission Successful</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #121212; color: #fff; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
                .form-container { background-color: #1e1e1e; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5); width: 100%; max-width: 400px; text-align: center; }
                .main-heading { font-size: 2.5rem; font-weight: bold; color: #00bcd4; margin-bottom: 1.5rem; }
                h2 { color: #fff; margin-bottom: 1.5rem; }
                p { font-size: 1.1rem; color: #bbb; }
                .back-button { margin-top: 1rem; padding: 0.75rem; background-color: #00bcd4; color: white; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; transition: background-color 0.3s; }
                .back-button:hover { background-color: #008ba3; }
            </style>
        </head>
        <body>
            <div class="form-container">
                <div class="main-heading">roboNinjaz</div>
                <h2>Form Submitted Successfully!</h2>
        """)
        
        yield from resp.awrite(f"<p><strong>WiFi SSID:</strong> {wifi_ssid}</p>")
        yield from resp.awrite(f"<p><strong>WiFi Password:</strong> {wifi_password}</p>")
        yield from resp.awrite(f"<p><strong>Email ID:</strong> {username}</p>")
        yield from resp.awrite(f"<p><strong>Password:</strong> {userpassword}</p>")
        
        yield from resp.awrite("""
                <h1>Restart the device!</h1>
            </div>
        </body>
        </html>
        """)

        gc.collect()  # Free up memory after sending response

def runAP():
    enable_AP()
    app.run(debug=True, host="0.0.0.0", port=80)
    gc.collect()  # Final cleanup
