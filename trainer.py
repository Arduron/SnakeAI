from snake_game import App
from tqdm import tqdm
from qAufsatz import StateDict
from policymaker import QPolicy
from os import path

import json

from matplotlib import pyplot 
    

training_games = 10

stateDict = StateDict()
polititian = QPolicy()
baseName = 'TrainedModels/trainedState'

load = input('Load existing model? (y/n) ')

if load == 'y':
    train = input('Continue training? (y/n) ')
    if train == 'n':
        polititian.epsilonstart = 0
    
    #ask for model number to load 
    modelNr = input('Model number = ')
    filename = baseName + modelNr + '.json'

    #import training data isf existant 
    if path.exists(filename):
        with open(filename, 'r') as fp:
            stateDict.stateHash = json.load(fp)

#create new filename
modelNr = 1
filename = baseName + str(modelNr) + '.json'
while path.exists(filename):
    modelNr = int(modelNr) + 1
    filename = baseName + str(modelNr) + '.json'
    

steps = []
_exit = False


for i in tqdm(range(training_games)):
    
    _running = True
    
    snakeGame = App()
    snakeGame.on_startup()
    polititian.setEpsilon(i)
    steps.append(0)
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
        steps[i] = _running[1]
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

    if _exit:
        training_games = i + 1
        break 
    
# save traiined state in s json file 
with open(filename, 'w') as fp:
    json.dump(stateDict.stateHash, fp, indent=4)
    
pyplot.plot(range(training_games), steps) 
pyplot.show()






