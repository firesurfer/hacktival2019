from word2number import w2n
from pint import UnitRegistry
from fractions import Fraction

ureg = UnitRegistry()
    
def extract(text):
    text = text.lower().replace("pound-feet", "pound feet").split()
    cooldown = 0
    final = []
    for index, element in enumerate(text):
        if cooldown > 1:
            cooldown -= 1
            continue
        candidate = str()
        cooldown = 0

        # search for sequence of "zahlwörtern"
        while doeswork(transform_to_digit, text[index+cooldown]):
            if cooldown == 0:
                candidate = text[index+cooldown]
            else:
                candidate += " " + text[index+cooldown]
            cooldown += 1

        # parse "zahlwörter" to float
        if doeswork(transform_to_digit, candidate):
            candidate = transform_to_digit(candidate)

        # if no "zahlwörter", try to read float
        if cooldown == 0:
            try:
                candidate = float(element.replace(",", ""))  # for supporting 7,000 for example
                cooldown += 1
                while doeswork(transform_to_digit, text[index+cooldown]):
                    #if cooldown == 1:
                    adding_element += " " + text[index+cooldown]
            #cooldown += 1
            except:
                continue

        # at this point, candidate contains the number part as a float

        metric = str()
        final_m = 0
        for i in range(3):
            if index+cooldown+i+1 > len(text):
                continue
            metric += " " + text[index+cooldown+i]
            if doeswork(ureg, metric):
                final_m = ureg(metric)
        try:
            final.append([candidate, index, final_m])
        except:
            pass
    return(final)


def doeswork(function, element):
    try:
        function(element)
        return True 
    except:
        return False 
    
def transform_to_digit(digit):
    nums = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,"nine":9, 'ten':10,'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15,'sixteen':16,'seventeen':17,'eighteen':18,'nineteen':19, 'twenty':20,'thirty':30,'forty':40,'fifty':50,'sixty':60,'seventy':70,'eighty':80,'ninety':90, 'hundred':100,'thousand':1000, 'million':1000000, 'billion': 1000000000}
    digit = digit.split()
    dezimal=10
    point=False
    first_run=True
    for element in digit:
        nope=0
        try:
            current = Fraction(element)
        except:
            nope+=1
        try:
            current = nums[element]
        except:
            nope+=1
        if element=='point':
            point=True
            if first_run:
                previous=0
                final=0
                first_run= False
            continue
        else:
            if nope==2:
                raise Exception('nope')
        
        if(first_run):
            previous = current
            final = current
            first_run=False
            continue
        if point:
            final = Fraction(final)
            final+=Fraction(current, dezimal)
            dezimal*=10
        else:
            if current>previous:
                final*=current
            else:
                final+=current
        previous=current
    return(float(final))
    
print(transform_to_digit("point three two one"))
        
            
            

    
