"""
Matplotlib Animation Example

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from glob import glob
import pandas as pd
"""
# Load sensor's data
DATA_HEADERS_SIZE = 9
dataframe = pd.read_csv('1.csv', skiprows=[0], header=None)
data = dataframe.iloc[:, DATA_HEADERS_SIZE:].to_numpy()
xlim = data.shape[1]
n_frames = data.shape[0]

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, xlim), ylim=(-4, 4))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    x = np.arange(xlim)
    y = data[i]
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=n_frames, interval=20) #, blit=True)
# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
"""

class DataPlotter():
    def __init__(self, name, data_headers_size=9,
		ylim_top=4, ylim_bottom=4,
		interval=20):   

        dataframe = pd.read_csv(name, skiprows=[0], header=None)
        self.data = dataframe.iloc[:, data_headers_size:].to_numpy()
    
        self.n_frames = self.data.shape[0]
        self.xlim = self.data.shape[1]
        self.ylim_top = ylim_top
        self.ylim_bottom = ylim_bottom
        self.interval = interval

        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, self.xlim), ylim=(self.ylim_bottom, self.ylim_top))
        self.line, = self.ax.plot([], [], lw=2)
    
    def init(self):
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        x = np.arange(self.xlim)
        y = self.data[i]
        self.line.set_data(x, y)
        return self.line,

    def show(self):
        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init,
                                      frames=self.n_frames, interval=20, blit=True)
        plt.show()

# files from echos folder have header size of 5
# files from features folder have header size of 4
# files of raw data have header size of 9

import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Plot waveforms from a csv file. Files from echos, features and raw data folder have header size of 5,4 and 9 respectively.')
    
    parser.add_argument('-n','--name', type=str,
                        help='the name of the csv file')
    parser.add_argument('-r','--header', type=int, default=5,
                        help='the header size of the csv file')
    parser.add_argument('-i','--interval', type=int, default=20,
                        help='refresh rate of the plot')
    parser.add_argument('-yt','--ylim_top', type=float, default=4,
                        help='refresh rate of the plot')
    parser.add_argument('-yb','--ylim_bottom', type=float, default=-4,
                        help='refresh rate of the plot')
    args = parser.parse_args()

    name = args.name
    header_size = args.header
    ylim_top = args.ylim_top
    ylim_bottom = args.ylim_bottom
    interval = args.interval

    data_plotter = DataPlotter(name=name, data_headers_size=header_size,
                               ylim_top=ylim_top, ylim_bottom=ylim_bottom, interval=interval)
    
    data_plotter.show()

