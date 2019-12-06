from sense_hat import SenseHat
from time import sleep
from socket import *
from datetime import datetime

BROADCAST_TO_PORT = 7000

s = SenseHat()
s.low_light = True
s.clear()

e = (0, 0, 0)  # Empty
r = (255, 0, 0)  # Red

arrow_up = [
    r, r, r, r, r, r, r, r,
    e, e, e, r, r, e, e, e,
    e, e, r, r, r, r, e, e,
    e, r, r, r, r, r, r, e,
    r, r, e, r, r, e, r, r,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e
]

cross = [
    r, e, e, e, e, e, e, r,
    e, r, e, e, e, e, r, e,
    e, e, r, e, e, r, e, e,
    e, e, e, r, r, e, e, e,
    e, e, e, r, r, e, e, e,
    e, e, r, e, e, r, e, e,
    e, r, e, e, e, e, r, e,
    r, e, e, e, e, e, e, r
]

def error_animation():
    for i in range(4):
        s.set_pixels(cross)
        sleep(.1)
        s.clear()
        sleep(.1)

def upload_animation():
    for i in range(7, -1, -1):
        s.set_pixels(arrow_up)
        sleep(.1)
        for j in range(8):
            s.set_pixel(j, i, e)
        sleep(.1)
    s.clear()


def UDP_Sender():
    raspberry_id = "TestData22"
    temperature = str(round(s.get_temperature(), 1))
    humidity = str(round(s.get_humidity(), 1))
    time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    data = "{\"raspberryId\":\"" + raspberry_id + "\",\"temperature\":\"" + temperature + "\",\"humidity\":\"" + humidity + "\",\"timeStamp\":\"" + time + "\"}"
    mySocket.sendto(bytes(data.encode("UTF-8")), ('<broadcast>', BROADCAST_TO_PORT))
    upload_animation()

mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while True:
    try:
        UDP_Sender()
        #15 minutes sleep
        sleep(900)
    except error as err:
        print (err)
        error_animation()
