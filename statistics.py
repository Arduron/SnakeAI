import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy
from os import path

plt.ion()
class Stats:
    def __init__(self, initObject):
        self.numberofQ = []
        self.applesEaten = []
        self.meanQchange = []
        self.meanApplesEaten = []
        self.initObject = initObject
        self.baseName = initObject.baseName

    def getStats(self):
        return {'numberofQ':self.numberofQ, 'applesEaten': self.applesEaten,\
                'meanQchange': self.meanQchange, 'meanApplesEaten':self.meanApplesEaten}

    def on_init(self):
        if self.initObject.plotStats:
            self.init_plots()
            # self.goPlot = input('Plot data? (y/n) ')
            self.goPlot = 'y'
            #     self.init_plots()
                 
    def init_plots(self):
        self.fig, self.axs = plt.subplots(3, 2, constrained_layout=True)
        self.length = len(self.numberofQ)
        # self.axs[0,0] = self.fig.add_subplot(3,1,1)
        # self.axs[1,0] = self.fig.add_subplot(3,1,2)
        # self.axs[2,0] = self.fig.add_subplot(3,1,3)
        self.lines1, = self.axs[0,0].plot([],[])
        self.lines2, = self.axs[1,0].plot([],[])
        self.lines3, = self.axs[2,0].plot([],[])
        self.lines4, = self.axs[0,1].plot([],[])
        self.lines5, = self.axs[1,1].plot([],[])
        self.lines6, = self.axs[2,1].plot([],[])

        #Autoscale on unknown axis and known lims on the other
        self.axs[0,0].set_autoscaley_on(True)
        self.axs[1,0].set_autoscaley_on(True)
        self.axs[2,0].set_autoscaley_on(True)
        self.axs[0,0].grid()
        self.axs[1,0].grid()
        self.axs[2,0].grid()
        self.axs[0,1].grid()
        self.axs[1,1].grid()
        self.axs[2,1].grid()
        self.axs[0,0].set_title('No. of states')
        self.axs[1,0].set_title('Apples eaten')
        self.axs[2,0].set_title('Mean Q change')
        self.axs[0,1].set_title('Mean apples Eaten')
        self.axs[1,1].set_title(' ')
        self.axs[2,1].set_title(' ')

    def update(self, stateDict, eatenApple):
        self.numberofQ.append(len(stateDict.stateHash))
        self.applesEaten.append(eatenApple - self.initObject.originalSnakeLength)
        
        start = len(self.applesEaten) - self.initObject.meanApplesEaten
        newMean = 0
        if start < 0:
            start = 0
        for i in range(start, len(self.applesEaten)):
            newMean = newMean + self.applesEaten[i]
        newMean = newMean / (len(self.applesEaten) - start)
        self.meanApplesEaten.append(newMean)

        self.meanQchange.append(stateDict.getMeanQ())
        self.length = len(self.numberofQ)

    def on_running(self, i):
        if self.goPlot == 'y' and i%self.initObject.plotIntervall == 0: 
            #Update data (with the new _and_ the old points)
            self.lines1.set_xdata(range(self.length))
            self.lines2.set_xdata(range(len(self.applesEaten)))
            self.lines3.set_xdata(range(self.length))
            self.lines4.set_xdata(range(self.length))
            # self.lines5.set_xdata(range(len(self.applesEaten)))
            # self.lines6.set_xdata(range(self.length))
            self.lines1.set_ydata(self.numberofQ)
            self.lines2.set_ydata(self.applesEaten)
            self.lines3.set_ydata(self.meanQchange)
            self.lines4.set_ydata(self.meanApplesEaten)
            # self.lines5.set_ydata(self.applesEaten)
            # self.lines6.set_ydata(self.meanQchange)
            #Need both of these in order to rescale
            self.axs[0,0].relim()
            self.axs[0,0].autoscale_view()
            self.axs[1,0].relim()
            self.axs[1,0].autoscale_view()
            self.axs[2,0].relim()
            self.axs[2,0].autoscale_view()
            self.axs[0,1].relim()
            self.axs[0,1].autoscale_view()
            self.axs[1,1].relim()
            self.axs[1,1].autoscale_view()
            self.axs[2,1].relim()
            self.axs[2,1].autoscale_view()
            #We need to draw *and* flush
            self.fig.canvas.draw()
            if i == 0:
                self.fig.canvas.flush_events()
            
    
    def safeIt(self):
        self.init_plots()
        self.goPlot = 'y'
        self.on_running(0)
        modelNr = 1
        filename = self.baseName + str(modelNr) + '.png'
        while path.exists(filename):
            modelNr = int(modelNr) + 1
            filename = self.baseName + str(modelNr) + '.png'
        self.fig.savefig(filename)
        self.fig.canvas.flush_events()

