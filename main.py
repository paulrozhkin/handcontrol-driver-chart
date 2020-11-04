import csv
import time
import matplotlib.pyplot as plt
import serial
import pandas as pd
import plotly.express as px
import numpy as np
from numpy.fft import rfft, rfftfreq
from numpy import abs as np_abs
from scipy.signal import butter, filtfilt


def read_motors():
    lines = []
    with serial.Serial('COM9', 115200, timeout=1) as ser:
        print('Start receive')
        print('Press CTRL+C for stop')
        try:
            while 1:
                try:
                    line = ser.readline().strip()
                    values = line.decode('ascii').split(',')
                    tick, adc = [int(s) for s in values]
                    lines.append([tick, adc])
                except ValueError:
                    print('Error parse data')
                    continue
        except KeyboardInterrupt:
            timeFileName = time.strftime("%Y%m%d-%H%M%S")
            with open('C:/DATA/MyProject/BigProjects/ProjectHand/hand/DriverChart/data/' + timeFileName + '.csv', 'w',
                      newline='') as csv_file:
                fieldnames = ['tick', 'adc']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                for line in lines:
                    if len(line) != 2:
                        print('Len != 2 for line' + line)
                        continue

                    writer.writerow({'tick': line[0], 'adc': line[1]})

            print('Data saved')


def plot_char(csv_path):
    print('Plot chart for ' + csv_path)
    df = pd.read_csv(csv_path, ";")

    fig = px.line(df, x='tick', y='adc', title='График изменения значения АЦП при сжатии/разжатии пальца')
    fig.show()


def spectrum(csv_path):
    print('Plot spectrum for ' + csv_path)
    df = pd.read_csv(csv_path)
    fs = 1000
    data = []
    for value in df['adc'].values:
        data.append(value)

    time = np.arange(0, len(data))

    # np.fft.fft
    spectrum_signal = rfft(data)
    spectrum_signal = (np_abs(spectrum_signal) / (len(data) / 2))

    plt.plot(rfftfreq(len(data), 1. / fs), spectrum_signal)
    plt.xlabel(u'Частота, Гц')
    plt.ylabel(u'Напряжение, мВ')
    plt.title(u'Спектр сигнала')
    plt.grid(True)
    plt.show()


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def filtration(csv_path):
    print('Filtration for ' + csv_path)
    df = pd.read_csv(csv_path, ";")

    data = []
    for value in df['adc'].values:
        data.append(value)

    fs = 1000.0
    cutoff = 20
    order = 6
    conditioned_signal = butter_highpass_filter(data, cutoff, fs, order)

    fig = px.line(conditioned_signal,
                  title='График изменения значения АЦП при сжатии/разжатии пальца с фильтром низких частот')
    fig.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # read_motors()
    # spectrum('C:/DATA/MyProject/BigProjects/ProjectHand/hand/DriverChart/data/full.csv')
    # plot_char('C:/DATA/MyProject/BigProjects/ProjectHand/hand/DriverChart/data/book.csv')
    filtration('C:/DATA/MyProject/BigProjects/ProjectHand/hand/DriverChart/data/full.csv')
