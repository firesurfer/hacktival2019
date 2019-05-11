from word2number import w2n
from pint import UnitRegistry
from fractions import Fraction

ureg = UnitRegistry()

def extract(captions):
    strings = [t['text'] for t in captions]
    for cap, nums in zip(captions, extract_inner(strings)):
        cap['values'] = nums
    return captions


def extract_inner(strings):
    token_list = [s.lower().replace("pound-feet", "pound feet").split() for s in strings]
    text = sum(token_list, [])
    final = [[] for _ in range(len(strings))]
    idxs = []
    for idx, t in enumerate(token_list):
        for _ in range(len(t)):
            idxs.append(idx)
    cooldown = 0
    for index, element in enumerate(text):

        if cooldown > 1:
            cooldown -= 1
            continue
        candidate = str()
        cooldown = 0

        # search for sequence of "zahlwörtern"
        while index+cooldown < len(text) and doeswork(transform_to_digit, " ".join(text[index:index+cooldown+1])):
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

        if index+cooldown < len(text) and text[index+cooldown] in ("dollar", "dollars"):
            final[idxs[index]].append((candidate, "dollar"))
            cooldown += 1
            continue

        metric = str()
        final_m = 0
        for i in range(3):
            if index+cooldown+i+1 > len(text):
                continue
            metric += " " + text[index+cooldown+i]
            if doeswork(ureg, metric):
                final_m = ureg(metric)
        try:
            if final_m == 0:
                continue
            final[idxs[index]].append(candidate * final_m)
        except:
            pass
    return final


def doeswork(function, element):
    try:
        function(element)
        return True 
    except:
        return False

def transform_to_digit(digit):
    # print(digit)
    nums = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,"nine":9, 'ten':10,'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15,'sixteen':16,'seventeen':17,'eighteen':18,'nineteen':19, 'twenty':20,'thirty':30,'forty':40,'fifty':50,'sixty':60,'seventy':70,'eighty':80,'ninety':90, 'hundred':100,'thousand':1000, 'million':1000000, 'billion': 1000000000}
    nums_10 = [0,1,2,3,4,5,6,7,8,9]
    digit = [d for d in digit.split() if d != "and"]
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
            current = Fraction(nums[element])
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
            if current in nums_10:
                final+=Fraction(current, dezimal)
                dezimal*=10
            else:
                final*=current
        else:
            if current>previous:
                final*=current
            else:
                final+=current
        previous=current
    return(float(final))


