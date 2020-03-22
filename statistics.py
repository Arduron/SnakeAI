import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy
plt.ion()
class Stats:
    def __init__(self):
        self.numberofQ = []
        self.applesEaten = []
        self.fig = plt.figure()
        self.length = len(self.applesEaten)
        self.ax1 = self.fig.add_subplot(3,1,1)
        self.ax2 = self.fig.add_subplot(3,1,2)
        self.ax3 = self.fig.add_subplot(3,1,3)
        self.lines, = self.ax1.plot([],[], 'o')
        #Autoscale on unknown axis and known lims on the other
        self.ax1.set_autoscaley_on(True)


    def update(self, stateDict, eatenApple):
        self.numberofQ.append(len(stateDict.stateHash))
        self.applesEaten = eatenApple
        self.length = len(self.applesEaten)

    def on_running(self, lenDict, eatenApple):
        self.update(lenDict, eatenApple)
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(range(self.length))
        self.lines.set_ydata(self.numberofQ)
        #Need both of these in order to rescale
        self.ax1.relim()
        self.ax1.autoscale_view()
        #We need to draw *and* flush
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
        # self.ax1.clear()
        # self.ax2.clear()
        # self.ax3.clear()
        # self.ax1.plot(range(self.length), self.numberofQ)
        # self.ax2.plot(range(self.length), self.applesEaten)
        # plt.show(block = False)
        # plt.ioff()
        # plt.show
        # plt.pause(0.0001)

    def updatePlot(self, stateDict):
        ani = animation.FuncAnimation(self.fig, self.animatePlot, len(stateDict.stateHash), interval = 1000)
        plt.show(block = False)
