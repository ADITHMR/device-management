import network
from drivers.oled import *
from drivers.display import *
from process.file_mgr import *
import time
from utils import get_wifi_credentials


# Global variable for WiFi connection status
wifi_connected = False
wifi_connection_timeout = 10  # Timeout after 10 seconds
wifi_conn_start_time = time.time()

@micropython.native 
def connect_wifi(ssid=0,password=0):
    global wifi_connected  # Ensure we're using the global variable
    flag=1
    if ssid==0 or password==0:
        try:
            WIFI_SSID, WIFI_PASSWORD= get_wifi_credentials()
            print(f"connecting to {WIFI_SSID}")
         
        except :
            flag=0
            print("connect_wifi() :Error accessing wifi credentials")
            
        
    else:
        WIFI_SSID = str(ssid)
        WIFI_PASSWORD = str(password)
        print(f"connecting to{WIFI_SSID}")
       
    if flag==1:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        print('Connecting to WiFi...')
        oled_log("Conn to WiFi...")
        disp_scroll_str("CONNecting")
        wifi_conn_start_time = time.time()

        while not wlan.isconnected():
            oled_two_data(1, 2, "Conn to WiFi", str(wifi_connection_timeout - (time.time() - wifi_conn_start_time)))
            if (time.time() - wifi_conn_start_time) > wifi_connection_timeout:
                print("Connection timed out")
                wifi_connected = False
                return False
            time.sleep(1)
        
        wifi_connected = True
        print('WiFi connected') 
        oled_log("WiFi connected")
        disp_seq_str(["DONE"], 1)
        print('IP Address:', wlan.ifconfig()[0])
        oled_log("IP->")
        oled_log(wlan.ifconfig()[0])
        
        ip_last_byte = wlan.ifconfig()[0].split('.')[3]
        disp_seq_str([str(ip_last_byte)], 1)
        return True
    return False
