from sense_hat import SenseHat
from time import sleep
from socket import *
from datetime import datetime

BROADCAST_TO_PORT = 7000

s = SenseHat()

s.low_light = True

s.clear()

g = (0, 255, 0)  # Green
e = (0, 0, 0)  # Empty
b = (0, 0, 255)  # Blue
r = (255, 0, 0)  # Red
w = (255, 255, 255)  # White

arrow_down = [
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    b, e, e, b, b, e, e, b,
    e, b, e, b, b, e, b, e,
    e, e, b, b, b, b, e, e,
    e, e, e, b, b, e, e, e,
    b, b, b, b, b, b, b, b
]

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

stop = [
    e, e, r, r, r, r, e, e,
    e, r, r, r, r, r, r, e,
    r, r, r, r, r, r, r, r,
    r, w, w, w, w, w, w, r,
    r, w, w, w, w, w, w, r,
    r, r, r, r, r, r, r, r,
    e, r, r, r, r, r, r, e,
    e, e, r, r, r, r, e, e
]


def download_animation():
    s.set_pixels(arrow_down)
    sleep(1)
    s.clear()
    sleep(1)

def upload_animation():
    s.set_pixels(arrow_up)
    sleep(1)
    s.clear()
    sleep(1)

def upload_animation2():
  for i in range(7, -1, -1):
    s.set_pixels(arrow_up)
    sleep(.2)
    for j in range(8):
      s.set_pixel(j, i, e)
    sleep(.2)


def UDP_Sender():
    raspberry_id = "TestData22"
    temperature = str(round(s.get_temperature(), 2))
    humidity = str(round(s.get_humidity(), 2))
    time = str(datetime.now())

    data = "{\"raspberryId\":\"" + raspberry_id + "\",\"temperature\":\"" + temperature + "\",\"humidity\":\"" + humidity + "\",\"timeStamp\":\"" + time + "\"}"
    mySocket.sendto(bytes(data.encode("UTF-8")), ('<broadcast>', BROADCAST_TO_PORT))
    sleep(1)

mySocket = socket(AF_INET, SOCK_DGRAM)
mySocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

while True:
    upload_animation2()
    UDP_Sender()
