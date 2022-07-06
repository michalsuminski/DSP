from tkinter import filedialog
from main import *
from tkinter import *

# TYPE_OF_SIGNAL = uniformly_distributed_noise
SIGNAL1 = generate_signal(uniformly_distributed_noise, 1, 0, 10, 0, 0, 0, 1000, 0, 0)
SIGNAL2 = generate_signal(uniformly_distributed_noise, 1, 0, 10, 0, 0, 0, 1000, 0, 0)


def choose_type_of_signal(var):
    # global TYPE_OF_SIGNAL
    if var == 'szum o rozkładzie jednostajnym':
        return uniformly_distributed_noise
    elif var == 'szum gaussowski':
        return gaussian_noise
    elif var == 'sygnał sinusoidalny':
        return sinusoid
    elif var == 'sygnał sinusoidalny wyprostowany jednopołówkowo':
        return sinusoid_one_half
    elif var == 'sygnał sinusoidalny wyprostowany dwupołówkowo':
        return sinusoid_two_half
    elif var == 'sygnał prostoktny':
        return rectangle
    elif var == 'sygnał prostokątny symetryczny':
        return symmetric_rectangle
    elif var == 'sygnał trójkątny':
        return triangle
    elif var == 'skok jednostkowy':
        return unit_jump
    elif var == 'impuls jednostkowy':
        return unit_impulse
    elif var == 'szum impulsowy':
        return impulse_noise
    elif var == 'S2':
        return S2


def assign_values_to_signals(signal, n):
    global SIGNAL1, SIGNAL2
    if n == 1:
        SIGNAL1 = signal
    else:
        SIGNAL2 = signal


def choose_type_of_plot(type_of_signal, n):
    if type_of_signal == unit_impulse or type_of_signal == impulse_noise:
        if n == 1:
            plot_discrete(SIGNAL1)
        else:
            plot_discrete(SIGNAL2)
    else:
        if n == 1:
            plot_continuous(SIGNAL1)
        else:
            plot_continuous(SIGNAL2)


def read_signal(n):
    global SIGNAL1, SIGNAL2
    filename = filedialog.askopenfilename(initialdir="./", title="Select file")
    if n == 1:
        SIGNAL1 = read_from_file(filename)
    else:
        SIGNAL2 = read_from_file(filename)


def set_text(e, text):
    e.delete(0, END)
    e.insert(0, text)


def show_parameters(signal):
    print(e_s1.get())
    if e_s1.get() == '1':
        # parametry rekonstrukcji
        set_text(e_mse, str(round(mse(SIGNAL1, SIGNAL2), 3)))
        set_text(e_snr, str(round(snr(SIGNAL1, SIGNAL2), 3)))
        set_text(e_psnr, str(round(psnr(SIGNAL1, SIGNAL2), 3)))
        set_text(e_md, str(round(md(SIGNAL1, SIGNAL2), 3)))
    else:
        set_text(e_skut, str(round(signal.rms_continuous(), 3)))
        set_text(e_ws, str(round(signal.mean_continuous(), 3)))
        set_text(e_bws, str(round(signal.mean_abs_continuous(), 3)))
        set_text(e_moc, str(round(signal.mean_power_continuous(), 3)))
        set_text(e_war, str(round(signal.variance_continuous(), 3)))
        # podstawowe parametry
        set_text(e_czestotoliwosc_probkowania, str(signal.f))
        set_text(e_okres, str(signal.T))
        set_text(e_czas_poczatkowy, str(signal.t1))
        set_text(e_czas_trwania, str(signal.d))
        set_text(e_amplituda, str("0"))
        set_text(e_probka_skoku, str("0"))
        set_text(e_prawdopodobienstwo, str("0"))
        set_text(e_wsp_wypelnienia, str("0"))
        set_text(e_czas_skoku, str("0"))


