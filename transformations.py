import math
import time

import numpy as np
from matplotlib import pyplot as plt
from numpy import trunc
from scipy.fft import fft
# from sympy import fwht
from scipy.linalg import hadamard


def S2(t):
    return 2 * math.sin(math.pi * t) + math.sin(2 * math.pi * t) + 5 * math.sin((2 * math.pi) / 0.5 * t)


def chart(x, y):
    plt.figure()
    plt.plot(x, y)
    # plt.xticks(np.arange(min(signal.x), max(signal.x) + 1, 1.0))
    plt.grid()
    plt.show()


def W(k, n, N):
    re = math.cos((2 * math.pi * k * n) / N)
    im = math.sin((2 * math.pi * k * n) / N)
    return complex(re, -im)


def modul(c):
    a = pow(c.real, 2)
    b = pow(c.imag, 2)
    return math.sqrt(a + b)


def argument(c):
    return np.angle(c)
    # arctg = math.atan2(c.imag, c.real)
    # if c.real > 0:
    #     return arctg
    # elif c.real < 0:
    #     return arctg + math.pi
    # elif c.real == 0 and c.imag > 0:
    #     return 1/2 * math.pi
    # else:
    #     return -1/2 * math.pi


def DFT(x):
    start = time.time()
    N = len(x)
    X = []
    for k in range(N):
        summ = 0
        for n in range(N):
            w = W(k, n, N)
            summ += x[n] * w
        X.append(summ)
    end = time.time()
    print('czas trwania: ' + str(end - start))
    return X


def motyl(a, b, n, N, flag):
    if flag:
        return complex(a + b), complex(a - b)
    else:
        return complex(a + b), complex((a - b) * W(1, n, N))


# m to jest ilu bitowy zapis liczby, np. m=3 to 010, m=4 to 0010
def permutation(x, m):
    new_x = x.copy()
    for i in range(len(x)):
        tmp = format(i, 'b')
        while len(tmp) < m:
            tmp = '0' + tmp
        new_index = int(tmp[::-1], 2)
        new_x[new_index] = x[i]
    return new_x


# tablica wejsciowa musi byc spermutowana na parzyste i nieparzyste!!!
def FFT2F(x):
    start = time.time()
    X = x.copy()
    N = len(x)  # liczba probek wejsciowych, musi byc 2^m, gdzie m=1..10
    le = int(math.log2(N))  # liczba etapow
    lb = 1  # liczba blokow
    lm = N // 2  # liczba motylkow w bloku
    # petla po etapach
    for i in range(le):
        # print('---------ETAP ' + str(i) + '-----------------')
        for j in range(lb):
            # print('---------BLOK ' + str(j) + '-----------------')
            for k in range(lm):
                i1 = k + (lm * 2) * j  # indeks pierwszego wejscie do motylka
                i2 = i1 + lm  # indeks drugiego wejscie do motylka
                # print(i1, i2)
                n = k * pow(2, i)
                if i == (le - 1):
                    # k jako wykładnik do motylka ( w instrukcji to jest n)
                    X[i1], X[i2] = motyl(X[i1], X[i2], n, N, True)
                else:
                    X[i1], X[i2] = motyl(X[i1], X[i2], n, N, False)
        lb *= 2
        lm //= 2
    end = time.time()
    print('czas trwania: ' + str(end - start))
    return permutation(X, le)


def WHT(x):
    start = time.time()
    H = hadamard(len(x))
    # H = [(1 / math.sqrt(2)) * i for i in H]
    res = np.matmul(x, H)
    res = [(1 / math.sqrt(2)) * i for i in res]
    end = time.time()
    print('czas trwania: ' + str(end - start))
    return res


def FWHT(x):
    start = time.time()
    N = len(x)
    H = hadamard(N//2)
    x1 = [x[i] + x[(N // 2) + i] for i in range(N // 2)]
    x2 = [x[i] - x[(N // 2) + i] for i in range(N // 2)]
    res1 = np.matmul(x1, H)
    res2 = np.matmul(x2, H)
    res = [*res1, *res2]
    res = [(1 / math.sqrt(2)) * i for i in res]
    end = time.time()
    print('czas trwania: ' + str(end - start))
    return res


# x = [i/16 for i in range(16)]
# y = [i/16 for i in range(16)]
# print('---------DFT----------')
# print(DFT(x))
# print('---------FFT-scipy----------')
# print(fft(x))
# print('---------FFT----------')
# print(FFT2F(x))
# print('---------FWHT-sympy----------')
# print(fwht(x))
# print('---------FWHT----------')
# print(WHT(y))
