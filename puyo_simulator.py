import puyo_class

import numpy as np
import collections

"""
Subclase que hereda de puyo_class.py
Utilizado como simulador

ーーーInstrucciones de control de Puyo Puyoーーー

Movimiento: Mover a la izquierda 1
            Mover a la derecha 2
            Mover hacia abajo 3

Rotación: Rotación en el sentido de las agujas del reloj 1
          Rotación en sentido contrario a las agujas del reloj 2
          
El tamaño del tablero es por defecto de 6 * 13.
# La vista visible es de WIDTH * (HEIGHT - 1)
"""

WIDTH = puyo_class.WIDTH
HEIGHT = puyo_class.HEIGHT


class Player(puyo_class.PuyoSuper):
    # Manejo del flujo usando un contador (step)
    def flow_management(self):
        # print('puyo now', self.color_axis, self.color_rotate)
        # print('next', self.color_axis_next, self.color_rotate_next)
        # print('nexnex', self.color_axis_nexnex, self.color_rotate_nexnex)
        self.chigiri(self.can_chigiri())
        self.set_puyo()
        self.delete_14th_column()
        self.chain_number = 0
        self.score_turn = 0
        while self.can_fire():
            self.chain_number += 1
            score_current = self.score_calculation(self.chain_number, self.link_bonus_sum,
                                                   len(collections.Counter(self.color_list)), self.deleted_puyo_number)
            self.score += score_current
            self.score_turn += score_current
            self.fall()
            self.link_bonus_sum = 0
        if self.is_gameover():
            self.gameover = True
        elif self.is_all_clear():
            self.all_clear_flag = True
        self.tsumo()
        self.set_end = False

    # Colocar la puyo movida
    def set_puyo(self):
        self.field[self.x_axis][self.y_axis] = self.color_axis
        self.field[self.x_rotate][self.y_rotate] = self.color_rotate

    # Establecer fire_flag para aquellos con más de 4 conexiones
    # La parte de self.color_delete ha sido sobrescrita
    def flag_over4links(self, i, j):
        self.link_is_counted[i][j] = 0
        self.field[i][j] = 0
        self.deleted_puyo_number += 1
        if self.link_is_counted[i + 1][j] > 0 and self.color_delete == self.field[i + 1][j]:
            self.flag_over4links(i + 1, j)
        if self.link_is_counted[i][j + 1] > 0 and self.color_delete == self.field[i][j + 1]:
            self.flag_over4links(i, j + 1)
        if self.link_is_counted[i - 1][j] > 0 and self.color_delete == self.field[i - 1][j]:
            self.flag_over4links(i - 1, j)
        if self.link_is_counted[i][j - 1] > 0 and self.color_delete == self.field[i][j - 1]:
            self.flag_over4links(i, j - 1)

    # Detectar la ignición: calcular la cantidad de conexiones a partir de Puyos con 0 conexiones.
    def can_fire(self):
        judge = False
        self.deleted_puyo_number = 0
        self.color_list = []
        for i in range(1, WIDTH + 1):
            for j in range(1, HEIGHT + 1):  # range(2, HEIGHT + 1)かも
                if self.field[i][j] != 0:
                    self.link_counter = 0
                    self.link_is_counted = np.zeros((WIDTH + 2) * (HEIGHT + 2), dtype=int)\
                        .reshape(WIDTH + 2, HEIGHT + 2).tolist()
                    self.color_delete = self.field[i][j]
                    self.link_calculation(i, j)
                    if self.link_counter >= 4:
                        self.flag_over4links(i, j)
                        self.link_bonus_sum += self.link_bonus(self.link_counter)
                        self.color_list.append(self.color_delete)
                        judge = True
        return judge

    # Caída causada por la ignición
    def fall(self):
        flag = True
        while flag:
            flag = False
            for i in range(1, WIDTH + 1):
                for j in range(1, HEIGHT):
                    if self.field[i][HEIGHT - j + 1] == 0 and self.field[i][HEIGHT - j] != 0:
                        self.field[i][HEIGHT - j + 1] = self.field[i][HEIGHT - j]
                        self.field[i][HEIGHT - j] = 0
                        flag = True

    # Tomar acciones al azar
    def random_action(self):
        random_act = np.random.randint(0, 21)
        self.auto_play(random_act)
        return True

    # Devolver el estado
    def get_state(self):
        field_info = np.array(self.field)[1:WIDTH + 1, 2:HEIGHT + 1]
        puyo_info = np.array(self.color_axis)
        puyo_info = np.append(puyo_info, self.color_rotate)
        puyo_info = np.append(puyo_info, self.color_axis_next)
        puyo_info = np.append(puyo_info, self.color_rotate_next)
        puyo_info = np.append(puyo_info, self.color_axis_nexnex)
        puyo_info = np.append(puyo_info, self.color_rotate_nexnex)
        field_info = np.array(field_info, dtype=np.float32)
        puyo_info = np.array(puyo_info, dtype=np.float32)
        return field_info, puyo_info

    # Proporcionar una de las 22 acciones posibles
    def rl_step(self, num):
        done = False
        self.score_turn = 0
        self.auto_play(num)
        self.flow_management()
        if self.gameover:
            done = True
        return self.get_state(), self.score_turn, done, self.chain_number
        # return self.get_state(), self.chain_number, done, self.chain_number

    # Realizar 22 tipos de acciones
    def auto_play(self, num):
        cnt = 0
        self.set_end = False
        while not self.set_end:
            # Caer directamente
            if num == 0:
                if cnt <= 1:
                    self.move(1)
                else:
                    self.move(3)
            elif num == 1:
                if cnt == 0:
                    self.move(1)
                else:
                    self.move(3)
            elif num == 2:
                self.move(3)
            elif num == 3:
                if cnt == 0:
                    self.move(2)
                else:
                    self.move(3)
            elif num == 4:
                if cnt <= 1:
                    self.move(2)
                else:
                    self.move(3)
            elif num == 5:
                if cnt <= 2:
                    self.move(2)
                else:
                    self.move(3)

            # Caer invertido
            elif num == 6:
                if cnt <= 1:
                    self.rotate(2)
                    self.move(1)
                else:
                    self.move(3)
            elif num == 7:
                if cnt == 0:
                    self.rotate(2)
                    self.move(1)
                elif cnt == 1:
                    self.rotate(2)
                else:
                    self.move(3)
            elif num == 8:
                if cnt <= 1:
                    self.rotate(2)
                else:
                    self.move(3)
            elif num == 9:
                if cnt == 0:
                    self.rotate(1)
                    self.move(2)
                elif cnt == 1:
                    self.rotate(1)
                else:
                    self.move(3)
            elif num == 10:
                if cnt <= 1:
                    self.rotate(1)
                    self.move(2)
                else:
                    self.move(3)
            elif num == 11:
                if cnt <= 1:
                    self.rotate(1)
                    self.move(2)
                elif cnt == 2:
                    self.move(2)
                else:
                    self.move(3)

            # 時計回りで落下
            elif num == 12:
                if cnt == 0:
                    self.move(1)
                    self.rotate(1)
                else:
                    self.move(3)
            elif num == 13:
                if cnt == 0:
                    self.rotate(1)
                else:
                    self.move(3)
            elif num == 14:
                if cnt == 0:
                    self.move(2)
                    self.rotate(1)
                else:
                    self.move(3)
            elif num == 15:
                if cnt == 0:
                    self.move(2)
                    self.rotate(1)
                elif cnt == 1:
                    self.move(2)
                else:
                    self.move(3)
            elif num == 16:
                if cnt == 0:
                    self.move(2)
                    self.rotate(1)
                elif 0 < cnt <= 2:
                    self.move(2)
                else:
                    self.move(3)

            # 反時計回りで落下
            elif num == 17:
                if cnt == 0:
                    self.rotate(2)
                    self.move(1)
                else:
                    self.move(3)
            elif num == 18:
                if cnt == 0:
                    self.rotate(2)
                else:
                    self.move(3)
            elif num == 19:
                if cnt == 0:
                    self.rotate(2)
                    self.move(2)
                else:
                    self.move(3)
            elif num == 20:
                if cnt == 0:
                    self.rotate(2)
                    self.move(2)
                elif cnt == 1:
                    self.move(2)
                else:
                    self.move(3)
            elif num == 21:
                if cnt == 0:
                    self.move(2)
                    self.rotate(2)
                elif 0 < cnt <= 2:
                    self.move(2)
                self.move(3)
            cnt += 1