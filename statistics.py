import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

class Stats:
    def __init__(self):
        self.numberofQ = [0]
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)

    def update(self, stateDict):
        self.numberofQ.append(len(stateDict.stateHash))
    
    def animatePlot(self, lenDict):
        self.update(lenDict)
        self.ax1.clear()
        self.ax1.plot(range(len(self.numberofQ)), self.numberofQ)
        plt.draw()

    def updatePlot(self, stateDict):
        ani = animation.FuncAnimation(self.fig, self.animatePlot, len(stateDict.stateHash), interval = 1000)
        plt.show(block = False)
