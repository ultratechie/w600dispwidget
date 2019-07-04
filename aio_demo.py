# W600 plus SSD1306 OLED display widget demo
# Fetch feed from Adafruit IO (AIO) and display on display

from easyw600 import *
import ssd1306
import machine
import urequests as requests
import json
import time

# WiFi credentials 
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# Adafruit AIO credentials
AIO_KEY = "your_aoi_key"
# replace with your AIO feed URL
AIO_FEED_URL = "http://io.adafruit.com/api/v2/ultratechie/groups/homemonitor?X-AIO-Key=" + AIO_KEY 
TIME_URL = "http://worldtimeapi.org/api/timezone/Europe/London"

# how often is the feed updated on the LCD display
FEED_UPDATE_DELAY_SECS = 10

# SPI pin settings
spi_dc   = machine.Pin(24, machine.Pin.OUT, machine.Pin.PULL_FLOATING)
spi_cs   = machine.Pin(25, machine.Pin.OUT, machine.Pin.PULL_FLOATING)
spi_sck  = machine.Pin(26)
spi_miso = machine.Pin(27)
spi_mosi = machine.Pin(28)

# Initialize SPI
spi = machine.SPI(sck=spi_sck, mosi=spi_mosi, miso=spi_miso)
spi.init()

ssd = ssd1306.SSD1306_SPI(128,32,spi,spi_dc,None,spi_cs)

ssd.fill(0) # clear the display buffer
ssd.text('Connecting to', 0, 0, 0xffff)
ssd.text('WiFi..', 0, 10, 0xffff)
ssd.show()

# connect to Wifi
sta_if =connect(WIFI_SSID,WIFI_PASSWORD)
#ftpserver()

ssd.fill(0) 
ssd.text('Connected.', 0, 0, 0xffff)
ssd.text('Fetching data..', 0, 10, 0xffff)
ssd.show()


while(1):

    # fetch date time
    r = requests.get(TIME_URL)
    resp = r.text
    r.close()

    # parse the returned JSON 
    jo = json.loads(resp)
    local_date = jo["datetime"].split("T")[0]
    local_time = jo["datetime"].split("T")[1].split(".")[0]

    # fetch the AIO feed
    r = requests.get(AIO_FEED_URL)
    resp = r.text
    r.close()

    # parse the AIO JSON feed
    jo = json.loads(resp)
    humid = jo["feeds"][0]["last_value"]
    temp = jo["feeds"][1]["last_value"]

    
    ssd.fill(0) # clear the display buffer
    ssd.text("Time: %s"%(local_time), 0, 0, 0xffff)
    ssd.text('Temp: %s degC'%(temp), 0, 10, 0xffff)
    ssd.text('Humidity: %s%%'%(humid), 0, 20, 0xffff)
    ssd.show()
    
    time.sleep(FEED_UPDATE_DELAY_SECS)
    
    