signals = ['szum o rozkładzie jednostajnym', 'szum gaussowski', 'sygnał sinusoidalny',
           'sygnał sinusoidalny wyprostowany jednopołówkowo',
           'sygnał sinusoidalny wyprostowany dwupołówkowo', 'sygnał prostokątny', 'sygnał prostokątny symetryczny',
           'sygnał trójkątny', 'skok jednostkowy', 'impuls jednostkowy', 'szum impulsowy', 'S2']

filters = ['dolnoprzepustowy', 'środkowoprzepustowy']

okno = ['prostokątne', 'Hamminga']

root = Tk()
root.title("Generator sygnału")
# root.configure(background="#f7cbc8")

# kolumny 0 i 1
label_funkcja = Label(root, anchor="center", text="Wybierz sygnał:", font=("Helvetica", 12), width=22)
label_funkcja.grid(row=0, column=0, ipady=10)

variable = StringVar(root)
variable.set(signals[0])
lista_sygnalow = OptionMenu(root, variable, *signals)
lista_sygnalow.grid(row=0, column=1, columnspan=2)

label_filtr = Label(root, anchor="center", text="Wybierz r.filtra:", font=("Helvetica", 12), width=22)
label_filtr.grid(row=0, column=4, ipady=10)

variable1 = StringVar(root)
variable1.set(filters[0])
lista_sygnalow = OptionMenu(root, variable1, *filters)
lista_sygnalow.grid(row=0, column=5, columnspan=2)

label_okno = Label(root, anchor="center", text="Wybierz r.okna:", font=("Helvetica", 12), width=22)
label_okno.grid(row=0, column=7, ipady=10)

variable2 = StringVar(root)
variable2.set(okno[0])
lista_sygnalow = OptionMenu(root, variable2, *okno)
lista_sygnalow.grid(row=0, column=8, columnspan=2)

label_amplituda = Label(root, anchor="center", text="Amplituda:", font=("Helvetica", 12), width=22)
label_amplituda.grid(row=1, column=0, ipady=10)

e_amplituda = Entry(root, font=("Helvetica", 12), width=5)
e_amplituda.grid(row=1, column=1, padx=10, pady=10)

label_czas_poczatkowy = Label(root, anchor="center", text="Czas poczatkowy:", font=("Helvetica", 12), width=22)
label_czas_poczatkowy.grid(row=2, column=0, ipady=10)

e_czas_poczatkowy = Entry(root, font=("Helvetica", 12), width=5)
e_czas_poczatkowy.grid(row=2, column=1, padx=10, pady=10)

label_czas_trwania = Label(root, anchor="center", text="Czas trwania:", font=("Helvetica", 12), width=22)
label_czas_trwania.grid(row=3, column=0, ipady=10)

e_czas_trwania = Entry(root, font=("Helvetica", 12), width=5)
e_czas_trwania.grid(row=3, column=1, padx=10, pady=10)

label_okres = Label(root, anchor="center", text="Okres:", font=("Helvetica", 12), width=22)
label_okres.grid(row=4, column=0, ipady=10)

e_okres = Entry(root, font=("Helvetica", 12), width=5)
e_okres.grid(row=4, column=1, padx=10, pady=10)

label_czas_skoku = Label(root, anchor="center", text="Czas skoku:", font=("Helvetica", 12), width=22)
label_czas_skoku.grid(row=5, column=0, ipady=10)

e_czas_skoku = Entry(root, font=("Helvetica", 12), width=5)
e_czas_skoku.grid(row=5, column=1, padx=10, pady=10)

label_wsp_wypelnienia = Label(root, anchor="center", text="Współczynnik wypełnienia:", font=("Helvetica", 12), width=22)
label_wsp_wypelnienia.grid(row=6, column=0, ipady=10)

e_wsp_wypelnienia = Entry(root, font=("Helvetica", 12), width=5)
e_wsp_wypelnienia.grid(row=6, column=1, padx=10, pady=10)

label_czestotoliwosc_probkowania = Label(root, anchor="center", text="Częstotoliwość próbkowania:",
                                         font=("Helvetica", 12), width=22)
