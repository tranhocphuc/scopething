from bitlib import *
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import argparse
import time

frame = [np.zeros(12288)]


# def plot():
#     parser = argparse.ArgumentParser(
#         description='Plot waveforms from a csv file. Files from echos, features and raw data folder have header size of 5,4 and 9 respectively.')
#     parser.add_argument('-n', '--name', type=str,
#                         help='the name of the csv file')
#     parser.add_argument('-r', '--header', type=int, default=5,
#                         help='the header size of the csv file')
#     parser.add_argument('-i', '--interval', type=int, default=20,
#                         help='refresh rate of the plot')
#     parser.add_argument('-yt', '--ylim_top', type=float, default=4,
#                         help='refresh rate of the plot')
#     parser.add_argument('-yb', '--ylim_bottom', type=float, default=-4,
#                         help='refresh rate of the plot')
#     args = parser.parse_args()
#     data_plotter = DataPlotter(name=frame, data_headers_size=0,
#                                ylim_top=6, ylim_bottom=0, interval=args.interval)
#     data_plotter.show()


class DataAcquisition():
    def __init__(self):
        self.data = []
        self.stop = '0'

    def make_measurement(self, MY_RATE, MY_SIZE):
        self.MY_RATE = MY_RATE
        self.MY_SIZE = MY_SIZE
        TRUE = 1
        FALSE = 0
        print("Starting, attempting to open devices...")
        if (BL_Open('USB:/dev/ttyUSB1',1)==0):
            print ("  FAILED: all devices not found (check your probe file).")
        else: 
            print ('\nNumber of devices opened: %s' %BL_Count(BL_COUNT_DEVICE))
            print (" Library: %s (%s)\n\n" % (BL_Version(BL_VERSION_LIBRARY),BL_Version(BL_VERSION_BINDING)))
            
            BL_Select(BL_SELECT_DEVICE,0)
            BL_Mode(BL_MODE_FAST)

            print (" Capture: %d @ %.0fHz = %fs" % (BL_Size(),BL_Rate(MY_RATE),BL_Time()))
            BL_Intro(BL_ZERO); #How many seconds to capture before the trigger event- 0 by default
            BL_Delay(5); #How many seconds to capture after the trigger event- 0 by default
            BL_Rate(MY_RATE); # optional, default BL_MAX_RATE
            BL_Size(MY_SIZE); # optional default BL_MAX_SIZE

            BL_Select(BL_SELECT_CHANNEL,0);
            BL_Trigger(3.8, BL_TRIG_FALL); # my modification
            BL_Select(BL_SELECT_SOURCE,BL_SOURCE_POD); # use the POD input - the only one available
            BL_Range(BL_Count(BL_COUNT_RANGE)); # maximum range for y-axis - use this whenever possible
            BL_Offset(BL_ZERO); # Y-axis offset is set to zero as BL_ZERO
            BL_Enable(TRUE);

            print (" Bitscope Enabled")
            # DATA = []
            # global frame #Global variable for later use
            # for i in range(20):
            #     #BL_Trace(0.01, BL_SYNCHRONOUS) # version 1
            #     BL_Trace(BL_TRACE_FOREVER) # version 2
            #     #DATA.append(BL_Acquire())
            #     frame = np.array(BL_Acquire())
            #     #self.data.append(frame)
            # #pd.DataFrame(self.data).to_csv(root + "/data.csv", index=False)
            # BL_Close()
            #Close the library to release resources (we're done).

    def start_measure(self, fold):
        while True:
            try:
                BL_Trace(BL_TRACE_FOREVER)  # version 2
                # DATA.append(BL_Acquire())
                frame = np.array(BL_Acquire())
                self.data.append(frame)
                print(len(self.data))
            except KeyboardInterrupt:
                self.save(fold)
                print("Finished saving")
                break

    def save(self, fold):
        pd.DataFrame(self.data).to_csv(fold+"/data.csv", index= False)
        self.data = []


print(frame)

#How to use: python plot_data.py -n first.csv -r 0 -yt 6 -yb 0

class DataPlotter():
    def __init__(self, name, data_headers_size=9, ylim_top=4, ylim_bottom=4, interval=20):
        time.sleep(3)
        self.data = frame
        
        self.n_frames = self.data.shape[0]
        self.xlim = self.data.shape[0]
        self.ylim_top = ylim_top
        self.ylim_bottom = ylim_bottom
        self.interval = interval

        self.fig = plt.figure()
        self.ax = plt
        self.line, = self.ax.plot([], [], lw=2)
    
    def init(self):
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        plt.gcf()
        x = np.arange(self.xlim)
        # y = self.data[i]
        y = frame
        print(y[0])
        self.line.set_data(x, y)
        return self.line,

    def show(self):
        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init,frames=self.n_frames, interval=20, blit=True, repeat = True)
        plt.show()


# files from echos folder have header size of 5
# files from features folder have header size of 4
# files of raw data have header size of 9
#
# def plot():
#     parser = argparse.ArgumentParser(
#         description='Plot waveforms from a csv file. Files from echos, features and raw data folder have header size of 5,4 and 9 respectively.')
#     parser.add_argument('-n', '--name', type=str,
#                         help='the name of the csv file')
#     parser.add_argument('-r', '--header', type=int, default=5,
#                         help='the header size of the csv file')
#     parser.add_argument('-i', '--interval', type=int, default=20,
#                         help='refresh rate of the plot')
#     parser.add_argument('-yt', '--ylim_top', type=float, default=4,
#                         help='refresh rate of the plot')
#     parser.add_argument('-yb', '--ylim_bottom', type=float, default=-4,
#                         help='refresh rate of the plot')
#     args = parser.parse_args()
#     data_plotter = DataPlotter(name= frame, data_headers_size=0,
#                                ylim_top=6, ylim_bottom=0, interval=args.interval)
#     data_plotter.show()


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(
#         description='Plot waveforms from a csv file. Files from echos, features and raw data folder have header size of 5,4 and 9 respectively.')
#     parser.add_argument('-n', '--name', type=str,
#                         help='the name of the csv file')
#     parser.add_argument('-r', '--header', type=int, default=5,
#                         help='the header size of the csv file')
#     parser.add_argument('-i', '--interval', type=int, default=20,
#                         help='refresh rate of the plot')
#     parser.add_argument('-yt', '--ylim_top', type=float, default=4,
#                         help='refresh rate of the plot')
#     parser.add_argument('-yb', '--ylim_bottom', type=float, default=-4,
#                         help='refresh rate of the plot')
#     args = parser.parse_args()
#     def print_something():
#         while True:
#             print("hear")
#     def print_something_else():
#         while True:
#             print("listen")
#
#     #Thread for Data Acquisition
#     data_collect = DataAcquisition()
#     thread_collect = threading.Thread(target = data_collect.make_measurement, args= (1140000, 12288))
#     thread_collect.start()
#     #Main Thread for Plotting
#     data_plotter = DataPlotter(name=frame, data_headers_size=0,
#                                ylim_top=6, ylim_bottom=0, interval= args.interval)
#     data_plotter.show()


