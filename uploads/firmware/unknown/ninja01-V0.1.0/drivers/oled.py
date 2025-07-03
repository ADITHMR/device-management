import ssd1306

import machine
# Initialize I2C bus (SCL, SDA pins)
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))

try:
    # Create an OLED object connected to the I2C bus
    global oled
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    isOled=1
except:
    isOled=0

# Clear the display (optional)

logData=[""]
# Display text
def oled_log(data):
    if isOled==1:
        for i in range(0, len(data), 16):
            # Append each chunk (substring) to the list
            if len(logData )>5:
                logData.pop(0)
            logData.append(data[i:i+16])
            
        
        
        line=0
        oled.fill(0)
        oled.show()
        for data in  logData:
            oled.text(data,0,line)
            line+=10
        oled.show()
        


def oled_two_data(s1,s2,head,value):
    if isOled==1:
        oled.fill(0)
        
        total_height_px=(s1*8)+(s2*8)+3
        gap=(64-total_height_px)//3
        
        text_width = (len(head)+2) * 6*s1
        x1 = (128 - text_width) // 2
        y1=(64-total_height_px)//2
        oled.write_text(head,x1,y1,s1)
        
        text_width = (len(value)+2) * 6*s2
        x2 = (128 - text_width) // 2
        y2=y1+(s1*8)+3
        oled.write_text(value,x2,y2,s2)
        
        oled.show()

def oled_three_data(s1,s2,s3,head,value1,value2):
    if isOled==1:
        oled.fill(0)
        
        total_height_px=(s1*8)+(s2*8)+(s3*8)+3
        gap=(64-total_height_px)//3
        
        text_width = (len(head) +2)* 6*s1
        x1 = (128 - text_width) // 2
        y1=(64-total_height_px)//2
        oled.write_text(head,x1,y1,s1)
        
        text_width = (len(value1)+2) * 6*s2
        x2 = (128 - text_width) // 2
        y2=y1+(s1*8)+3
        oled.write_text(value1,x2,y2,s2)
        
        text_width = (len(value2)+2) * 6*s2
        x3= (128 - text_width) // 2
        y3=y2+(s2*8)+3
        oled.write_text(value2,x3,y3+1,s3)
    #     print(f"total={total_height_px},y1={y1},y2={y2},y3={y3}")
        oled.show()
    
