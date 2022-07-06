import math

from scipy.integrate import quad
from math import sqrt


# obliczanie calki wzor wziety stad:
# https://stackoverflow.com/questions/32233026/find-the-numerical-integration-of-points-in-c-sharp
# metoda trapezow
def count_integral(x, y):
    integral = 0
    for i in range(1, len(x)):
        integral += (y[i] + y[i - 1]) / 2 * (x[i] - x[i - 1])
    return integral


class Signal:
    def __init__(self, x, y, f, t1, T):
        self.x = x
        self.y = y
        self.f = f
        self.t1 = t1
        self.T = T
        self.d = x[-1]

    # Uwaga: w przypadku, kiedy przyjęty zakres czasu nie jest wielokrotnością okresu
    # sygnału niepełny okres należy pominąć w obliczeniach
    def check_term_condition(self):
        if self.T == 0:
            return self.x, self.y
        elif type(self.d / self.T) != int:
            k = int(self.d / self.T)
            index = self.x.index(k * self.T)
            return self.x[:index], self.y[:index]
        else:
            return self.x, self.y

    # # https://www.southampton.ac.uk/~fangohr/teaching/python/book/html/16-scipy.html
    # def mean_continuous(self, function):
    #     t1 = self.x[0]
    #     t2 = self.x[-1]
    #     # quad zwraca krotke [wartość całki, bład obliczen]
    #     return (1 / (t2 - t1)) * quad(function, t1, t2)[0]

    def mean_continuous(self):
        x, y = self.check_term_condition()
        t1 = x[0]
        t2 = x[-1]
        return (1 / (t2 - t1)) * count_integral(x, y)

    def mean_discrete(self):
        x, y = self.check_term_condition()
        return 1 / (len(x) * sum(y))

    # tip: można porownac sobie wyniki funkcji liczacych
    # dla sygnalu ciaglego i dyskretnego i powinny byc praktycznie takie same

    def mean_abs_continuous(self):
        x, y = self.check_term_condition()
        t1 = x[0]
        t2 = x[-1]
        y1 = [abs(i) for i in y]
        return (1 / (t2 - t1)) * count_integral(x, y1)

    def mean_abs_discrete(self):
        x, y = self.check_term_condition()
        return 1 / len(x) * sum(map(abs, y))

    def mean_power_continuous(self):
        x, y = self.check_term_condition()
        t1 = x[0]
        t2 = x[-1]
        y1 = [pow(i, 2) for i in y]
        return (1 / (t2 - t1)) * count_integral(x, y1)

    def mean_power_discrete(self):
        x, y = self.check_term_condition()
        return 1 / len(x) * sum([pow(i, 2) for i in y])

    def variance_continuous(self):
        x, y = self.check_term_condition()
        t1 = x[0]
        t2 = x[-1]
        mean = self.mean_abs_continuous()
        y1 = [pow((i - mean), 2) for i in y]
        return (1 / (t2 - t1)) * count_integral(x, y1)

    def variance_discrete(self):
        x, y = self.check_term_condition()
        mean = self.mean_abs_continuous()
        return 1 / len(x) * sum([pow((i - mean), 2) for i in y])

    # rms - wartosc skuteczna
    def rms_continuous(self):
        return sqrt(self.mean_power_continuous())

    def rms_discrete(self):
        return sqrt(self.mean_power_discrete())


# Operacje matematyczne
def add_signals(s1, s2):
    res_y = []
    for index in range(len(s1.x)):
        res_y.append(s1.y[index] + s2.y[index])
    return Signal(s1.x, res_y, s1.f, s1.t1, s1.T)


def sub_signals(s1, s2):
    res_y = []
    for index in range(len(s1.x)):
        res_y.append(s1.y[index] - s2.y[index])
    return Signal(s1.x, res_y, s1.f, s1.t1, s1.T)


def mul_signals(s1, s2):
    res_y = []
    for index in range(len(s1.x)):
        res_y.append(s1.y[index] * s2.y[index])
    return Signal(s1.x, res_y, s1.f, s1.t1, s1.T)


