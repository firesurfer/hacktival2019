import numpy as np
import re
from word2number import w2n
from pint import UnitRegistry

ureg = UnitRegistry()

    
def extract(text):
    text = text.lower().split()
    cooldown = 0
    final= []
    for index, element in enumerate(text):
        if cooldown-1 > 0:
            cooldown += -1
            continue
        candidate = str()
        cooldown = 0
        while (doeswork(w2n.word_to_num, text[index+cooldown])):
            if cooldown == 0:
                candidate= text[index+cooldown]
            else:
                candidate+= " " + text[index+cooldown]
            cooldown+= 1
        if cooldown == 0:
            try:
                candidate = float(element)
                cooldown+=1
            except:
                continue
                pass
        if doeswork(w2n.word_to_num, candidate):
            candidate = w2n.word_to_num(candidate)
            
        metric = str()
        final_m = 0
        for i in range(3):
            if index+cooldown+i+1 > len(text):
                continue
            metric+= " " + text[index+cooldown+i]
            if (doeswork(ureg, metric)):
                final_m = metric
        try:
            final.append([candidate, index, final_m])
        except:
            pass
    return(final)

def doeswork( function, element):
    try:
        function(element)
        return True 
    except:
        return False 
        
        
    



if __name__ =='__main__':

    #f = open("first_test.txt", "r")
    #text = f.read()
    #print(extract(text))
    tmp = "This is an string example. It includes 2.6 words. 3 years to go. One billion inches this shit."
    print(extract(tmp))
