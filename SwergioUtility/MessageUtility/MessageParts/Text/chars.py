'''
Set of available characters
'''

class Chars():
    txt = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    number = ['1','2','3','4','5','6','7','8','9','0']
    spezial = ['+','"','*','%','&','/','(',')','=','?','[',']','{','}',',','.',';',':',' ','-','_','!']
    
    chars = txt + number + spezial
    def __init__(self):
        pass

    def Index(self,char):
        return self.chars.index(char)
    def Char(self,index):
        return self.chars[index]