from generator import *
from array import array

# https://stackoverflow.com/questions/807863/how-to-output-list-of-floats-to-a-binary-file-in-python
def write_to_file(signal, filename):
    # 3 miejsce w tablicy rodzaj wartosci => 0-rzeczywiste, 1-zespolone
    tab = [signal.t1, signal.f, 0, signal.T, *signal.y]
    output_file = open(filename, 'wb')
    float_array = array('d', tab)
    # print(float_array)
    float_array.tofile(output_file)
    output_file.close()


def read_from_file(filename):
    input_file = open(filename, 'rb')
    float_array = array('d')
    float_array.frombytes(input_file.read())
    # print(float_array)
    t1 = float_array[0]
    f = float_array[1]
    T = float_array[2]
    y = list(float_array[4:])
    x = []
    sample_interval = 1 / f
    for i in range(len(y)):
        x.append(t1 + i * sample_interval)
    return Signal(x, y, f, t1, T)
