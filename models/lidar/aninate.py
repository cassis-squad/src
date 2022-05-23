#!/usr/bin/env python3
'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = '/dev/ttyUSB0'
DMAX = 4000
IMIN = 0
IMAX = 50

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,

def run():
    try: 
        lidar = RPLidar(PORT_NAME)
        fig = plt.figure()
        ax = plt.subplot(111, projection='polar')
        line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                               cmap=plt.cm.Greys_r, lw=0)
        ax.set_rmax(DMAX)
        ax.grid(True)

        iterator = lidar.iter_scans()
        ani = animation.FuncAnimation(fig, update_line,
            fargs=(iterator, line), interval=50)
        plt.show()
        for element in iterator:
            for e in element:
                e[1] = int(e[1])
                if e[1] < 90 and e[1] > 0 and e[2] < 200:
                    print(e)
        lidar.stop()
        lidar.disconnect()
    except KeyboardInterrupt:
        lidar.stop()
        lidar.disconnect()

if __name__ == '__main__':
    run()