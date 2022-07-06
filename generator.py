import math
import random
from operations import *
import numpy as np
from matplotlib import pyplot as plt


# globalne parametry sa ustawione po to ze funkcja przekazywana jako argument do scipy.integrate.quad
# (patrz plik operations.py, obliczanie parametrow sygnalu, funkcja liczaca całke)
# może przyjmowac tylko jeden argument
# edit: może przyjać, więcej, trzeba je podac jako args(x1,x2...)
def setVariables(amplitude, term, time1, timeS, kw2, probability, sample_to_jump):
    global A, T, t1, ts, kw, p, ns
    A = amplitude
    T = term
    t1 = time1
    ts = timeS
    kw = kw2
    p = probability
    ns = sample_to_jump


def uniformly_distributed_noise(t):
    return random.uniform(-A, A)


# podanie amplitudy nie ma tu znaczenia bo w rozkladzie gaussa amplituda moze przyjmowac dowolne wartosci
def gaussian_noise(t):
    return random.gauss(0, 1)


# t - aktualny czas (wartość x)
def sinusoid(t):
    return A * np.sin((2 * np.pi / T) * (t - t1))


def sinusoid_one_half(t):
    return 0.5 * A * (np.sin((2 * np.pi / T) * (t - t1)) + np.abs(np.sin((2 * np.pi / T) * (t - t1))))


def sinusoid_two_half(t):
    return A * np.abs(np.sin((2 * np.pi / T) * (t - t1)))


def unit_jump(t):
    if t > ts:
        return 1
    elif t == ts:
        return (1 / 2) * A
    else:
        return 0


# kw - współczynnik wypełnienia
def rectangle(t):
    k = int((t - t1) / T)
    if (k * T + t1) <= t < (kw * T + k * T + t1):
        return A
    else:
        return 0


def symmetric_rectangle(t):
    k = int((t - t1) / T)
    if (k * T + t1) <= t < (kw * T + k * T + t1):
        return A
    else:
        return -A


# źle generuje sygnał, podpytac kogos o wzor
def triangle(t):
    # k = int((t - t1) / T)
    k = (int)((t / T) - (t1 / T))
    if (k * T + t1) <= t < (kw * T + k * T + t1):
        return (A / (kw * T)) * (t - k * T - t1)
    else:
        return (-A / (T * (1 - kw))) * (t - k * T - t1) + (A / (1 - kw))


def unit_impulse(sample_number):
    if ns == sample_number:
        return 1
    else:
        return 0


def impulse_noise(sample_number):
    random_number = random.randrange(0, 100, 1) / 100
    if random_number < p:
        return 1
    else:
        return 0


# Parametry: A - amplituda sygnału, t1 - czas pocztkowy(s), d - czas trwania sygnału(s)
# T - okres podstawowy, ts - czas, w którym następuje skok, f - czestotliwosc probkowania
# p - prawdopodbienstwo, ns - numer próbki, dla której następuje skok amplitudy
def generate_signal(type_of_signal, A, t1, d, T, ts, kw, f, ns, p):
    setVariables(A, T, t1, ts, kw, p, ns)
    x = []
    y = []
    number_of_samples = int(d * f)
    sample_interval = 1 / f  # okres probkowania - odległość między kolejnymi probkami
    if type_of_signal == unit_impulse or type_of_signal == impulse_noise:
        for sample_number in range(number_of_samples + 1):  # +1 bo od 0
            x.append(t1 + sample_number * sample_interval)
            y.append(type_of_signal(sample_number))
    else:
        for sample_number in range(number_of_samples + 1):  # +1 bo od 0
            x.append(t1 + sample_number * sample_interval)
            y.append(type_of_signal(x[sample_number]))
    return Signal(x, y, f, t1, T)


# tworzenie wykresów
def plot_discrete(signal):
    number_of_samples = len(signal.x)
    for sample_number in range(number_of_samples):  # +1 bo od 0
        plt.plot(signal.x[sample_number], signal.y[sample_number], marker="o", markeredgecolor="red",
                 markerfacecolor="red")
    # plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
    plt.grid()
    plt.show()


def plot_continuous(signal):
    plt.plot(signal.x, signal.y)
    # plt.xticks(np.arange(min(signal.x), max(signal.x) + 1, 1.0))
    plt.grid()
    plt.show()


