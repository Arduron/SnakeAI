

class SaveStuff:
    def __init__(initObject):
        self.initObject = initObject
        self.baseName = initObject.baseName

    def initSaving(self)
        if self.initObject.askToLoad:
            load = input('Load existing model? (y/n) ')
            if load == 'y':
                train = input('Continue training? (y/n) ')
                if train == 'n':
                    polititian.epsilon = 0
                
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