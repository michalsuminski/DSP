from generator import *
from fileOperator import *
from transformations import *
import time

h = count_filter_coeffs(51, 5, 400)
# print(h)
s1 = generate_signal(S2, 1, 0, 4, 1,  0, 0, 16, 0, 0)
s2 = generate_signal(sinusoid, 0.5, 0, 2, 1, 0, 0, 20, 0, 0)
# s12 = add_signals(s1, s2)

# sygnał opóźniony o 1 sek
s3 = generate_signal(sinusoid, 2,   1, 1, 1/3,  0, 0, 400, 0, 0)
s4 = generate_signal(sinusoid, 0.5, 1, 1, 1/20, 0, 0, 400, 0, 0)
s34 = add_signals(s3, s4)

X = FFT2F(s1.y[:-1])
print(X)
re = [i.real for i in X]
print(re)
im = [i.imag for i in X]
domain = [i*(1/s1.d) for i in range(len(s1.y[:-1]))]

mod = [modul(i) for i in X]
arg = [argument(i) for i in X]
print(arg)

# wykres czesci rzeczywistej
start = time.time()
chart(domain, fwht(s1.y[:-1]))
end = time.time()
print('czas trwania: ' + str(end - start))
start = time.time()
chart(domain, WHT(s1.y[:-1]))
end = time.time()
print('czas trwania: ' + str(end - start))
start = time.time()
chart(domain, FWHT(s1.y[:-1]))
end = time.time()
print('czas trwania: ' + str(end - start))
start = time.time()
chart(domain, DFT(s1.y[:-1]))
end = time.time()
print('czas trwania: ' + str(end - start))
start = time.time()
chart(domain, FFT2F(s1.y[:-1]))
end = time.time()
print('czas trwania: ' + str(end - start))
# chart(s1.x, s1.y)
# chart(domain, re)
# chart(domain, im)
# chart(domain, arg)
# chart(domain, mod)