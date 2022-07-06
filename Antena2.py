import numpy as np
from generator import *
from operations import *

# na poczatku = 0, potem aktualizacja o delta t
time = 0
# lista do trzymania probek
probes = []
# odleglosc/pozycja obiektu - na poczatku 0
objectDistance = 20

# parametry anteny przekazywane przez użytkownika
end_time = 10
delta_t = 0.001
objectSpeed = 1
probesSpeed = 100
bufferSize = 20
reportingPeriod = 1
f = 100


def sinus(t):
    # return 1 * np.sin((2 * np.pi / 0.03) * (t - 0))
    return (1 * np.sin((2 * np.pi / 0.3) * (t - 0))) + (0.5 * np.sin((2 * np.pi / 0.8) * (t - 0)))

def report(signal):
    middle_index = int(len(signal) / 2)
    left_half = signal[:middle_index]
    index_of_max = len(left_half) - left_half.index(max(left_half))
    distance = (1/f * index_of_max * probesSpeed) / 2
    print("Distance from antena is: " + str(distance))
    indexes = [i for i in range(len(signal))]
    plt.plot(indexes, signal)
    plt.show()



s1 = generate_signal(sinus, 2, 0, 2, 3/5, 0, 0, f, 0, 0)

num_of_reports = int(end_time / reportingPeriod)
for i in range(num_of_reports):
    print("Real object distnace is: " + str(objectDistance))
    # obliczenie po jakim czasie wroci sygnał
    delay_time = (2 * objectDistance) / probesSpeed
    # print(delay_time)
    # aktualizacja pozycji obiektu
    objectDistance += objectSpeed * (reportingPeriod)
    # generacja sygnału z delayem
    s1_delayed = delay(s1, delay_time, sinus)
    # obliczenie korelacji
    s_corr = correlation(s1.y, s1_delayed.y)
    report(s_corr)

