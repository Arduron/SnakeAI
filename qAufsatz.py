class StateDict:
    def __init__(self, initObjekt):
        self.stateHash = {str((0)):{"Up":1, "Down":1, "Right":1, "Left":1}}
        self.learningrate = initObjekt.learningrate
        self.diskontierung = initObjekt.diskontierung

    def addState(self,newState):
        if self.stateHash.get(newState) == None:
            newEntry ={newState: {"Up":0, "Down":0, "Right":0, "Left":0}}
            self.stateHash.update(newEntry)      

    def QUpdate(self, state, action, nextState, reward):
        stateQ = self.returnStateQ(state)
        nextStateQ = self.returnStateQ(nextState)
        maxQ = max(nextStateQ.values())
        self.stateHash[state][action] = stateQ[action] + self.learningrate * (reward + self.diskontierung * maxQ - stateQ[action])

    def returnStateQ(self, state):
        self.addState(state)
        return self.stateHash.get(state)
        


