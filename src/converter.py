from pint import UnitRegistry
import math
from copy import deepcopy

ureg = UnitRegistry(system='mks')  # metric


class converter:

    def __init__(self):

        self.money_conversion = {
            "dollar": 1,
            "euro": 1.12,
            "pound": 1.3
        }
        self.length = [
            (0.1 * ureg.millimeter, "length", "{} * the width human hair"),
            (1 * ureg.millimeter, None, None),
            (1 * ureg.kilometer, None, None),
            (878.36 * ureg.kilometer, "length", "{} * the distance Paris -> Berlin"),
            (384400 * ureg.kilometer, "length", "{} * the distance to the moon")
        ]
        self.money = [
            (59039 * ureg.dollar, "dollar", "{} * the median annual US income", ),
            (20700000000 * ureg.dollar, "nasa", "{} * the NASA annual budget", ),
            (686074048000 * ureg.dollar, "military", "{} * the US military budget"),
            (19390000000000 * ureg.dollar, "dollar", "{} * the US GDP")
        ]

        #self.area = {  # in m^2
        #    "soccer field": 7140,
        #    "table tennis": 4.1785
        #}
        self.latest_measurement = None


    def what_to_show(self,input, europe = True):
        output = list()
        if type(input) is tuple:
            conversion = " ".join(map(str, input))
            output.append(tuple([conversion]))
            if (europe and input[1] == "euro") or (not europe and input[1] == "dollar"):
                # no conversion needed
                output.append(None)
            else:
                output_eur, output_dol = self.convert_currency(input, europe)
                output.append









    def convert(self, input, europe = True):
        if type(input) is tuple:
            return self.convert_currency(input, europe)
        else:
            return self.convert_unit(input, europe)

    def convert_currency(self, input, europe:bool):

        conv = self.money_conversion
        output_eur = (conv["euro"] / conv[input[1]]) * input[0]
        output_dol = (conv["dollar"] / conv[input[1]]) * input[0]
        if europe:
            return output_eur, self.relate_money(output_dol)
        else:
            return output_dol, self.relate_money(output_dol)


    def relate_money(self, input): # expects value in Dollars
        value = input[0]
        factors = list()
        for comp in self.money:
            factors.append((math.log10(value / comp[0]) - 1)**2)
        sortedfactors = deepcopy(factors)
        sortedfactors.sort()
        index1 = factors.index(sortedfactors[0])
        index2 = factors.index(sortedfactors[1])
        return self.money[index1], self.money[index2]




    def convert_unit(self, input, europe):
        output = input.to_base_units()  # system defined at top (mks -> metric)
        return output.to_compact()


def convert_uint(value, europe):
    ureg.default_system = 'mks' if europe else 'imperial'
    output = value.to_base_units()  # system defined at top (mks -> metric)
    return f"{output.to_compact():.2f}"