label_czestotoliwosc_probkowania.grid(row=7, column=0, ipady=10)

e_czestotoliwosc_probkowania = Entry(root, font=("Helvetica", 12), width=5)
e_czestotoliwosc_probkowania.grid(row=7, column=1, padx=10, pady=10)

label_probka_skoku = Label(root, anchor="center", text="Numer próbki do skoku:", font=("Helvetica", 12), width=22)
label_probka_skoku.grid(row=8, column=0, ipady=10)

e_probka_skoku = Entry(root, font=("Helvetica", 12), width=5)
e_probka_skoku.grid(row=8, column=1, padx=10, pady=10)

label_prawdopodobienstwo = Label(root, anchor="center", text="Prawdopodobieństwo:", font=("Helvetica", 12), width=22)
label_prawdopodobienstwo.grid(row=9, column=0, ipady=10)

e_prawdopodobienstwo = Entry(root, font=("Helvetica", 12), width=5)
e_prawdopodobienstwo.grid(row=9, column=1, padx=10, pady=10)

label_histogram = Label(root, anchor="center", text="Ilość przedziałów:", font=("Helvetica", 12), width=22)
label_histogram.grid(row=10, column=0, ipady=10)

e_histogram = Entry(root, font=("Helvetica", 12), width=5)
e_histogram.grid(row=10, column=1, padx=10, pady=10)

label_l_poziomow_kwantowania = Label(root, anchor="center", text="L. poziomów kwantowania:", font=("Helvetica", 12),
                                     width=22)
label_l_poziomow_kwantowania.grid(row=11, column=0, ipady=10)

e_l_poziomow_kwantowania = Entry(root, font=("Helvetica", 12), width=5)
e_l_poziomow_kwantowania.grid(row=11, column=1, padx=10, pady=10)

label_sinc = Label(root, anchor="center", text="L. do rekonstrukcji SINC:", font=("Helvetica", 12), width=22)
label_sinc.grid(row=12, column=0, ipady=10)

e_sinc = Entry(root, font=("Helvetica", 12), width=5)
e_sinc.grid(row=12, column=1, padx=10, pady=10)

label_rzad_filtra = Label(root, anchor="center", text="Rząd filtra:", font=("Helvetica", 12), width=22)
label_rzad_filtra.grid(row=13, column=0, ipady=10)

e_rzad_filtra = Entry(root, font=("Helvetica", 12), width=5)
e_rzad_filtra.grid(row=13, column=1, padx=10, pady=10)

label_f_odciecia = Label(root, anchor="center", text="Częst. odcięcia:", font=("Helvetica", 12), width=22)
label_f_odciecia.grid(row=14, column=0, ipady=10)

e_f_odciecia = Entry(root, font=("Helvetica", 12), width=5)
e_f_odciecia.grid(row=14, column=1, padx=10, pady=10)

# kolumny 2 i 3
label_s1 = Label(root, anchor="w", text="Sygnał 1:", font=("Helvetica", 12), width=7)
label_s1.grid(row=1, column=2, ipady=10)

e_s1 = Entry(root, font=("Helvetica", 12), width=4)
e_s1.grid(row=1, column=3, padx=10, pady=10)

label_s2 = Label(root, anchor="w", text="Sygnał 2:", font=("Helvetica", 12), width=7)
label_s2.grid(row=2, column=2, ipady=10)

e_s2 = Entry(root, font=("Helvetica", 12), width=4)
e_s2.grid(row=2, column=3, padx=10, pady=10)

# kolumny 4, 5, 6, 7, 8, 9
button_generuj = Button(root, text="Generuj", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                        command=lambda: assign_values_to_signals(generate_signal(type_of_signal=choose_type_of_signal(
                            variable.get()), A=float(e_amplituda.get()), t1=float(e_czas_poczatkowy.get()),
                            d=float(e_czas_trwania.get()), T=float(e_okres.get()), ts=float(e_czas_skoku.get()),
                            kw=float(e_wsp_wypelnienia.get()), f=float(e_czestotoliwosc_probkowania.get()),
                            ns=float(e_probka_skoku.get()), p=float(e_prawdopodobienstwo.get())), 1))
