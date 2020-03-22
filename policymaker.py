from random import randint
import random 

class QPolicy:
    def __init__(self, initObjekt):
        self.epsilonDiscount = initObjekt.epsilonDiscount
        self.epsilonStart = initObjekt.epsilonStart

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

        