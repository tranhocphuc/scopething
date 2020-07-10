
import numpy as np
from pylab import figure, plot, show
import pandas as pd
from analysis import annotate_series
from scope import await_, capture, main
from utils import DotDict
import time
import thread

#Phuc modi
data = [np.zeros(12288)]
await_(main())
class DataAcquisition():
    def __init__(self,period, nsamples, trigger_level, trigger_position,trace_delay):
        self.data = []
        self.period = period
        self.nsamples = nsamples
        self.trigger_level = trigger_level
        self.trigger_position = trigger_position
        self.trace_delay = trace_delay
    def Capture(self):
        global data
        for i in range(300):
            sample = capture(['A'], self.period, self.nsamples, self.trigger_level, self.trigger_position,self.trace_delay)
            data.append(sample['A'].samples)
            #data = np.array(sample['A].samples)

class SaveData():
    def __init__(self):
        self.data = data
    def SaveCSV(self):
        pd.DataFrame(data).to_csv('data.csv', index = False)

if __name__ = "__main__":
    start_time = time.time()
    data_collect = DataAcquisition(period=20e-3, nsamples=12288,trigger_level= -, trigger_position = 0, trace_delay = 2000)
    save_data = SaveData()

    thread_collect = threading.Thread(target = data_collect.Capture)
    thread_save = threading.Thread(target = save_data.SaveCSV)
    thread_collect.start()
    thread_save.start()
    finish = time.time()
    print("Took: {} seconds".format(finish-start_time))
#End Phuc modi

# o = 400
# m = 5
# n = o * m
# samples = square_wave(o)
# samples = np.hstack([samples] * m) * 2
# samples = np.hstack([samples[100:], samples[:100]])
# samples += np.random.normal(size=n) * 0.1
# samples += np.linspace(4.5, 5.5, n)
# series = DotDict(samples=samples, sample_rate=1000000)

# data = capture(['A'], period=20e-3, nsamples=2000)
# series = data.A
start_time = time.time()
print(" Capturing data...")
data = []
for i in range(300):
    sample = capture(['A'], period=20e-3, nsamples=12288, trigger_level=0, trigger_position=0, trace_delay=2000)
    data.append(sample['A'].samples)
capture_time = time.time()
print(" Capture time: {}s".format(capture_time - start_time))


print(" Saving data...")
pd.DataFrame(data).to_csv('data.csv', index=False)
print(" Save time: {}s".format(save_time - capture_time))
save_time = time.time()
# figure(1)
# plot(series.timestamps, series.samples)

# if annotate_series(series):
#     waveform = series.waveform
#     if 'duty_cycle' in waveform:
#         print(f"Found {waveform.frequency:.0f}Hz {waveform.shape} wave, "
#               f"with duty cycle {waveform.duty_cycle * 100:.0f}%, "
#               f"amplitude ±{waveform.amplitude:.1f}V and offset {waveform.offset:.1f}V")
#     else:
#         print(f"Found {waveform.frequency:.0f}Hz {waveform.shape} wave, "
#               f"with amplitude ±{waveform.amplitude:.2f}V and offset {waveform.offset:.2f}V")

#     plot(waveform.timestamps + waveform.capture_start - series.capture_start, waveform.samples * waveform.amplitude + waveform.offset)

# show()
