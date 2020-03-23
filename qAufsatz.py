from collections import deque
from settings import InitObject
from random import randint


class StateDict:
    def __init__(self, initObject):
        self.stateHash = {str((0)):{"Up":1, "Down":1, "Right":1, "Left":1}}
        self.learningrate = initObject.learningrate
        self.diskontierung = initObject.diskontierung
        self.initObject = initObject
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

class QPolicy:
    def __init__(self, initObject):
        self.epsilonDiscount = initObject.epsilonDiscount
        self.epsilonStart = initObject.epsilonStart

    def getAction(self, stateQ):
        maxKey = []
        maxQ = max(stateQ.values())
        if stateQ["Up"] == maxQ:
            maxKey.append("Up")
        if stateQ["Down"] == maxQ:
            maxKey.append("Down")
        if stateQ["Right"] == maxQ:
            maxKey.append("Right")
        if stateQ["Left"] == maxQ:
            maxKey.append("Left")
        maxChosen = maxKey[randint(0, len(maxKey)-1)]

        if randint(0,10000) > 10000 * self.epsilon:
            return maxChosen
        else:
           randKey = ["Up", "Down", "Right", "Left"]
           return random.choice(randKey)


    def setEpsilon(self, episodeNumber):
        self.epsilon = self.epsilonStart * self.epsilonDiscount ** episodeNumber        


