import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

class Stats:
    def __init__(self):
        self.numberofQ = []
        self.applesEaten = [0]
        self.fig = plt.figure()
        self.length = len(self.applesEaten)
        self.ax1 = self.fig.add_subplot(3,1,1)
        self.ax2 = self.fig.add_subplot(3,1,2)
        self.ax3 = self.fig.add_subplot(3,1,3)


    def update(self, stateDict, eatenApple):
        self.numberofQ.append(len(stateDict.stateHash))
        self.applesEaten = eatenApple
        self.length = len(self.applesEaten)
    
    def animatePlot(self, lenDict, eatenApple):
        plt.ion()
        self.update(lenDict, eatenApple)
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax1.plot(range(self.length), self.numberofQ)
        self.ax2.plot(range(self.length), self.applesEaten)
        plt.draw()
        plt.show(block = False)
        plt.ioff()
        plt.show
        # plt.pause(0.0001)

    def updatePlot(self, stateDict):
        ani = animation.FuncAnimation(self.fig, self.animatePlot, len(stateDict.stateHash), interval = 1000)
        plt.show(block = False)
