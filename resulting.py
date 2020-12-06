import matplotlib.pyplot as plt  # directory for saving
import os
import re
import math
import json
import csv
import png
import numpy as np
from scipy.signal import hilbert
import matplotlib
matplotlib.use('Agg')

def final(file, val, pref):
    max_data = max(map(max, val))
    min_data = min(map(min, val))
    data_color = [[int(255*(x-min_data)/(max_data-min_data)) for x in l] for l in val]
    with open(file+pref, 'wb') as fpng:
        w = png.Writer(len(val[0]), len(val), greyscale=True)
        w.write(fpng, data_color)

class Result:
    def __init__(self, dir = 'data/baseline/Sensor{}', conf = 'res/config.json'):
        #self.dir = 'data/baseline/Sensor{}' # directory for final files,by sensors
        with open(conf) as jf:
            configuration = json.load(jf)
            self.window = configuration['WINDOW']# Reading config
            self.number_of_sensors = configuration['NUMBER_OF_SENSORS']
        self.dir = dir
        self.cnt = 0
        self.raw_data = self.getRaw()
        
    def getRaw(self):
        file_names = []
        for i in range(self.number_of_sensors):
            file_name = os.listdir(self.dir.format(i))
            file_names.append(file_name)
        raws=[]
        tpl = r'^raw\d+.csv$'
        for dr in file_names:
            for i in dr:
                if re.match(tpl, i):
                    raws.append(i)
        return raws

    def hilbert(self):
        for one_file in self.raw_data:
            with open(self.dir.format(self.cnt) + '/'+ one_file) as fi:
                with open(self.dir.format(self.cnt)+"/hilb.csv", 'w') as fo:
                    vals_init = [[float(x) for x in l.split()] for l in fi.readlines()]
                    vals = list(zip(*vals_init))
                    # Narrowband filtering + Hilbert transformation
                    res_fft = []
                    maxf = 0
                    for i, row in enumerate(vals):
                        fft = np.fft.rfft(row)
                        # this is to check the spectrum and find the carrying freauency
                        # near-zero freqencies somehow are exremely large
                        plt.plot(np.abs(fft)[10:])
                        maxf += np.abs(fft)[10:].argmax()
                        #plt.savefig(args.output + "_fft_" + str(i) + ".png")
                        # plt.clf()

                    mid = maxf/len(vals)

                    for i, row in enumerate(vals):
                        fft = np.fft.rfft(row)
                        for j, freq in enumerate(fft):
                            # if not (args.freq_min <= j <= args.freq_max):
                            if not (mid - self.window/2.0 <= j <= mid + self.window/2.0):
                                fft[j] = 0
                        res_fft.append(np.abs(hilbert(np.fft.irfft(fft))))

                    print(mid)
                    # saving spectrum
                    plt.savefig(self.dir.format(self.cnt) +'/spectrum.png')
                    plt.cla()
                    res = list(zip(*res_fft))
                    max_data = max(map(max, res))
                    min_data = min(map(min, res))
                    for r in res:
                        stri = ""
                        for t in r:
                            stri += str(round((t - min_data)/(max_data-min_data), 2))
                            stri += " "
                        print(stri, file=fo)

                    with open(self.dir.format(self.cnt) + "/2hilb.csv", 'w') as fu:
                        for r in vals_init:
                            stri = ""
                            for t in r:
                                stri += str(round(t, 2))
                                stri += " "
                            print(stri, file=fu)

                    final(file=self.dir.format(self.cnt), val=vals_init, pref="/prehilb.png")
                    # writing final graphics
                    final(file=self.dir.format(self.cnt), val=res, pref="/2hilb.png")
            self.cnt += 1  # plussing to copy next files in another folder




result = Result()
result.hilbert()

        





