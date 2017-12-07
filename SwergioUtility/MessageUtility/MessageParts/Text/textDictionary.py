from SwergioUtility.MessageUtility.MessageParts.Text.chars import Chars

from SwergioUtility.ExpertData.expertData import ExpertData

class TextDictionary():

    def  __init__(self, max_dictionary_size = 300, text_data = None,expert_data = None, dictionary_text_path = None):
        self.chars = Chars()
        self.max_dictionary_size = max_dictionary_size
        self.dictionary_text_path = dictionary_text_path
        if text_data is None:
            if expert_data is None:
                if self.dictionary_text_path is None:
                    exp = ExpertData()
                else:
                    exp = ExpertData(filePath = dictionary_text_path)
            else:
                exp = expert_data
            text_data = exp.MessagesAsText() 
        self.GenNgrams(text_data)
        

    def GenNgrams(self, text):
        full_dict = []
        full_dict_counter = []
        
        for txt in text:
            split = self.SplitText(txt)
            for s in split:
                l = len(s)
                for n in range(1,l+1):
                    for i in range(l-n+1):
                        ngram = s[i:i+n]
                        if ngram in full_dict:
                            i_x = full_dict.index(ngram)
                            full_dict_counter[i_x] += 1
                        else:
                            full_dict.append(ngram)
                            full_dict_counter.append(1)
        full_dict_merged = []
        for i in range(len(full_dict)):
            if len(full_dict[i]) > 1:
                full_dict_merged.append([full_dict[i],full_dict_counter[i]])
        def getKey(item):
            return item[1]

        sort_dict = sorted(full_dict_merged, key=getKey,reverse=True)
        
        
        char_dict = self.chars.chars
        char_dict_counter = [1 for i in char_dict]
        char_dict_merged = []
        for i,c_d in enumerate(char_dict):
            char_dict_merged.append([c_d,char_dict_counter[i]])

        full_dict = char_dict_merged + sort_dict

        self.full_dict = full_dict
        if len(full_dict) > self.max_dictionary_size:
            dict = full_dict[0:self.max_dictionary_size]
        else:
            dict = full_dict

        self.dictionary = [d[0] for d in dict]
        self.dictionary_size = len(self.dictionary)
    
        return self.dictionary 
        
    def SplitText(self, txt):
        split = []
        nt = ""
        for t in txt:
            if t in self.chars.spezial:
                if nt != "" :
                    split.append(nt)
                nt = ""
                split.append(t)
            else:
                nt = nt + t
        if nt != "":
            split.append(nt)
        return split

    def TextToIndex(self, txt,idx_shift = 0):
        idx = []
        split = self.SplitText(txt)
        for t in split:
            l = len(t)
            nexti = 0
            for i in range(l):
                if i < nexti:
                    continue
                for n in range(l-i,0,-1):
                    ngram = t[i:i+n]
                    if ngram in self.dictionary:
                        idx.append(self.dictionary.index(ngram)+idx_shift)
                        nexti = i + len(ngram)        
                        break
        return idx

    def IndexToText(self,idx,idx_shift = 0):
        txt = []
        for i in idx:
            txt.append(self.dictionary[i-idx_shift])
        return ''.join(txt)
        


