from os import path
import json
import torch

from settings import InitObject
from statistics import Stats
from qAufsatz import StateDict

class SaveStuff:
    def __init__(self, initObject):
        self.initObject = initObject
        self.baseName = initObject.baseName
        self.filename = ''

    def initSaving(self, agent, polititian):
        if self.initObject.askToLoad:
            load = input('Load existing model? (y/n) ')
            if load == 'y':
                train = input('Continue training? (y/n) ')
                if train == 'n':
                    agent.epsilon = agent.eps_min
                
                #ask for model number to load 
                modelNr = input('Model number = ')
                self.filename = self.baseName + modelNr + '.pt'

                #import training data isf existant 
                if path.exists(self.filename):
                    agent.Q_eval.load_state_dict(torch.load(self.filename))
                    agent.Q_eval.eval()    

        #create new self.filename
        modelNr = 1
        self.filename = self.baseName + str(modelNr) + '.pt'
        while path.exists(self.filename):
            modelNr = int(modelNr) + 1
            self.filename = self.baseName + str(modelNr) + '.pt'
    
    def saveIt(self, agent, statisticsHash):
        # save traiined state in s json file 
        saveHash = {'Stats': statisticsHash,'StateModel': agent.Q_eval.state_dict()}
        torch.save(agent.Q_eval.state_dict(), self.filename)