button_generuj.grid(row=1, column=4)

button_wczytaj = Button(root, text="Wczytaj", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                        command=lambda: read_signal(1))
button_wczytaj.grid(row=1, column=5)

button_zapisz = Button(root, text="Zapisz", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                       command=lambda: write_to_file(SIGNAL1, filedialog.asksaveasfilename()))
button_zapisz.grid(row=1, column=6)

button_wykres = Button(root, text="Wykres", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                       command=lambda: choose_type_of_plot(choose_type_of_signal(variable.get()), 1))
button_wykres.grid(row=1, column=7)

button_histogram = Button(root, text="Histogram", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                          command=lambda: show_histogram(SIGNAL1, int(e_histogram.get())))
button_histogram.grid(row=1, column=8)

button_parametry = Button(root, text="Parametry", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                          command=lambda: show_parameters(SIGNAL1))
button_parametry.grid(row=1, column=9)

button_kwantuj = Button(root, text="Kwantyzacja", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                        command=lambda: assign_values_to_signals(
                            quantization(SIGNAL1, int(e_l_poziomow_kwantowania.get())), 1))
button_kwantuj.grid(row=1, column=10)

button_sinc = Button(root, text="SINC", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                     command=lambda: assign_values_to_signals(reconstruction_sinc(SIGNAL1, int(e_sinc.get())), 1))
button_sinc.grid(row=1, column=11)

button_filtruj = Button(root, text="Filtruj", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                        command=lambda: assign_values_to_signals(filter_signal(SIGNAL1, int(e_rzad_filtra.get()),
                                                                               int(e_f_odciecia.get()), variable1.get(),
                                                                               variable2.get()), 1))
button_filtruj.grid(row=1, column=12)

button_delay = Button(root, text="Delay", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                      command=lambda: assign_values_to_signals(delay(SIGNAL1, float(e_s1.get()), choose_type_of_signal(
                          variable.get())), 1))
button_delay.grid(row=3, column=8)

button_splot = Button(root, text="Splot", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                      command=lambda: assign_values_to_signals(convolution_manager(SIGNAL1, SIGNAL2), 2))
button_splot.grid(row=3, column=9)

button_korelacja = Button(root, text="Korelacja", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                          command=lambda: assign_values_to_signals(correlation_manager(SIGNAL1, SIGNAL2), 2))
button_korelacja.grid(row=3, column=10)

button_korelacja_ze_splot = Button(root, text="KorelacjaS", font=("Helvetica", 10), bg="blue", fg="white", width=15,
                                   command=lambda: assign_values_to_signals(
                                       correlation_using_convolution_manager(SIGNAL1, SIGNAL2), 2))
button_korelacja_ze_splot.grid(row=3, column=11)

# PRZYCISKI NA TRANSFORMCJE
button_dft = Button(root, text="DFT", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                          command=lambda: assign_values_to_signals(DFT(SIGNAL1.y[:-1]), 1))
button_dft.grid(row=3, column=6)

button_fft = Button(root, text="FFT2f", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                            command=lambda: assign_values_to_signals(FFT2F(SIGNAL1.y[:-1]), 1))
button_fft.grid(row=4, column=6)


button_wh = Button(root, text="W-H", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                          command=lambda: chart([i*(1/SIGNAL2.d) for i in range(len(SIGNAL2.y[:-1]))], WHT(SIGNAL1.y[:-1])))
button_wh.grid(row=3, column=7)

button_fast_wh = Button(root, text="FWH", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                            command=lambda: chart([i*(1/SIGNAL2.d) for i in range(len(SIGNAL2.y[:-1]))], FWHT(SIGNAL1.y[:-1])))
button_fast_wh.grid(row=4, column=7)

