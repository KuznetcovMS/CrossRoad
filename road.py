from data import *


class Road:
    def __init__(self, tkcanvas):
        self.canvas = tkcanvas
        # Road
        self.canvas.create_rectangle(10, 400, 890, 500, fill='gray20', outline='gray20')
        self.canvas.create_rectangle(400, 10, 500, 890, fill='gray20', outline='gray20')
        # Markup
        for i in range(14):
            self.canvas.create_rectangle(40 * i + 15 + 20 * i, 440, 100 + 40 * i + 20 * i, 460, fill='white', width=10,
                                         outline='gray20')
            self.canvas.create_rectangle(400, 400, 500, 500, fill='grey20', outline='gray20')

            self.canvas.create_rectangle(440, 40 * i + 15 + 20 * i, 460, 100 + 40 * i + 20 * i, fill='white', width=10,
                                         outline='gray20')
        # Stop lines
        self.nstop = self.canvas.create_rectangle(405, 395, 440, 400, fill='white', tag='stop_line')
        self.estop = self.canvas.create_rectangle(505, 405, 500, 440, fill='white', tag='stop_line')
        self.sstop = self.canvas.create_rectangle(460, 500, 495, 505, fill='white', tag='stop_line')
        self.wstop = self.canvas.create_rectangle(400, 460, 395, 495, fill='white', tag='stop_line')
        # Line index


class TrafficLight:
    def __init__(self, tkcanvas, tkroot, pillar_coord, box_coord, red_coord, yellow_coord, green_coord, index):
        self.canvas = tkcanvas
        self.root = tkroot
        self.index = index
        self.indexl = 0
        # Traffic light frame
        self.pillar = self.canvas.create_rectangle(pillar_coord[0], pillar_coord[1], pillar_coord[2], pillar_coord[3], fill='black')
        self.box = self.canvas.create_rectangle(box_coord[0], box_coord[1], box_coord[2], box_coord[3], fill='black')
        # Traffic light lights
        self.red_light = self.canvas.create_oval(red_coord, fill='red4')
        self.yellow_light = self.canvas.create_oval(yellow_coord, fill='yellow4')
        self.green_light = self.canvas.create_oval(green_coord, fill='green4')
        self.wasgreen = False

    def traffic_light(self):
        if self.index == 1:
            self.canvas.itemconfigure(self.red_light, fill='red4')
            self.canvas.itemconfigure(self.yellow_light, fill='yellow4')
            self.canvas.itemconfigure(self.green_light, fill='green2')
            self.wasgreen = True
            self.indexl = 1
            self.index += 1

        elif self.index == 2:
            self.canvas.itemconfigure(self.red_light, fill='red4')
            self.canvas.itemconfigure(self.yellow_light, fill='yellow')
            self.canvas.itemconfigure(self.green_light, fill='green4')
            self.indexl = 2
            if self.wasgreen:
                self.index += 1
            else:
                self.index -= 1

        elif self.index == 3:
            self.canvas.itemconfigure(self.red_light, fill='red')
            self.canvas.itemconfigure(self.yellow_light, fill='yellow4')
            self.canvas.itemconfigure(self.green_light, fill='green4')
            self.wasgreen = False
            self.index -= 1
            self.indexl = 3


