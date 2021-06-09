from random import uniform, choice, choices
from math import sin, cos, radians
from data import *


class Vehicle:
    def __init__(self, tkcanvas, tkroot, traffic_light, tag, forward_vector, target_spawn, traffic_controller):
        self.root = tkroot
        self.canvas = tkcanvas
        self.spawn = target_spawn
        self.sc = self.get_spawn_coord()
        self.traffic_controller = traffic_controller
        self.traffic_light = traffic_light
        self.target_dict = {'N': [0, -1],
                            'E': [1, 0],
                            'S': [0, 1],
                            'W': [-1, 0]}
        self.forward_vector = forward_vector
        self.direction = []
        self.target_direction = []
        self.key = ''
        self.tick_id = ''
        self.rotate_iteration = 0
        self.angle = 0
        self.start_rotate = False
        self.v0 = self.forward_vector.index(0)
        self.v1 = 1 - self.forward_vector.index(0)
        self.type = self.set_type()
        self.car_type = self.set_car_type()
        self.speed = self.set_speed()
        self.angle_mult = self.set_angle_mult()
        self.set_direction()
        self.set_target_direction()
        self.d0 = self.target_direction.index(0)
        self.d1 = 1 - self.target_direction.index(0)
        self.get_angle()
        self.alpha = self.get_alpha()
        self.tag = tag + self.rotate_determination()
        self.color = choice(colors)
        self.car = self.canvas.create_polygon(self.sc[0], self.sc[1], self.sc[2], self.sc[3], self.sc[4], self.sc[5],
                                              self.sc[6], self.sc[7], fill=self.color, tag=self.tag, outline='black')
        self.can_rotate = False
        self.set_scale()
        self.time = -1
        self.timer()
        add_num_list(self.type)
        add_num_all()
        self.deleted = False
        self.ai()

    def ai(self):
        collision_list = self.get_collision_list()
        can_move = True
        stop_line = False
        self.can_rotate = False

        for elem in collision_list:
            if 'car' in elem:
                can_move = False
        if 'stop_line' in collision_list:
            stop_line = True
        self.move(stop_line, can_move)
        if self.start_rotate and can_move and self.rotate_determination() != 'F' and self.rotate_iteration < self.get_rotate_iteration_count() and self.can_rotate:
            self.rotate_iteration += 1
            if self.get_rotate_iteration_count() - 1 < self.rotate_iteration < self.get_rotate_iteration_count():
                blast = True
            else:
                blast = False
            self.rotate(self.angle, blast)
        self.tick_id = self.root.after(16, self.ai)
        self.actor_destroy()

    def move(self, stop_line, can_move):

        if not stop_line and can_move:
            self.canvas.move(self.car, self.direction[0], self.direction[1])
            self.can_rotate = True

        elif stop_line and self.traffic_light.indexl == 1 and can_move:
            self.traffic_controller.overlapping()
            if self.traffic_controller.can_crossing(self.tag):
                self.canvas.move(self.car, self.direction[0], self.direction[1])
                self.start_rotate = True
                self.can_rotate = True

    def rotate_determination(self):
        d = {'N': ['E', 'W', 'S'],
             'E': ['S', 'N', 'W'],
             'S': ['W', 'E', 'N'],
             'W': ['N', 'S', 'E']}
        if self.key == d.get(self.spawn)[2]:
            return 'F'
        elif self.key == d.get(self.spawn)[0]:
            return 'L'
        elif self.key == d.get(self.spawn)[1]:
            return 'R'

    def rotate(self, angle, blast):
        x = self.canvas.coords(self.car)[::2]
        y = self.canvas.coords(self.car)[1::2]
        local_x = [x[i] - self.get_center(0) for i in range(4)]
        local_y = [y[i] - self.get_center(1) for i in range(4)]
        local_x = [local_x[i] * cos(radians(angle)) + local_y[i] * sin(radians(angle)) for i in range(4)]
        local_y = [local_y[i] * cos(radians(angle)) - local_x[i] * sin(radians(angle)) for i in range(4)]
        x = [local_x[i] + self.get_center(0) for i in range(4)]
        y = [local_y[i] + self.get_center(1) for i in range(4)]
        self.canvas.coords(self.car, x[0], y[0], x[1], y[1], x[2], y[2], x[3], y[3])
        self.canvas.scale(self.car, self.get_center(0), self.get_center(1), 1, 1.0001)
        self.rotate_forward_vector(blast)
        self.set_direction()

    def get_alpha(self):
        if self.rotate_determination() != 'F':
            return 1 / self.get_rotate_iteration_count()
        else:
            return 0

    def rotate_forward_vector(self, blast):
        if blast:
            self.forward_vector[self.v0] = round(self.forward_vector[self.v0])
            self.forward_vector[self.v1] = round(self.forward_vector[self.v1])
        else:
            self.forward_vector[self.v0] += self.target_direction[self.d1] * self.alpha
            self.forward_vector[self.v1] -= self.forward_vector[self.v1] * self.alpha

    def get_center(self, i):
        x = self.canvas.coords(self.car)[::2]
        y = self.canvas.coords(self.car)[1::2]
        center = [sum(x) / 4, sum(y) / 4]
        return center[i]

    def set_direction(self):
        self.direction = [self.forward_vector[0] * self.speed, self.forward_vector[1] * self.speed]

    def set_target_direction(self):
        self.target_dict.pop(self.spawn)
        d = {'N': ['E', 'W', 'S'],
             'E': ['S', 'N', 'W'],
             'S': ['W', 'E', 'N'],
             'W': ['N', 'S', 'E']}
        if self.type == 'H':
            direction = choices(['L', 'F', 'R'], rotate_weights_h, k=1)
        elif self.type == 'V':
            direction = choices(['L', 'F', 'R'], rotate_weights_v, k=1)
        if direction[0] == 'L':
            self.key = d.get(self.spawn)[0]
        elif direction[0] == 'R':
            self.key = d.get(self.spawn)[1]
        elif direction[0] == 'F':
            self.key = d.get(self.spawn)[2]
        self.target_direction = self.target_dict.get(self.key)

    def get_collision_list(self):
        output = []
        coord = self.canvas.coords(self.car)
        overlapping = ()
        if self.spawn == 'W':
            overlapping = self.canvas.find_overlapping(coord[2] - 2, coord[3], coord[4] + 5, coord[5])
        elif self.spawn == 'N':
            overlapping = self.canvas.find_overlapping(coord[2], coord[3] - 2, coord[4], coord[5] + 5)
        elif self.spawn == 'E':
            overlapping = self.canvas.find_overlapping(coord[2] + 2, coord[3], coord[4] - 5, coord[5])
        elif self.spawn == 'S':
            overlapping = self.canvas.find_overlapping(coord[2], coord[3] + 2, coord[4], coord[5] - 5)
        for elem in overlapping:
            ob = self.canvas.gettags(elem)
            if ob and ob[0] != self.tag and ob[0] != 'current':
                output.append(ob[0])
        return output

    def actor_destroy(self):
        coord = self.canvas.coords(self.car)
        for elem in coord:
            if elem > 900 or elem < 0:
                self.canvas.delete(self.car)
                self.root.after_cancel(self.tick_id)
                if not self.deleted:
                    sub_num_list(self.type)
                    if self.type == 'H':
                        h_time.append(self.time)
                    elif self.type == 'V':
                        v_time.append(self.time)
                    self.deleted = True

    def get_angle(self):
        determination = self.rotate_determination()
        if determination == 'L':
            self.angle = 0.47 * self.speed * self.angle_mult
        elif determination == 'R':
            self.angle = -0.85 * self.speed * self.angle_mult

    def get_rotate_iteration_count(self):
        return 90 / abs(self.angle)

    def get_spawn_coord(self):
        if self.spawn == 'W':
            return w_spawn
        elif self.spawn == 'N':
            return n_spawn
        elif self.spawn == 'E':
            return e_spawn
        elif self.spawn == 'S':
            return s_spawn

    def set_type(self):
        if self.spawn == 'W' or self.spawn == 'E':
            return 'H'
        elif self.spawn == 'N' or self.spawn == 'S':
            return 'V'

    def set_car_type(self):
        return choice(['standard', 'cargo'])

    def set_speed(self):
        if self.car_type == 'standard':
            return uniform(1, 1.5)
        else:
            return uniform(0.75, 1)

    def set_scale(self):
        if self.type == 'H' and self.car_type == 'standard':
            self.canvas.scale(self.car, self.get_center(0), self.get_center(1), 0.75, 1)
        elif self.type == 'V' and self.car_type == 'standard':
            self.canvas.scale(self.car, self.get_center(0), self.get_center(1), 1, 0.75)

    def set_angle_mult(self):
        if self.car_type == 'standard':
            return 1.15
        elif self.car_type == 'cargo':
            return 1

    def timer(self):
        self.time += 1
        self.root.after(1000, self.timer)








