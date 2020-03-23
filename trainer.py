from snake_game import App
from tqdm import tqdm
from qAufsatz import StateDict
from qAufsatz import QPolicy
from statistics import Stats
from os import path
import matplotlib.animation as animation
from settings import InitObject

import json
from matplotlib import pyplot 
    
verzögern = False
spielfeldgöße = [15,15] #Breite dann Höhe
training_games = 1000000
askToLoad = True
saveTrainingData = True
plotStats = True
plotInervall = 1000

initObject = InitObject(verzögern, spielfeldgöße, training_games, askToLoad, saveTrainingData, plotStats, plotInervall)

stateDict = StateDict(initObject)
polititian = QPolicy(initObject)    

EatenApples = []

# for sttistics
if plotStats:
    statistics = Stats(initObject)
    goPlot = input('Plot data? (y/n) ')
    if goPlot == 'y':
        statistics.on_init()

_exit = False
for i in tqdm(range(initObject.training_games)):
    
    _running = True
    
    snakeGame = App(initObject)    
    polititian.setEpsilon(i)
    EatenApples.append(0)
    appleDis = snakeGame.getAppleDis()

    while _running and not _exit:
        #get current state
        currentState = snakeGame.getState()

        #füge ihn zur liste
        stateDict.addState(currentState)

        #get Q values
        currentStateQ = stateDict.returnStateQ(currentState)

        #errechtne nächsten schritt
        nextAction = polititian.getAction(currentStateQ)

        #führe ihn aus
        _running = [0,0,0]
        _running = snakeGame.on_execute(nextAction)
        EatenApples[i] = _running[1]
        _exit = _running[2]
        _running = _running[0]
        
        #reward??
        result = snakeGame.getResult()

        appleDisOld = appleDis
        appleDis = snakeGame.getAppleDis()
        if appleDis < appleDisOld:
            rewardDis = 0.05
        elif appleDisOld < appleDis:
            rewardDis = -0.05
        else:
            rewardDis = 0
        if result[0] == 1:
            reward = 4 + rewardDis
        elif result[1] == 1:
            reward = -1 + rewardDis
        else:
            reward = 0 + rewardDis
        stateDict.QUpdate(currentState, nextAction, snakeGame.getState(), reward)

        
    #plot statistics
    if plotStats:
        statistics.update(stateDict, EatenApples[i])
        if goPlot == 'y' and i%initObject.plotIntervall == 0:
            statistics.on_running()

    if _exit:
        training_games = i + 1
        break 

if initObject.saveTrainingData:
    # save traiined state in s json file 
    with open(filename, 'w') as fp:
        json.dump(stateDict.stateHash, fp, indent=4)
    
# save traiined state in s json file 
with open(filename, 'w') as fp:
    json.dump(stateDict.stateHash, fp, indent=4)

if initObject.plotStats:
    statistics.on_init()
    statistics.on_running()
    pyplot.pause(100)
# fig2 = pyplot.figure()
# ax2 = fig2.add_subplot(1,1,1)  
# ax2.plot(range(training_games), EatenApples) 
pyplot.show()