class TrafficController:
    def __init__(self, tkroot, tkcanvas):
        self.root = tkroot
        self.canvas = tkcanvas
        self.W_F_R = []
        self.W_L = []
        self.N_F_R = []
        self.N_L = []
        self.E_F_R = []
        self.E_L = []
        self.S_F_R = []
        self.S_L = []
        self.target_dict = {'W': ['E', 'N', 'S'],
                            'E': ['W', 'N', 'S'],
                            'N': ['S', 'W', 'E'],
                            'S': ['N', 'W', 'E']}
        self.target_list_dict = {'W': [self.W_F_R, self.W_L],
                                 'E': [self.E_F_R, self.E_L],
                                 'N': [self.N_F_R, self.N_L],
                                 'S': [self.S_F_R, self.S_L]}
        self.overlapping()

    def get_spawn_point(self, tag):
        return tag[3]

    def get_rotate_direction(self, tag):
        return tag[-1]

    def get_parallel_list(self, spawn_point):
        return self.target_list_dict.get(self.target_dict.get(spawn_point)[0])

    def get_perpendicular_lists(self, spawn_point):
        return [self.target_list_dict.get(self.target_dict.get(spawn_point)[1]), self.target_list_dict.get(self.target_dict.get(spawn_point)[2])]

    def is_perpendicular_clear(self, perpendicular_lists):
        if len(perpendicular_lists[0][0]) == 0 and len(perpendicular_lists[0][1]) == 0 and len(perpendicular_lists[1][0]) == 0 and len(perpendicular_lists[1][1]) == 0:
            return True
        else:
            return False

    def clear_all_lists(self):
        self.W_F_R.clear()
        self.W_L.clear()
        self.N_F_R.clear()
        self.N_L.clear()
        self.E_F_R.clear()
        self.E_L.clear()
        self.S_F_R.clear()
        self.S_L.clear()

    def overlapping(self):
        self.clear_all_lists()
        overlapping = self.canvas.find_overlapping(405, 405, 495, 495)
        for elem in overlapping:
            if self.canvas.gettags(elem):
                tag = self.canvas.gettags(elem)[0]
                spawn_point = self.get_spawn_point(tag)
                rotate_direction = self.get_rotate_direction(tag)
                if rotate_direction == 'F' or rotate_direction == 'R':
                    self.target_list_dict[spawn_point][0].append(tag)
                elif rotate_direction == 'L':
                    self.target_list_dict[spawn_point][1].append(tag)

    def can_crossing(self, tag):
        spawn_point = self.get_spawn_point(tag)
        rotate_direction = self.get_rotate_direction(tag)
        parallel_list = self.get_parallel_list(spawn_point)
        perpendicular_lists = self.get_perpendicular_lists(spawn_point)
        perpendicular_clear = self.is_perpendicular_clear(perpendicular_lists)
        if rotate_direction == 'L':
            if len(parallel_list[0]) == 0 and len(parallel_list[1]) == 0 and perpendicular_clear:
                return True
            else:
                return False
        elif rotate_direction == 'R' or rotate_direction == 'F':
            if len(parallel_list[1]) == 0 and perpendicular_clear:
                return True
            else:
                return False


class Statistics:
    def __init__(self, tkroot, tkcanvas):
        self.root = tkroot
        self.canvas = tkcanvas
        self.space_dimensions = '73м * 73м'
        self.horizontal_avg_speed = 0
        self.vertical_avg_speed = 0
        self.num_car_in_system = 0
        self.horizontal_avg_time = 0
        self.vertical_avg_time = 0
        self.text = f'Размер участка: {self.space_dimensions}\n' \
                    f'Колличество машин в системе: {self.num_car_in_system}\n' \
                    f'Ср. скорость на гор. участке: {self.horizontal_avg_speed} км/ч\n' \
                    f'Ср. скорость на верт. участке: {self.vertical_avg_speed} км/ч\n' \
                    f'Cр. вр. нахождения в системе на гор. направ: {self.horizontal_avg_time}с\n' \
                    f'Cр. вр. нахождения в системе на верт. направ: {self.vertical_avg_time}с\n'
        self.text_label = self.canvas.create_text(515, 100, text=self.text, font=6, anchor='w', justify='left')
        self.update_stat()

    def update_stat(self):
        self.vertical_avg_time = self.get_avg_time(v_time)
        self.horizontal_avg_time = self.get_avg_time(h_time)
        self.num_car_in_system = get_num_car()
        self.set_speed()
        self.text = f'Размер участка: {self.space_dimensions}\n' \
                    f'Колличество машин в системе: {self.num_car_in_system}\n' \
                    f'Ср. скорость на гор. участке: {self.horizontal_avg_speed} км/ч\n' \
                    f'Ср. скорость на верт. участке: {self.vertical_avg_speed} км/ч\n' \
                    f'Cр. вр. нахождения в системе на гор. направ: {self.horizontal_avg_time}с\n' \
                    f'Cр. вр. нахождения в системе на верт. направ: {self.vertical_avg_time}с\n'
        self.canvas.itemconfigure(self.text_label, text=self.text)
        self.root.after(1000, self.update_stat)

    def get_avg_time(self, time_list):
        if len(time_list) > 0:
            return round(sum(time_list) / len(time_list), 1)
        else:
            return 0

    def set_speed(self):
        if self.horizontal_avg_time != 0:
            self.horizontal_avg_speed = round(73 / self.horizontal_avg_time * 3.6, 1)
        if self.vertical_avg_time != 0:
            self.vertical_avg_speed = round(73 / self.vertical_avg_time * 3.6, 1)
