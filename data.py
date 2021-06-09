tr_lt_n = [[374, 350, 366, 390], [350, 230, 390, 350], [350, 230, 390, 270], [350, 270, 390, 310], [350, 310, 390, 350]]
tr_lt_e = [[510, 526, 640, 534], [550, 510, 670, 550], [630, 510, 670, 550], [590, 510, 630, 550], [550, 510, 590, 550]]

w_spawn = [12, 462, 80, 462, 80, 492, 12, 492]
n_spawn = [435, 12, 435, 80, 405, 80, 405, 12]
e_spawn = [888, 436, 820, 436, 820, 406, 888, 406]
s_spawn = [460, 888, 460, 820, 490, 820, 490, 888]

colors = ['gold', 'purple', 'orange', 'red3', 'blue', 'orange', 'black']

rotate_weights_h = [0.2, 0.6, 0.2]
rotate_weights_v = [0.4, 0.2, 0.4]

h_time = []
v_time = []

h_num_car = 0
v_num_car = 0
num_car_all = 0


def add_num_list(tp):
    global h_num_car, v_num_car
    if tp == 'H':
        h_num_car += 1
    elif tp == 'V':
        v_num_car += 1


def sub_num_list(tp):
    global h_num_car, v_num_car
    if tp == 'H':
        h_num_car -= 1
    elif tp == 'V':
        v_num_car -= 1


def get_num_car():
    global h_num_car, v_num_car
    return h_num_car + v_num_car


def add_num_all():
    global  num_car_all
    num_car_all += 1