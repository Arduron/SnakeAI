from snake_game import App
from tqdm import tqdm
from qAufsatz import StateDict
from policymaker import QPolicy
from os import path

import json

from matplotlib import pyplot 
    

training_games = 1000

stateDict = StateDict()
polititian = QPolicy()

ans = input('load existing Model? (y/n) ')

if ans == 'y':
    polititian.epsilon = 0
    #ask for model number to load 
    modelNr = input('Model number = ')
    filename = 'trainedState' + modelNr + '.json'
    #import training data isf existant 
    if path.exists(filename):
        with open(filename, 'r') as fp:
            stateDict.stateHash = json.load(fp)

#create new filename
modelNr = 1
filename = 'trainedState' + str(modelNr) + '.json'
while path.exists(filename):
    modelNr = int(modelNr) + 1
    filename = 'trainedState' + str(modelNr) + '.json'
    

steps = []


for i in tqdm(range(training_games)):
    
    _running = True
    
    snakeGame = App()
    snakeGame.on_startup()
    polititian.setEpsilon(i)
    steps.append(0)
    appleDis = snakeGame.getAppleDis()


    while _running:
        #get current state
        currentState = snakeGame.getState()

        #füge ihn zur liste
        stateDict.addState(currentState)

        #get Q values
        currentStateQ = stateDict.returnStateQ(currentState)

        #errechtne nächsten schritt
        nextAction = polititian.getAction(currentStateQ)

        #führe ihn aus
        _running = [0,0]
        _running = snakeGame.on_execute(nextAction)
        steps[i] = _running[1]
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
    
# save traiined state in s json file 
with open(filename, 'w') as fp:
    json.dump(stateDict.stateHash, fp, indent=4)
    
pyplot.plot(range(training_games), steps) 
pyplot.show()






