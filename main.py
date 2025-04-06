import Rotors


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
        self.UKW = {
            1: 5,
            2: 10,
            3: 13,
            4: 26,
            5: 1,
            6: 12,
            7: 25,
            8: 24,
            9: 22,
            10: 2,
            11: 23,
            12: 6,
            13: 3,
            14: 18,
            15: 17,
            16: 21,
            17: 15,
            18: 14,
            19: 20,
            20: 19,
            21: 16,
            22: 9,
            23: 11,
            24: 8,
            25: 7,
            26: 4
        }  # рефлектор
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
            if i < 1 or i > 5:
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
                    break

                connect = connect.split(' ')
                self.commutations[ord(connect[0]) - 64] = ord(connect[-1]) - 64
                self.commutations[ord(connect[-1]) - 64] = ord(connect[0]) - 64
                alphabet.remove(connect[0])
                alphabet.remove(connect[1])

    def rotate(self, rotor):
        if self.rotors[rotor].notch == self.rotor_pos[rotor - 1] - 1:
            self.rotor_pos[rotor - 2] += 1

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
                    if rotor == 3:
                        self.rotor_pos[rotor - 1] += 1
                        self.rotate(rotor)
                        self.rotate(rotor - 1)

                        for i in range(len(self.rotor_pos) - 1):
                            if self.rotor_pos[i] == 27:
                                self.rotor_pos[i] = 1

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

                if s in self.commutations:
                    s = self.commutations[s]

                new_letter += chr(s + 64)

        print(new_letter)

    def letters_to_numbers(self, letter):
        num_code = []
        for i in letter:
            if i == ' ':
                num_code.append(i)
            else:
                num_code.append(ord(i.upper()) - 64)
        return num_code

    def user(self):
        self.settings()
        while 1:
            letter = input("\nВведите сообщение: ")
            if letter == '0':
                print("Работа завершена")
                break
            else:
                self.coding(letter)


M = Machine()
M.user()
