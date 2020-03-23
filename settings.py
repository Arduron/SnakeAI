#init values
#commonly used
verzögern = True
spielfeldgöße = [15,15] #Breite dann Höhe
training_games = 100
askToLoad = True
saveTrainingData = True

#uncommon
originalSnakeLength = 3
learningrate = 0.2
diskontierung = 0.9
epsilonStart = 0.9
epsilonDiscount = 0.99
verzögerung = 20.0/1000.0
plotIntervall = 10
baseName = 'TrainedModels/trainedState'
epsilonMin = 1000



class InitObject:
    def __init__(self, verzögern, spielfeldgöße, training_games, askToLoad, saveTrainingData, plotStats, plotIntervall):
        self.verzögern = verzögern
        self.spielfeldgöße = spielfeldgöße
        self.originalSnakeLength = originalSnakeLength
        self.learningrate = learningrate
        self.diskontierung = diskontierung
        self.epsilonStart = epsilonStart
        self.epsilonDiscount = epsilonDiscount
        self.training_games = training_games
        self.askToLoad = askToLoad
        self.verzögerung = verzögerung
        self.saveTrainingData = saveTrainingData
        self.plotStats = plotStats
        self.plotIntervall = plotIntervall
        self.meanQrange = 100
        self.meanApplesEaten = 100
        self.baseName = baseName
        self.epsilonMin = epsilonMin
    
