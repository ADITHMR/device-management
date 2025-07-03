
import network
import json
import esp32

def write_serial_no(number_str,prefix="PB"):
    a=prefix
    c=number_str

    sta_if = network.WLAN(network.STA_IF)
    mac_address = sta_if.config('mac')
    last_24bits = mac_address[3:] 
    last_24bits_str = ''.join('%02x' % b for b in last_24bits)
    b=  last_24bits_str
    serialnumber=a+b+c

    
    # print(f"b'{serialnumber}'")
    s_no = esp32.NVS('serial_number')
    s_no.set_blob('s_num', serialnumber)
    s_no.set_i32('s_num_len', len(serialnumber))
    s_no.commit()
    print(f"Done!   {serialnumber}")
def get_serial_no():
    try:
        s_no = esp32.NVS('serial_number')
        retrieved = bytearray(s_no.get_i32('s_num_len'))
        data=s_no.get_blob('s_num', retrieved)
        print(retrieved.decode())
        return (retrieved.decode())
        
    except Exception as e:
        print("Error: on get_serial_no()", e)
        return("Serial Number ERROR")
       

def get_version():
    with open('version.dat', 'r') as f:
        data = json.load(f)
            
        version=f"{data['version']}"
        return (version)

def get_update_flag():
    try:
        with open('schema.dat', 'r') as f:
            data = json.load(f)
        if data["update_flag"]=="enabled":
            return True
        elif data["update_flag"]=="disabled":
            return False
        else:
            return "Error"
    except Exception as e:
        print("Error: on get_update_flag()", e)
        return("ERROR")
        
  