button_re = Button(root, text="Re", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                      command=lambda: chart([i*(1/SIGNAL2.d) for i in range(len(SIGNAL2.y[:-1]))], [i.real for i in SIGNAL1]))
button_re.grid(row=4, column=8)

button_im = Button(root, text="Im", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                      command=lambda: chart([i*(1/SIGNAL2.d) for i in range(len(SIGNAL2.y[:-1]))], [i.imag for i in SIGNAL1]))
button_im.grid(row=4, column=9)

button_arg = Button(root, text="Arg", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                          command=lambda: chart([i*(1/SIGNAL2.d) for i in range(len(SIGNAL2.y[:-1]))], [argument(i) for i in SIGNAL1]))
button_arg.grid(row=4, column=10)

button_mod = Button(root, text="Mod", font=("Helvetica", 10), bg="blue", fg="white", width=15,
                                   command=lambda: chart([i*(1/SIGNAL2.d) for i in range(len(SIGNAL2.y[:-1]))], [modul(i) for i in SIGNAL1]))
button_mod.grid(row=4, column=11)

button_generuj2 = Button(root, text="Generuj", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                         command=lambda: assign_values_to_signals(generate_signal(type_of_signal=choose_type_of_signal(
                             variable.get()), A=float(e_amplituda.get()), t1=float(e_czas_poczatkowy.get()),
                             d=float(e_czas_trwania.get()), T=float(e_okres.get()), ts=float(e_czas_skoku.get()),
                             kw=float(e_wsp_wypelnienia.get()), f=float(e_czestotoliwosc_probkowania.get()),
                             ns=float(e_probka_skoku.get()), p=float(e_prawdopodobienstwo.get())), 2)
                         )
button_generuj2.grid(row=2, column=4)

button_wczytaj2 = Button(root, text="Wczytaj", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                         command=lambda: read_signal(2))
button_wczytaj2.grid(row=2, column=5)

button_zapisz2 = Button(root, text="Zapisz", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                        command=lambda: write_to_file(SIGNAL2, filedialog.asksaveasfilename()))
button_zapisz2.grid(row=2, column=6)

button_wykres2 = Button(root, text="Wykres", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                        command=lambda: choose_type_of_plot(choose_type_of_signal(variable.get()), 2))
button_wykres2.grid(row=2, column=7)

button_histogram2 = Button(root, text="Histogram", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                           command=lambda: show_histogram(SIGNAL2, int(e_histogram.get())))
button_histogram2.grid(row=2, column=8)

button_parametry2 = Button(root, text="Parametry", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                           command=lambda: show_parameters(SIGNAL2))
button_parametry2.grid(row=2, column=9)

button_kwantuj2 = Button(root, text="Kwantyzacja", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                         command=lambda: assign_values_to_signals(
                             quantization(SIGNAL2, int(e_l_poziomow_kwantowania.get())), 2))
button_kwantuj2.grid(row=2, column=10)

# musimy mieć juz spróbkowany i skwantowany sygnał
button_sinc2 = Button(root, text="SINC", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                      command=lambda: assign_values_to_signals(reconstruction_sinc(SIGNAL2, int(e_sinc.get())), 2))
button_sinc2.grid(row=2, column=11)

button_filtruj2 = Button(root, text="Filtruj", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                         command=lambda: assign_values_to_signals(filter_signal(SIGNAL2, int(e_rzad_filtra.get()),
                                                                                int(e_f_odciecia.get()),
                                                                                variable1.get(), variable2.get()), 2))
button_filtruj2.grid(row=2, column=12)

# przyciski na operacje
button_dodawanie = Button(root, text="Dodawanie", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                          command=lambda: write_to_file(add_signals(SIGNAL1, SIGNAL2), filedialog.asksaveasfilename()))
button_dodawanie.grid(row=3, column=4)

