class RotorI:
    def __init__(self):
        self.notch = 25
        self.connections = {
            1: 5,
            2: 11,
            3: 13,
            4: 6,
            5: 12,
            6: 7,
            7: 4,
            8: 17,
            9: 22,
            10: 26,
            11: 14,
            12: 20,
            13: 15,
            14: 23,
            15: 25,
            16: 8,
            17: 24,
            18: 21,
            19: 19,
            20: 16,
            21: 1,
            22: 9,
            23: 2,
            24: 18,
            25: 3,
            26: 10
        }

    def go_through(self, pos):
        return self.connections[pos]


class RotorII:
    def __init__(self):
        self.notch = 13
        self.connections = {
            1: 1,
            2: 10,
            3: 4,
            4: 11,
            5: 19,
            6: 9,
            7: 18,
            8: 21,
            9: 24,
            10: 2,
            11: 12,
            12: 8,
            13: 23,
            14: 20,
            15: 13,
            16: 3,
            17: 17,
            18: 7,
            19: 26,
            20: 14,
            21: 16,
            22: 25,
            23: 6,
            24: 22,
            25: 15,
            26: 5
        }

    def go_through(self, pos):
        return self.connections[pos]


class RotorIII:
    def __init__(self):
        self.notch = 4
        self.connections = {
            1: 2,
            2: 4,
            3: 6,
            4: 8,
            5: 10,
            6: 12,
            7: 3,
            8: 16,
            9: 18,
            10: 20,
            11: 24,
            12: 22,
            13: 26,
            14: 14,
            15: 25,
            16: 5,
            17: 9,
            18: 23,
            19: 7,
            20: 1,
            21: 11,
            22: 13,
            23: 21,
            24: 19,
            25: 17,
            26: 15
        }


    def go_through(self, pos):
        return self.connections[pos]


class RotorIV:
    def __init__(self):
        self.notch = 18
        self.connections = {
            1: 5,
            2: 19,
            3: 15,
            4: 22,
            5: 16,
            6: 26,
            7: 10,
            8: 1,
            9: 25,
            10: 17,
            11: 21,
            12: 9,
            13: 18,
            14: 8,
            15: 24,
            16: 12,
            17: 14,
            18: 6,
            19: 20,
            20: 7,
            21: 11,
            22: 4,
            23: 3,
            24: 13,
            25: 23,
            26: 2
        }

    def go_through(self, pos):
        return self.connections[pos]


class RotorV:
    def __init__(self):
        self.notch = 8
        self.connections = {
            1: 22,
            2: 26,
            3: 2,
            4: 18,
            5: 7,
            6: 9,
            7: 20,
            8: 25,
            9: 21,
            10: 16,
            11: 19,
            12: 4,
            13: 14,
            14: 8,
            15: 12,
            16: 24,
            17: 1,
            18: 23,
            19: 13,
            20: 10,
            21: 17,
            22: 15,
            23: 6,
            24: 5,
            25: 3,
            26: 11
        }

    def go_through(self, pos):
        return self.connections[pos]
