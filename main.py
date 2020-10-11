import csv
import time
import matplotlib.pyplot as plt
import serial
import pandas as pd
import plotly.express as px


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
    df = pd.read_csv(csv_path)

    fig = px.line(df, x='tick', y='adc', title='График изменения значения АЦП при сжатии/разжатии пальца')
    fig.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # read_motors()
    plot_char('C:/DATA/MyProject/BigProjects/ProjectHand/hand/DriverChart/data/Сжать/20201011-011829.csv')
