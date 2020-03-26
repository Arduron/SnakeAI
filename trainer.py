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
from helperfunctions import SaveStuff
    
verzögern = False
spielfeldgöße = [15,15] #Breite dann Höhe
training_games = 30000
askToLoad = False
saveTrainingData = True
plotStats = True
plotInervall = 100

initObject = InitObject(verzögern, spielfeldgöße, training_games, askToLoad, saveTrainingData, plotStats, plotInervall)

stateDict = StateDict(initObject)
polititian = QPolicy(initObject) 
saveStuff = SaveStuff(initObject)  
saveStuff.initSaving(stateDict, polititian)

EatenApples = 0

# for sttistics
statistics = Stats(initObject)
statistics.on_init()

_exit = False
for i in tqdm(range(initObject.training_games)):
    
    _running = True
    
    snakeGame = App(initObject)    
    polititian.setEpsilon(i)
    EatenApples = 0
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
        EatenApples = _running[1]
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
    if initObject.plotStats:
        statistics.update(stateDict, EatenApples)
        statistics.on_running(i)

    if _exit:
        training_games = i + 1
        break 

#save statistics plot
statistics.safeIt()

#save Training Data and Stats 
if initObject.saveTrainingData:
    saveStuff.saveIt(stateDict.stateHash, statistics.getStats())






