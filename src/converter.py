from pint import UnitRegistry
import math
from copy import deepcopy

ureg = UnitRegistry(system='mks')  # metric


class Converter:

    def __init__(self):

        self.money_conversion = {
            "dollar": 1,
            "euro": 1.12,
            "pound": 1.3
        }
        self.length = [
            (0.1 * ureg.millimeter, "length", "{:.2f} * the width human hair"),
            (878.36 * ureg.kilometer, "length", "{:.2f} * the distance Paris -> Berlin"),
            (384400 * ureg.kilometer, "length", "{:.2f} * the distance to the moon")
        ]
        self.money_comp = [
            (59039, "dollar", "{:.2f} * the median annual US income", ),
            (20700000000, "nasa", "{:.2f} * the NASA annual budget", ),
            (686074048000, "military", "{:.2f} * the US military budget"),
            (19390000000000, "dollar", "{:.2f} * the US GDP")
        ]

        #self.area = {  # in m^2
        #    "soccer field": 7140,
        #    "table tennis": 4.1785
        #}
        self.latest_measurement = None

    def number_beautifier(self,n):
        millnames = ['', ' Thousand', ' Million', ' Billion', ' Trillion']
        n = float(n)
        millidx = max(0, min(len(millnames) - 1,
                             int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

        return '{:.0f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])



    def what_to_show(self,input, europe = True):
        output = []
        if type(input) is tuple:
            if input[1] not in self.money_conversion:  # freakin people
                return []
            inputstring = self.number_beautifier(input[0]) + " " + input[1]
            output.append((inputstring, input[1]))
            dollarvalue = self.convert_currency(input[0], input[1], "dollar")
            if europe:
                converted = (self.convert_currency(input[0], input[1], "euro"), "euro")
            else:
                converted = (dollarvalue, "dollar")

            convertedstring = self.number_beautifier(converted[0]) + " " + converted[1]
            output.append((convertedstring, converted[1]))
            compstrings = self.relate_to(dollarvalue, self.money_comp)
            for comp in compstrings:
                output.append(comp)
        else:
            output.append((str(input), str(input.units)))
            converted = convert_uint(input, europe)
            output.append((converted, "<dummy>"))

            compstrings = []
            ureg.default_system = 'mks'
            if input.to_base_units().units == "meter":
                compstrings = self.relate_to(input, self.length)
            for comp in compstrings:
                output.append(comp)

        return output



    def convert_currency(self, value, source_currency, goal_currency):

        conv = self.money_conversion
        return (conv[goal_currency] / conv[source_currency]) * value

    def relate_to(self, value, comp_list): # expects value in Dollars
        comp_with_factors = list()
        for comp in comp_list:
            factor = value / comp[0]
            comp_with_factors.append((comp, factor))
        filtered_comp_with_factors = list(filter(lambda x: 0.01 <= x[1] <= 1000, comp_with_factors))
        if len(filtered_comp_with_factors) > 2:
            filtered_comp_with_factors = [filtered_comp_with_factors[0], filtered_comp_with_factors[-1]]
        compstrings = []
        for element in filtered_comp_with_factors:
            showstring = element[0][2].format(element[1])
            icon = element[0][1]
            compstrings.append((showstring, icon))
        return compstrings





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