def div_signals(s1, s2):
    res_y = []
    for index in range(len(s1.x)):
        # 1. co przyjmujemy w przypadku dzielenia przez 0
        # 2. druga sprawa co jeśli jest 0/0
        if s2.y[index] == 0:
            res_y.append(max(s2.y))
        else:
            res_y.append(s1.y[index] / s2.y[index])
    return Signal(s1.x, res_y, s1.f, s1.t1, s1.T)


# M - rzad filtru, f0 - czestotliwosc odciecia
def count_filter_coeffs(M, f0, fp):
    h = []
    K = fp / f0
    for n in range(M):
        if n == (M - 1) / 2:
            h.append(2 / K)
        else:
            n1 = n - ((M - 1) / 2)
            sin_arg = (2 * math.pi * n1) / K
            sin = math.sin(sin_arg)
            down = math.pi * n1
            h.append(sin / down)
            # h.append(math.sin((2*math.pi*(n-(M-1)/2)) / K) / math.pi*(n-(M-1)/2))
    return h


# przyjmujemy ze podajemy juz tylko wartosci sygnału czyli signal.y
def convolution(signal_x, signal_h):
    hx = []
    # splot daje w wyniku M+N-1 probek
    for n in range(len(signal_x) + len(signal_h) - 1):
        # obliczenie splotu dla jednej probki
        tmp = 0
        for k in range(len(signal_h)):
            # gdy wychodzimy poza zakres sygnału to wartość = 0
            if n - k < 0 or n - k >= len(signal_x):
                tmp += signal_h[k] * 0
            else:
                tmp += signal_h[k] * signal_x[n - k]
        hx.append(tmp)
    return hx


def correlation_using_convolution(signal_x, signal_h):
    signal_x = signal_x[::-1]
    return convolution(signal_x, signal_h)


def correlation(signal_x, signal_h):
    hx = []
    for n in range(len(signal_x) - 1, (-1) * (len(signal_x) + (len(signal_h) - len(signal_x))), -1):
        tmp = 0
        for k in range(len(signal_h)):
            if n + k < 0 or n + k >= len(signal_x):
                continue
            tmp += signal_h[k] * signal_x[n + k]
        hx.append(tmp)
    return hx


def filter_signal(signal, M, f0, type_of_filter, type_of_window):
    h = count_filter_coeffs(M, f0, signal.f)
    if type_of_window == "Hamminga":
        for i in range(len(h)):
            w = 0.53836 - (0.46164 * (math.cos((2 * math.pi * i) / M)))
            h[i] = h[i] * w

    if type_of_filter == "środkowoprzepustowy":
        for i in range(len(h)):
            s = 2 * math.sin(math.pi * i / 2)
            h[i] = h[i] * s
    filtered_y = convolution(signal.y, h)
    distance = signal.x[1] - signal.x[0]
    difference = len(filtered_y) - len(signal.x)
    for i in range(difference):
        signal.x.append(signal.x[-1] + distance)

    return Signal(signal.x, filtered_y, signal.f, signal.t1, signal.T)


def delay(signal, delay_in_seconds, func):
    new_y = []
    for i in range(len(signal.x)):
        new_y.append(func(signal.x[i] + delay_in_seconds)) # opóźnienie czasu

    return Signal(signal.x, new_y, signal.f, signal.t1, signal.T)


def convolution_manager(signal_1, signal_2):
    y = convolution(signal_1.y, signal_2.y)
    x = []
    okres_drgan = 1 / signal_1.f
    for i in range(len(y)):
        x.append(i * okres_drgan)
    indexes = [i for i in range(len(x))]
    return Signal(indexes, y, signal_1.f, 0, signal_1.T)


def correlation_manager(signal_1, signal_2):
    y = correlation_using_convolution(signal_1.y, signal_2.y)
    x = []
    okres_drgan = 1 / signal_1.f
    for i in range(len(y)):
        x.append(i * okres_drgan)
    indexes = [i for i in range(len(x))]
    return Signal(indexes, y, signal_1.f, 0, signal_1.T)


def correlation_using_convolution_manager(signal_1, signal_2):
    y = correlation(signal_1.y, signal_2.y)
    x = []
    okres_drgan = 1 / signal_1.f
    for i in range(len(y)):
        x.append(i * okres_drgan)
    indexes = [i for i in range(len(x))]
    return Signal(indexes, y, signal_1.f, 0, signal_1.T)



