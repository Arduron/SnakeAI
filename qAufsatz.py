from collections import deque
from settings import InitObject


class StateDict:
    def __init__(self, initObjekt):
        self.stateHash = {str((0)):{"Up":1, "Down":1, "Right":1, "Left":1}}
        self.learningrate = initObjekt.learningrate
        self.diskontierung = initObjekt.diskontierung
        self.initObject = initObjekt
        self.Qchange = deque([])
        self.sumQ = 0 

    def addState(self,newState):
        if self.stateHash.get(newState) == None:
            newEntry ={newState: {"Up":0, "Down":0, "Right":0, "Left":0}}
            self.stateHash.update(newEntry)      

    def QUpdate(self, state, action, nextState, reward):
        stateQ = self.returnStateQ(state)
        nextStateQ = self.returnStateQ(nextState)
        maxQ = max(nextStateQ.values())
        addQ = self.learningrate * (reward + self.diskontierung * maxQ - stateQ[action])
        self.stateHash[state][action] = stateQ[action] + addQ

        if len(self.Qchange) == self.initObject.meanQrange:
            self.Qchange.pop()
        self.Qchange.append(abs(addQ))

    def returnStateQ(self, state):
        self.addState(state)
        return self.stateHash.get(state)

    def getMeanQ(self):
        if len(self.Qchange) > 0:
            return sum(list(self.Qchange)) / len(self.Qchange)
        else:
            return 0
        


