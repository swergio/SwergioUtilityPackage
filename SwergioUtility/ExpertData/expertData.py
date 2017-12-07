import numpy as np
import csv
import os

class ExpertData():


    def __init__(self, communicationenviroment = None,filePath = "/usr/src/app/Expert.csv"):
        self._env = communicationenviroment
        self._start_idx = 0
        self._length = None
        self._batch_size = 5
        self.filePath = filePath
        
    def setMaxTextLentgh(self, MaxTextLentgh):
        self.maxTxtLength = MaxTextLentgh

    '''
    Load data from expert data CSV file. 
    Expected  CSV structure is:
    Header: ['O_Namespace', 'O_Type', 'O_Text', 'A_Namespace', 'A_Type', 'A_Text', 'A_DoAct', 'ComID', 'Step']
    data: ['QATrainer', 'QUESTION', 'What is zero minus four?', 'TinaBob', 'QUESTION', '0-4=?', '1']
    '''

    def loadData(self, filePath = None):
        if filePath is None:
            filePath = self.filePath
        else:
            self.filePath = filePath

        with open(filePath, 'r') as f:
            data = list(csv.reader(f,delimiter=';',quotechar='"'))
        l = []
        for i in range(1,len(data)):
            
            o_ns = data[i][0]
            a_ns = data[i][3]

            if o_ns in self._env._socketIONamespaces and a_ns in self._env._socketIONamespaces:

                o_chatDetail = [(k,v.index(o_ns)) for k,v in self._env._socketIONamespacesDict.items() if o_ns in v]
                o_cty = self._env.ChatType.ValueNameToIndex([o_chatDetail[0][0]])
                o_cnr = self._env.ChatNumber.ValueToIndex([self._env.ChatNumber.GetValueByIndex(o_chatDetail[0][1])])

                o_mty = self._env.MessageType.ValueNameToIndex([data[i][1]])
                o_mtx = self._env.MessageText.ValueToIndex([data[i][2].lower()])
                o_mtx = self._env.MessageText.PadIndex(o_mtx,self._env.LengthOfMessageText)
                o_mtx = np.reshape(o_mtx,(int(o_mtx.shape[0])*int(o_mtx.shape[1])))
                o_act = [1]
                observation = np.concatenate((o_cty,o_cnr,o_mty,o_mtx,o_act))

                a_chatDetail = [(k,v.index(a_ns)) for k,v in self._env._socketIONamespacesDict.items() if a_ns in v]
                a_cty = self._env.ChatType.ValueNameToIndex([a_chatDetail[0][0]])
                a_cnr = self._env.ChatNumber.ValueToIndex([self._env.ChatNumber.GetValueByIndex(a_chatDetail[0][1])])
                
                a_mty = self._env.MessageType.ValueNameToIndex([data[i][4]])
                a_mtx = self._env.MessageText.ValueToIndex([data[i][5].lower()])
                a_mtx = self._env.MessageText.PadIndex(a_mtx,self._env.LengthOfMessageText)
                a_mtx = np.reshape(a_mtx,(int(a_mtx.shape[0])*int(a_mtx.shape[1])))
                a_act = [int(data[i][6])]
                action = np.concatenate((a_cty,a_cnr,a_mty,a_mtx,a_act))

                tupComStep = ( int(data[i][7]),int(data[i][8]))
                ll = [observation,action,tupComStep]
                l.append(ll)

        def getKey(item):
            return item[2]
        
        l = sorted(l, key = getKey)
        dataF= []
        for i,ll in enumerate(l):
            comID = ll[2][0]
            step = ll[2][1]
            hist = []
            for lo in l:
                comIDo = lo[2][0]
                stepo = lo[2][1]
                if step > stepo and comID == comIDo:
                    hist.append(lo[0])
                    hist.append(lo[1]) 
            lastInternStep =  max([-1] + [d['StepIntern'] for d in dataF if d['ComID']  == comID ])
            #Append Observation:
            if hist != []:
                p = hist[-1:][0]
                h = np.asarray(hist[:-1], dtype=int)
            else:
                p = []
                h = np.asarray([[]], dtype=int)
            dataF.append({'Hist': h, 'Prior': p, 'Current':ll[0], 'CurrentType':'O', 'ComID':comID, 'StepExtern': step, 'StepIntern':lastInternStep+1})    
            dataF.append({'Hist':np.asarray(hist, dtype=int),'Prior':ll[0],'Current':ll[1] , 'CurrentType':'A', 'ComID':comID, 'StepExtern': step, 'StepIntern':lastInternStep+2}) 
            
        self.data = dataF
        self._length = len(self.data)
        self._idx = np.asarray(list(range(0,self._length)))
        self.shuffel()

    def UpdateSampleSettings(self,Levels = [], Exclude = True, Types = ['O','A'],SplitTestSize = 0):
        if Exclude:
            self._idx = np.asarray([i for i,d in enumerate(self.data) if d['StepIntern'] not in Levels and d['CurrentType'] in Types])
        else:
            self._idx = np.asarray([i for i,d in enumerate(self.data) if d['StepIntern'] in Levels and d['CurrentType'] in Types])
        self.shuffel()
        if SplitTestSize > 0:
            self.SplitOfTestData(SplitTestSize)

    def SplitOfTestData(self,size):
        self._idxTest = self._idx[:size]
        self._idx = self._idx[size:]

    def shuffel(self):
        np.random.shuffle(self._idx)

    def next_batch(self, batch_size):
        if batch_size is None:
            batch_size = self._batch_size
        if self._start_idx + batch_size > len(self._idx):
            self._start_idx = 0
            self.shuffel()
        end_idx = self._start_idx + batch_size
        idx_list_part = range(self._start_idx, end_idx)
        idx_list = self._idx[list(idx_list_part)]
        self._start_idx += batch_size
        o = []
        a = []
        h = []
        for i in list(idx_list):
            rd =  self.data[i]
            o.append(rd['Prior'])
            a.append(rd['Current'])
            h.append(rd['Hist'])
        return np.asarray(o), np.asarray(a), np.asarray(h)

    def get_testdata(self, batch_size):
        if batch_size is None:
            batch_size = self._batch_size

        if self._idxTest is None:
            self.SplitOfTestData(batch_size)

        if len(self._idxTest) > batch_size:
            end_idx = len(self._idxTest)
        else:
            end_idx = batch_size
        idx_list_part = range(end_idx)
        idx_list = self._idxTest[list(idx_list_part)]
       
        o = []
        a = []
        h = []
        for i in list(idx_list):
            rd =  self.data[i]
            o.append(rd['Prior'])
            a.append(rd['Current'])
            h.append(rd['Hist'])
        return np.asarray(o), np.asarray(a), np.asarray(h)

    def random_batch(self,batch_size):
        if batch_size is None:
            batch_size = self._batch_size

        idx_list = self._idx[np.random.choice(len(self._idx), batch_size)]
        o = []
        a = []
        h = []
        for i in list(idx_list):
            rd =  self.data[i]
            o.append(rd['Prior'])
            a.append(rd['Current'])
            h.append(rd['Hist'])
        return np.asarray(o), np.asarray(a), np.asarray(h)

    def MessagesAsText(self):
        if os.path.exists(self.filePath) != True:
            return []
        with open(self.filePath, 'r') as f:
            data = list(csv.reader(f,delimiter=';',quotechar='"'))
    
        l = []
        for i in range(1,len(data)): 
            o_mtx = data[i][2].lower()
            a_mtx = data[i][5].lower()
            l.append(o_mtx)
            l.append(a_mtx)

        self.maxTxtLength = max([len(t) for t in l])
        return l

    def GetmaxTxtLength(self):
        if self._idx is None:
            if os.path.exists(self.filePath) != True:
                return self.maxTxtLength
            with open(self.filePath, 'r') as f:
                data = list(csv.reader(f,delimiter=';',quotechar='"'))
    
            l = []
            for i in range(1,len(data)): 
                o_mtx = self._env.MessageText.ValueToIndex([data[i][2].lower()])[0]
                a_mtx = self._env.MessageText.ValueToIndex([data[i][5].lower()])[0]
                l.append(o_mtx)
                l.append(a_mtx)

            self.maxTxtLength = max([len(t) for t in l])
            return self.maxTxtLength
        else:
            l = []
            for i in list(self._idx):
                cur = self.data[i]['Current']
                _,_,_, mtx, _ = np.split(cur,np.cumsum(self._env.message_space), axis=0)[:-1]
                l.append(np.where(mtx == self._env.MessageText.values.ENDMESSAGE.value)[0][0] + 1 )
            self.maxTxtLength = max(l)
            return self.maxTxtLength


    

    