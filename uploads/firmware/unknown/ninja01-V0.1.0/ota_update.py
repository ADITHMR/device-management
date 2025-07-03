import network
import urequests
import ujson
import json
import time
import os
import machine
import gc
from local_host.connect_wifi import connect_wifi
try:
    from drivers.oled import *
except Exception as e:
        print("Error:", e)
led = machine.Pin(2, machine.Pin.OUT)
progress=0

    
# Wi-Fi Connection Function
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        # Timeout after 30 seconds
        timeout = 30
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if timeout == 0:
            print("Failed to connect to Wi-Fi.")
            return False
    print('Connected to WiFi', wlan.ifconfig())
    return True

# Function to fetch the list of files from GitHub
def get_github_file_list(owner, repo, path):
    url = "https://raw.githubusercontent.com/ADITHMR/probots_micropython/refs/heads/device_branch/files_list.txt"
    print(f"Fetching file list from: {url}")

    try:
        # Make the request to GitHub API without the Authorization header for public repo
        response = urequests.get(url)
        if response.status_code  == 200:
            # Parse the JSON response
            file_list = ujson.loads(response.text)
            print(file_list)
            # Print the file list (name, path, etc.)
#             for file in file_list:
#                 print(f"Name: {file['name']}, Path: {file['path']}, Type: {file['type']}")
            return file_list
        else:
            print(f"Failed to fetch file list: {response.status_code }")
            return []
    except Exception as e:
        print(f"Error fetching file list: {e}")
        return []

# Function to download files from GitHub and store them on ESP32
def download_file(url, folder, filename):
    try:
        # Check if the folder exists, if not, create it
        try:
            os.listdir(folder)
            
            
        except OSError:
            os.mkdir(folder)
            print(f"Created folder: {folder}")

        # Construct the full file path
        file_path = f"{folder}/{filename}"

        # Download the file and save it to the specified folder
        response = urequests.get(url)
        if response.status_code  == 200:
            with open(file_path, 'w') as f:  # Use 'wb' for binary files
                f.write(response.text)  # Assuming text files for now
            print(f"Downloaded and saved to: {file_path}")
        else:
            print(f"Failed to download {filename}: {response.status_code }")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
    finally:
        response.close()

# Main function to perform OTA update
def ota_update():

    # Replace with your Wi-Fi credentials
    global progress
    progress=0
    

    # Replace with your GitHub username, repository name, and directory path (use empty string for root directory)
    owner = "ADITHMR"  # Replace with the GitHub username
    repo = "probots_micropython"  # Replace with the repository name
    path = ""  # Empty string means the root directory of the repo

    # Fetch the list of files to update from GitHub
    file_folders  = get_github_file_list(owner, repo, path)
    file_count = 0

# Loop through each folder entry in the data
    for folder in file_folders:
        # Add the number of files in the current folder
        file_count += len(folder["files"])

    if not file_folders:
        print("No files to update.")
        return
    finished_files=0
    for folder_data in file_folders:
        folder = folder_data["folder"]
        files = folder_data["files"]

            # For each folder, get the list of files from GitHub and download them
        for filename in files:
            gc.collect()
            print(f"Downloading {filename} from {folder}...")
            url = f"https://raw.githubusercontent.com/ADITHMR/probots_micropython/refs/heads/device_branch/"
            if folder== "/" :
                url+=filename
            else:
                url+=folder.strip('/')+"/"+filename
            print(url)
            
            
            led.value(not led.value())
            # Download each file and save it in the corresponding folder
            download_file(url, folder.strip('/'), filename)# Run the OTA update process
            finished_files+=1
            
            progress=int((finished_files / file_count) * 100)
            try:
                from drivers.oled import oled_log
                oled_two_data(1,3,"Updating",f"{progress}%")
            except Exception as e:
                print("OLED Error:", e)
            print(f"progress={progress}")
            if progress >=100:
                with open('schema.dat', 'r') as f:
                    data = json.load(f)
                data["update_flag"]="False"
                with open('schema.dat', 'w') as f:
                    json.dump(data, f)
                try:
                    from drivers.oled import oled_log
                    oled_two_data(1,3,"Update",f"Complete.")
                    print("Update complete")
                    time.sleep(1)
                except Exception as e:
                    print("OLED Error:", e)
def run_update():
    try:
        if not connect_wifi():
            try:
                from drivers.oled import oled_log
                oled_two_data(1,3,"WIFI Conn",f"Failed") 
                
            except Exception as e:
                print("OLED Error:", e)
            time.sleep(2)
            return()
            
    except:
        
        if not connect_wifi(ssid="Probot",password="Probot@1234"):
            try:
                from drivers.oled import oled_log
                oled_two_data(1,3,"WIFI Conn",f"Failed")
                
            except Exception as e:
                print("OLED Error:", e)
            time.sleep(2)
            return()
    try:
        ota_update()
    except Exception as e:
        print("Error on ota_update()", e)
        with open('schema.dat', 'r') as f:
            data = json.load(f)
        data["update_flag"]="False"
        with open('schema.dat', 'w') as f:
            json.dump(data, f)
        from drivers.oled import oled_log
        oled_two_data(1,3,"Update",f"Failed.")
        print("Update Failed")

