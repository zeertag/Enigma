import socket

import Rotors
import UKW


class Machine:
    def __init__(self):
        self.ETW = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 10,
            11: 11,
            12: 12,
            13: 13,
            14: 14,
            15: 15,
            16: 16,
            17: 17,
            18: 18,
            19: 19,
            20: 20,
            21: 21,
            22: 22,
            23: 23,
            24: 24,
            25: 25,
            26: 26
        }  # входной диск
        self.UKW = None  # рефлектор
        self.rotors = {
            1: Rotors.RotorI(),
            2: Rotors.RotorII(),
            3: Rotors.RotorIII(),
            4: Rotors.RotorIV(),
            5: Rotors.RotorV(),
        }  # роторы

        self.choice_rotors = None
        self.rotor_pos = None
        self.commutations = {}

    def check_rotors(self):
        for i in self.choice_rotors:
            if i < 1 or i > 5 or (len(self.choice_rotors) != len(set(self.choice_rotors))):
                print("Некорректный ввод параметров")
                return 1
        return 0

    def check_poses(self):
        for i in self.rotor_pos:
            if i < 0 or i > 25:
                print("Некорректный ввод параметров")
                return 1
        return 0

    def settings(self):
        f = 1
        while f:
            c = int(input("Выберите рефлектор (UKW-A - 1, UKW-B - 2, UKW-C - 3): "))
            if c == 1:
                self.UKW = UKW.UKW().UKW_A
            elif c == 2:
                self.UKW = UKW.UKW().UKW_B
            elif c == 3:
                self.UKW = UKW.UKW().UKW_C
            else:
                print("Некорректный ввод")
                continue
            break

        f = 1
        while f:
            self.choice_rotors = list(map(int, input("Выберите 3 ротора (1-5): ").split(' ')))
            f = self.check_rotors()

        f = 1
        while f:
            self.rotor_pos = list(
                map(lambda x: int(x) - 1, input("Выберите стартовые положения для роторов (1-26): ").split()))
            f = self.check_poses()

        self.rotor_pos.append(0)
        print()
        c = -1
        while c != 1 and c != 0:
            c = int(input("Подключить коммутации?(1-да, 0-нет): "))
        if c:
            alphabet = [chr(_) for _ in range(65, 91)]
            print()
            print("Выбирайте по 2 буквы из алфавита и записывайте в формате буква буква (например A B)")
            print("Для завершения ввода ввести 0")
            print('------')
            while len(alphabet) >= 2:
                print(alphabet)
                connect = input("Введите соединение: ")
                if connect == "0":
                    print()
                    break

                connect = connect.split(' ')
                self.commutations[ord(connect[0].upper()) - 64] = ord(connect[-1].upper()) - 64
                self.commutations[ord(connect[-1].upper()) - 64] = ord(connect[0].upper()) - 64
                alphabet.remove(connect[0].upper())
                alphabet.remove(connect[1].upper())
        else:
            print()

    def settings_from_file(self, f):
        lines = f.split('\n')
        # print(lines)

        # выбор рефлектора
        try:
            r = int(lines[0])
        except ValueError:
            exit("Ошибка в выборе рефлектора.")

        if r == 1:
            self.UKW = UKW.UKW().UKW_A
        elif r == 2:
            self.UKW = UKW.UKW().UKW_B
        elif r == 3:
            self.UKW = UKW.UKW().UKW_C
        else:
            exit("Некорректный ввод рефлектора.")

        # выбор роторов
        self.choice_rotors = []
        for i in lines[1].split(' '):
            try:
                self.choice_rotors.append(int(i))
            except ValueError:
                exit("Ошибка в выборе ротора.")
        if self.check_rotors():
            exit("Ошибка при выборе роторов.")

        # выбор позиций
        self.rotor_pos = []
        for i in lines[2].split(' '):
            try:
                self.rotor_pos.append(int(i) - 1)
            except ValueError:
                exit("Ошибка в выборе стартовой позиции ротора.")
        if self.check_poses():
            exit("Ошибка при выборе стартовых позиций роторов.")
        self.rotor_pos.append(0)

        # коммутации
        if lines[3] != '0':
            l = lines[3].split(';')
            for connect in l:
                connect = connect.split(" ")
                connect = list(map(lambda s: s.upper(), connect))
                self.commutations[ord(connect[0].upper()) - 64] = ord(connect[-1].upper()) - 64
                self.commutations[ord(connect[-1].upper()) - 64] = ord(connect[0].upper()) - 64

    def rotate(self, rotor):
        if rotor == 3:
            self.rotor_pos[rotor - 1] += 1
            if self.rotor_pos[rotor - 1] > 26:
                self.rotor_pos[rotor - 1] = 1

        if self.rotors[rotor].notch == self.rotor_pos[rotor - 1] - 1:
            self.rotor_pos[rotor - 2] += 1
            if self.rotor_pos[rotor - 2] > 26:
                self.rotor_pos[rotor - 2] = 1

    def go(self, s, rotor, r):
        p = s + (self.rotor_pos[r - 1] - self.rotor_pos[r])
        if p > 26:
            p -= 26
        elif p < 1:
            p += 26
        s = self.rotors[rotor].go_through(p)
        return s

    def key_for_data(self, data, rotor):
        d = self.rotors[rotor].connections
        for i in d:
            if d[i] == data:
                return i
        return "Ошибка"

    def balance(self, s):
        if s > 26:
            s -= 26
        elif s < 1:
            s += 26
        return s

    def coding(self, letter):
        num_code = self.letters_to_numbers(letter)
        new_letter = ''
        for symbol in num_code:
            if symbol == ' ':
                new_letter += symbol
            else:
                # сигнал вперед
                if symbol in self.commutations:
                    s = self.commutations[symbol]
                    s = self.ETW[s]
                else:
                    s = self.ETW[symbol]
                for rotor in range(len(self.choice_rotors), 0, -1):
                    if rotor > 1:
                        self.rotate(rotor)

                    s = self.go(s, self.choice_rotors[rotor - 1], rotor)

                # сигнал назад
                s += 0 - self.rotor_pos[0]
                s = self.balance(s)
                s = self.UKW[s]

                for i in range(len(self.choice_rotors)):
                    if i == 0:
                        s += self.rotor_pos[i]
                    else:
                        s += self.rotor_pos[i] - self.rotor_pos[i - 1]
                    s = self.balance(s)
                    s = self.key_for_data(s, self.choice_rotors[i])

                s += 0 - self.rotor_pos[2]
                s = self.balance(s)

                for i in self.ETW:
                    if self.ETW[i] == s:
                        s = self.ETW[i]

                if s in self.commutations:
                    s = self.commutations[s]

                new_letter += chr(s + 64)

        return new_letter

    def letters_to_numbers(self, letter):
        num_code = []
        for i in letter:
            if i == ' ':
                num_code.append(i)
            else:
                num_code.append(ord(i.upper()) - 64)
        return num_code

    def send_message(self, target_ip, port=12345):
        letter = input("Введите сообщение: ")
        coded = self.coding(letter)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((target_ip, port))
            s.sendall(coded.encode('utf-8'))
            print(f"[Отправлено] Зашифрованное сообщение: {coded}")

    def receive_message(self, local_ip, port=12345):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((local_ip, port))
            s.listen()
            print(f"[Ожидание] Ожидаем подключение на {local_ip}:{port}...")
            conn, addr = s.accept()
            with conn:
                print(f"[Подключено] Получено соединение от {addr}")
                data = conn.recv(1024).decode('utf-8')
                print(f"[Получено] Зашифрованное сообщение: {data}")

                original = self.coding(data)
                print(f"[Расшифровка] Исходное сообщение: {original}")

    def connect_computer(self):
        mode = input(
            "Вы хотите отправить или принять сообщение? (1 - отправить/2 - получить/3 - не связываться): ").strip().lower()
        if mode == '1':
            ip = input("Введите IP-адрес получателя (192.168.0.xxx): ").strip()
            self.send_message(ip)
        elif mode == '2':
            my_ip = input("Введите свой IP-адрес (192.168.0.xxx): ").strip()
            self.receive_message(my_ip)
        elif mode == '3':
            letter = input("Введите сообщение: ")
            coded = self.coding(letter)
            print(coded)
        else:
            print("Ошибка")

    def user(self):
        f = open("settings.txt").read()
        if len(f) == 0:
            self.settings()
        else:
            self.settings_from_file(f)

        self.connect_computer()


if __name__ == "__main__":
    M = Machine()
    M.user()
