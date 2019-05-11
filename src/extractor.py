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
        while index+cooldown > len(text) and doeswork(transform_to_digit, text[index+cooldown]):
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
