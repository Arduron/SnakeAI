import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy
plt.ion()
class Stats:
    def __init__(self):
        self.numberofQ = []
        self.applesEaten = []
        self.meanQchange = []

    def on_init(self):
        self.fig, self.axs = plt.subplots(3, 1, constrained_layout=True)
        self.length = len(self.numberofQ)
        # self.axs[0] = self.fig.add_subplot(3,1,1)
        # self.axs[1] = self.fig.add_subplot(3,1,2)
        # self.axs[2] = self.fig.add_subplot(3,1,3)
        self.lines1, = self.axs[0].plot([],[])
        self.lines2, = self.axs[1].plot([],[])
        self.lines3, = self.axs[2].plot([],[])
        #Autoscale on unknown axis and known lims on the other
        self.axs[0].set_autoscaley_on(True)
        self.axs[1].set_autoscaley_on(True)
        self.axs[2].set_autoscaley_on(True)
        self.axs[0].grid()
        self.axs[1].grid()
        self.axs[2].grid()
        self.axs[0].set_title('No. of states')
        self.axs[1].set_title('Apples eaten')
        self.axs[2].set_title('Mean Q change')


    def update(self, stateDict, eatenApple):
        self.numberofQ.append(len(stateDict.stateHash))
        self.applesEaten = eatenApple
        self.meanQchange.append(stateDict.getMeanQ())
        self.length = len(self.numberofQ)

    def on_running(self):
        #Update data (with the new _and_ the old points)
        self.lines1.set_xdata(range(self.length))
        self.lines2.set_xdata(range(len(self.applesEaten)))
        self.lines3.set_xdata(range(self.length))
        self.lines1.set_ydata(self.numberofQ)
        self.lines2.set_ydata(self.applesEaten)
        self.lines3.set_ydata(self.meanQchange)
        #Need both of these in order to rescale
        self.axs[0].relim()
        self.axs[0].autoscale_view()
        self.axs[1].relim()
        self.axs[1].autoscale_view()
        self.axs[2].relim()
        self.axs[2].autoscale_view()
        #We need to draw *and* flush
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def updatePlot(self, stateDict):
        ani = animation.FuncAnimation(self.fig, self.animatePlot, len(stateDict.stateHash), interval = 1000)
        plt.show(block = False)
