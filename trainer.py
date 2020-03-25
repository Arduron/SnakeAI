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

from pyTorch import Agent

    
agent = Agent(gamma=0.99, epsilon=1.0, batch_size=64, n_actions=4, eps_end=0.01, input_dims=[15], lr=0.001)
    
verzögern = False
spielfeldgöße = [15,15] #Breite dann Höhe
training_games = 3000
askToLoad = False
saveTrainingData = False
plotStats = True
plotInervall = 50

initObject = InitObject(verzögern, spielfeldgöße, training_games, askToLoad, saveTrainingData, plotStats, plotInervall)

stateDict = StateDict(initObject)
polititian = QPolicy(initObject) 
saveStuff = SaveStuff(initObject)  
saveStuff.initSaving(stateDict, polititian)

EatenApples = 0
TARGET_UPDATE = 10
targetCounter = 0

# for sttistics
statistics = Stats(initObject)
statistics.on_init()
eps_history = []

_exit = False
for i in tqdm(range(initObject.training_games)):
    
    _running = True
    
    snakeGame = App(initObject)    
    polititian.setEpsilon(i)
    EatenApples = 0
    appleDis = snakeGame.getAppleDis()

    while _running and not _exit:       
        #get current state
        observation = snakeGame.getState()

        #errechtne nächsten schritt
        action = agent.choose_action(observation)
        observation_ = snakeGame.getState()

        #führe ihn aus
        _running, EatenApples, _exit = snakeGame.on_execute(action)       
        
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
        agent.store_transition(observation, action, reward, observation_, not _running)
        if not (targetCounter % TARGET_UPDATE):
            agent.Q_target = agent.Q_eval
        
        agent.learn()
        targetCounter += 1

        eps_history.append(agent.epsilon)

        
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

   