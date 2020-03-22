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
        self.length = len(self.numberofQ)
        self.ax1 = self.fig.add_subplot(3,1,1)
        self.ax2 = self.fig.add_subplot(3,1,2)
        self.ax3 = self.fig.add_subplot(3,1,3)
        self.lines1, = self.ax1.plot([],[])
        self.lines2, = self.ax2.plot([],[])
        self.lines3, = self.ax3.plot([],[])
        #Autoscale on unknown axis and known lims on the other
        self.ax1.set_autoscaley_on(True)
        self.ax2.set_autoscaley_on(True)
        self.ax3.set_autoscaley_on(True)


    def update(self, stateDict, eatenApple):
        self.numberofQ.append(len(stateDict.stateHash))
        self.applesEaten = eatenApple
        self.length = len(self.numberofQ)

    def on_running(self, lenDict, eatenApple):
        self.update(lenDict, eatenApple)
        #Update data (with the new _and_ the old points)
        self.lines1.set_xdata(range(self.length))
        self.lines2.set_xdata(range(len(self.applesEaten)))
        self.lines3.set_xdata(range(len(self.applesEaten)))
        self.lines1.set_ydata(self.numberofQ)
        self.lines2.set_ydata(self.applesEaten)
        self.lines3.set_ydata(self.applesEaten)
        #Need both of these in order to rescale
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()
        self.ax3.relim()
        self.ax3.autoscale_view()
        #We need to draw *and* flush
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def updatePlot(self, stateDict):
        ani = animation.FuncAnimation(self.fig, self.animatePlot, len(stateDict.stateHash), interval = 1000)
        plt.show(block = False)