button_odejmowanie = Button(root, text="Odejmowanie", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                            command=lambda: write_to_file(sub_signals(SIGNAL1, SIGNAL2),
                                                          filedialog.asksaveasfilename()))
button_odejmowanie.grid(row=3, column=5)

button_mnozenie = Button(root, text="Mnożenie", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                         command=lambda: write_to_file(mul_signals(SIGNAL1, SIGNAL2), filedialog.asksaveasfilename()))
button_mnozenie.grid(row=4, column=4)

button_dzielenie = Button(root, text="Dzielenie", font=("Helvetica", 10), bg="blue", fg="white", width=10,
                          command=lambda: write_to_file(div_signals(SIGNAL1, SIGNAL2), filedialog.asksaveasfilename()))
button_dzielenie.grid(row=4, column=5)

# parametry sygnału
label_ws = Label(root, anchor="w", text="Wartość średnia:", font=("Helvetica", 12))
label_ws.grid(row=5, column=2, columnspan=3, ipady=10)

e_ws = Entry(root, font=("Helvetica", 12), width=15)
e_ws.grid(row=5, column=5, columnspan=3, padx=10, pady=10)

label_bws = Label(root, anchor="w", text="Bezwzględna wartość średnia:", font=("Helvetica", 12))
label_bws.grid(row=6, column=2, columnspan=3, ipady=10)

e_bws = Entry(root, font=("Helvetica", 12), width=15)
e_bws.grid(row=6, column=5, columnspan=3, padx=10, pady=10)

label_moc = Label(root, anchor="w", text="Moc średnia:", font=("Helvetica", 12))
label_moc.grid(row=7, column=2, columnspan=3, ipady=10)

e_moc = Entry(root, font=("Helvetica", 12), width=15)
e_moc.grid(row=7, column=5, columnspan=3, padx=10, pady=10)

label_war = Label(root, anchor="w", text="Wariancja:", font=("Helvetica", 12))
label_war.grid(row=8, column=2, columnspan=3, ipady=10)

e_war = Entry(root, font=("Helvetica", 12), width=15)
e_war.grid(row=8, column=5, columnspan=3, padx=10, pady=10)

label_skut = Label(root, anchor="w", text="Wartość skuteczna:", font=("Helvetica", 12))
label_skut.grid(row=9, column=2, columnspan=3, ipady=10)

e_skut = Entry(root, font=("Helvetica", 12), width=15)
e_skut.grid(row=9, column=5, columnspan=3, padx=10, pady=10)

# parametry sygnału
label_mse = Label(root, anchor="w", text="MSE:", font=("Helvetica", 12))
label_mse.grid(row=5, column=8, columnspan=2, ipady=10)

e_mse = Entry(root, font=("Helvetica", 12), width=15)
e_mse.grid(row=5, column=10, columnspan=2, padx=10, pady=10)

label_snr = Label(root, anchor="w", text="SNR:", font=("Helvetica", 12))
label_snr.grid(row=6, column=8, columnspan=2, ipady=10)

e_snr = Entry(root, font=("Helvetica", 12), width=15)
e_snr.grid(row=6, column=10, columnspan=2, padx=10, pady=10)

label_psnr = Label(root, anchor="w", text="PSNR:", font=("Helvetica", 12))
label_psnr.grid(row=7, column=8, columnspan=2, ipady=10)

e_psnr = Entry(root, font=("Helvetica", 12), width=15)
e_psnr.grid(row=7, column=10, columnspan=2, padx=10, pady=10)

label_md = Label(root, anchor="w", text="MD:", font=("Helvetica", 12))
label_md.grid(row=8, column=8, columnspan=2, ipady=10)

e_md = Entry(root, font=("Helvetica", 12), width=15)
e_md.grid(row=8, column=10, columnspan=2, padx=10, pady=10)

# stopka
title = Label(root, text="Michał Sumiński 230013, Jan Płoszaj 229985", font=("Helvetica", 8))
title.grid(row=14, column=2, columnspan=4)

root.mainloop()
