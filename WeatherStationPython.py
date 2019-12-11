from sense_hat import SenseHat
from time import sleep
from socket import *
from datetime import datetime
from multiprocessing import Process

BROADCAST_TO_PORT = 7000

s = SenseHat()
s.low_light = True
s.clear()

e = (0, 0, 0)  # Empty
r = (255, 0, 0)  # Red
b = (80, 186, 255) # Blue

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

connection1 = [
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    b, b, e, e, e, e, e, e,
    b, b, e, e, e, e, e, e
]

connection2 = [
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, b, b, e, e, e,
    e, e, e, b, b, e, e, e,
    b, b, e, b, b, e, e, e,
    b, b, e, b, b, e, e, e
]

connection3 = [
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, e, e,
    e, e, e, e, e, e, b, b,
    e, e, e, e, e, e, b, b,
    e, e, e, b, b, e, b, b,
    e, e, e, b, b, e, b, b,
    b, b, e, b, b, e, b, b,
    b, b, e, b, b, e, b, b
]

def connect_animation():
    s.set_pixels(connection1)
    sleep(.5)
    s.set_pixels(connection2)
    sleep(.5)
    s.set_pixels(connection3)
    sleep(.5)

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

def joystick():
    while True:
        for event in s.stick.get_events():
            if event.action == "pressed":
                if event.direction == "middle":
                    UDP_Sender()

def updateEvery15Minute():
    while True:
        try:
            UDP_Sender()
            # 900x60 = 15 minutes sleep
            sleep(900)
        except error as err:
            print (err)
            connect_animation()


process1 = Process(target=joystick)
process2 = Process(target=updateEvery15Minute)
process1.start()
process2.start()