# https://stackoverflow.com/questions/6986986/bin-size-in-matplotlib-histogram
# https://stackoverflow.com/questions/33203645/how-to-plot-a-histogram-using-matplotlib-in-python-with-a-list-of-data
def show_histogram(signal, number_of_intervals):
    plt.hist(signal.y, density=False, bins=number_of_intervals, edgecolor='white',
             linewidth=2)  # density=False would make counts
    plt.ylabel('Ilość próbek')
    plt.xlabel('Wartości amplitudy')
    plt.show()


def sampling(orginal_signal, new_fs):
    step = int(orginal_signal.f / new_fs)  # co którą probke bierzemy do nowego sygnału
    new_x = []
    new_y = []
    for i in range(0, len(orginal_signal.x), step):
        new_x.append(orginal_signal.x[i])
        new_y.append(orginal_signal.y[i])
    return Signal(new_x, new_y, new_fs, orginal_signal.t1, orginal_signal.T)


def quantization(orginal_signal, number_of_levels):
    max1 = max(orginal_signal.y)
    min1 = min(orginal_signal.y)
    quantized_values = []
    step = (max1 - min1) / number_of_levels
    for i in range(number_of_levels + 1):
        quantized_values.append(min1 + i * step)
    # print(quantized_values)

    temp = []
    for i in range(len(orginal_signal.y)):
        flag = False
        for j in range(number_of_levels):
            # wersja bez maksymalnej wartości
            # if quantized_values[j] <= orginal_signal.y[i] <= quantized_values[j + 1]:
            #     temp.append(quantized_values[j])
            # wersja z maksymalna wartością
            if quantized_values[j] <= orginal_signal.y[i] < quantized_values[j + 1]:
                flag = True
                temp.append(quantized_values[j])
        if not flag:
            temp.append(quantized_values[-1])
    return Signal(orginal_signal.x, temp, orginal_signal.f, orginal_signal.t1, orginal_signal.T)


def reconstruction_sinc(signal, n):
    # n - liczba probek
    # # Ts - odleglosc miedzy probkami
    # # t - aktualny czas (wartosc x)

    new_x = []
    Ts = 1 / signal.f  # odleglosc miedzy probkami
    step = Ts / (n + 1)  # nowa odleglosc miedzy probkami
    for i in range(len(signal.x)):
        new_x.append(signal.x[i])
        if i == len(signal.x) - 1:  # dla ostatniego elementu nie dodajemy bo wyjdziemy poza obszar trwania sygnalu
            break

        for j in range(1, n + 1):  # dodajemy n nowych probek ze zwielokrotniona wartoscia step
            new_x.append(signal.x[i] + j * step)
    new_y = []
    index = 0
    for i in range(len(signal.x)):
        new_y.append(signal.y[i])
        index = index + 1
        if i == len(signal.x) - 1:  # dla ostatniego elementu nie dodajemy bo wyjdziemy poza obszar trwania sygnalu
            break
        for j in range(n):  # dodajemy n nowych probek ze zwielokrotniona wartoscia step
            new_y.append(reconstruction_manager(signal, i, 1 / signal.f, n, new_x, index))
            index = index + 1
    return Signal(new_x, new_y, signal.f, signal.t1, signal.T)


def reconstruction_manager(signal, i, Ts, n, new_x, index_new_signal):
    left_range = i - int(n / 2)
    if left_range < 0:
        left_range = 0
    y_value = 0
    right_range = i + int(n / 2) + 2
    if right_range > len(signal.y):
        right_range = len(signal.y)

    tmp = []
    for j in range(left_range, right_range):
        y_value += signal.y[j] * sinc(new_x[index_new_signal] / Ts - j)
        tmp.append(y_value)

    print(tmp)
    return y_value


def sinc(t):
    if t == 0.0:
        return 1
    else:
        return math.sin(math.pi * t) / (math.pi * t)


def mse(signal, second_signal):
    mse_value = 0.0
    for i in range(len(signal.y)):
        mse_value += (signal.y[i] - second_signal.y[i]) ** 2
    return mse_value / len(signal.y)


def snr(signal, second_signal):
    numerator = 0
    denominator = 0
    for i in range(len(signal.y)):
        numerator += signal.y[i] ** 2
        denominator += (signal.y[i] - second_signal.y[i]) ** 2
    x = numerator / denominator
    return 10 * math.log(x, 10)


def psnr(signal, second_signal):
    max_y = max(signal.y)
    value = max_y / mse(signal, second_signal)
    return 10 * math.log(value, 10)


def md(signal, second_signal):
    md_value = 0
    for i in range(len(signal.y)):
        diff = abs(signal.y[i] - second_signal.y[i])
        if md_value < diff:
            md_value = diff
    return md_value
