from tkinter import *
from road import *
from vehicles import *
from data import *
from random import randint


w = 0
n = 0
e = 0
s = 0
tr_index = 1
tr_indexl = 0
bgreen = False


def traffic_light_change():
    global tr_index, tr_indexl, bgreen, traffic_lights_list
    if tr_index == 1:
        tr_indexl = 1
        tr_index += 1
        bgreen = True
        for elem in traffic_lights_list:
            elem.traffic_light()
        root.after(12000, traffic_light_change)
    elif tr_index == 2:
        tr_indexl = 2
        if bgreen:
            tr_index += 1
            for elem in traffic_lights_list:
                elem.traffic_light()
            root.after(2000, traffic_light_change)
        else:
            tr_index -= 1
            for elem in traffic_lights_list:
                elem.traffic_light()
            root.after(2000, traffic_light_change)
    elif tr_index == 3:
        for elem in traffic_lights_list:
            elem.traffic_light()
        bgreen = False
        tr_indexl = 3
        tr_index -= 1
        root.after(12000, traffic_light_change)


def spawn_w():
    global w
    coll = [elem for elem in canvas.find_overlapping(12, 462, 82, 492) if canvas.gettags(elem)]
    if len(coll) == 0:
        w += 1
        Vehicle(canvas, root, traffic_light_e, 'carW' + str(w), [1, 0], 'W', traffic_controller_w)
    root.after(randint(5000, 7000), spawn_w)


def spawn_n():
    global n
    coll = [elem for elem in canvas.find_overlapping(405, 12, 440, 80) if canvas.gettags(elem)]
    if len(coll) == 0:
        n += 1
        Vehicle(canvas, root, traffic_light_n, 'carN' + str(n), [0, 1], 'N', traffic_controller_n)
    root.after(randint(5000, 7000), spawn_n)


def spawn_e():
    global e
    coll = [elem for elem in canvas.find_overlapping(820, 405, 888, 440) if canvas.gettags(elem)]
    if len(coll) == 0:
        e += 1
        Vehicle(canvas, root, traffic_light_e, 'carE' + str(e), [-1, 0], 'E', traffic_controller_e)
    root.after(randint(5000, 7000), spawn_e)


def spawn_s():
    global s
    coll = [elem for elem in canvas.find_overlapping(460, 820, 495, 888) if canvas.gettags(elem)]
    if len(coll) == 0:
        s += 1
        Vehicle(canvas, root, traffic_light_n, 'carS' + str(s), [0, -1], 'S', traffic_controller_s)
    root.after(randint(5000, 7000), spawn_s)


root = Tk()
root.title('Crossroads')

canvas = Canvas(root, width=900, height=900)
canvas.grid(row=0, column=0)

road = Road(canvas)
traffic_light_n = TrafficLight(canvas, root, tr_lt_n[0], tr_lt_n[1], tr_lt_n[2], tr_lt_n[3], tr_lt_n[4], 3)
traffic_light_e = TrafficLight(canvas, root, tr_lt_e[0], tr_lt_e[1], tr_lt_e[2], tr_lt_e[3], tr_lt_e[4], 1)
traffic_lights_list = [traffic_light_n, traffic_light_e]
traffic_controller_w = TrafficController(root, canvas)
traffic_controller_n = TrafficController(root, canvas)
traffic_controller_e = TrafficController(root, canvas)
traffic_controller_s = TrafficController(root, canvas)
spawn_w()
spawn_n()
spawn_e()
spawn_s()
traffic_light_change()
stat = Statistics(root, canvas)

root.mainloop()
