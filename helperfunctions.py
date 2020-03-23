from os import path
import json

from settings import InitObject
from statistics import Stats
from qAufsatz import StateDict

class SaveStuff:
    def __init__(self, initObject):
        self.initObject = initObject
        self.baseName = initObject.baseName
        self.filename = ''

    def initSaving(self, stateDict, polititian):
        if self.initObject.askToLoad:
            load = input('Load existing model? (y/n) ')
            if load == 'y':
                train = input('Continue training? (y/n) ')
                if train == 'n':
                    polititian.epsilonStart = 0
                
                #ask for model number to load 
                modelNr = input('Model number = ')
                self.filename = self.baseName + modelNr + '.json'

                #import training data isf existant 
                if path.exists(self.filename):
                    with open(self.filename, 'r') as fp:
                        stateDict.stateHash = json.load(fp)['StateModel']

        #create new self.filename
        modelNr = 1
        self.filename = self.baseName + str(modelNr) + '.json'
        while path.exists(self.filename):
            modelNr = int(modelNr) + 1
            self.filename = self.baseName + str(modelNr) + '.json'
    
    def saveIt(self, stateHash, statisticsHash):
        # save traiined state in s json file 
        saveHash = {'Stats': statisticsHash,'StateModel': stateHash}
        with open(self.filename, 'w') as fp:
            json.dump(saveHash, fp, indent=4)