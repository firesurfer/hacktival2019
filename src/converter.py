from pint import UnitRegistry
import math

ureg = UnitRegistry(system='mks')  # metric


class Converter:

    def __init__(self):

        self.money_conversion = {
            "dollar": 1,
            "euro": 1.12,
            "pound": 1.3
        }
        self.length_comp = [
            # (0.1 * ureg.millimeter, "length", "{:.2f} x the width human hair"),
            (878.36 * ureg.kilometer, "length", "{:.2f} x the distance Paris -> Berlin"),
            (384400 * ureg.kilometer, "length", "{:.2f} x the distance to the moon")
        ]
        self.money_comp = [
            (59039, "dollar", "{:.0f} x Ø US income", ),
            (20700000000, "nasa", "{:.2f} x the NASA budget", ),
            #(686074048000, "military", "{:.2f} x US military budget"),
            (19390000000000, "dollar", "{:.2f} x the US GDP")
        ]

        self.area_comp = {  # in m^2
            "soccer field": 7140,
            "table tennis": 4.1785
        }
        self.latest_measurement = None

    def number_beautifier(self,n):
        millnames = ['', ' thousand', ' million', ' billion', ' trillion']
        n = float(n)
        millidx = max(0, min(len(millnames) - 1,
                             int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

        return '{:.0f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])

    def what_to_show(self,input, europe = True):
        output = []
        if type(input) is tuple:
            if input[1] not in self.money_conversion:  # freakin people
                return []
            inputstring = self.number_beautifier(input[0]) + " " + input[1] + "s"
            output.append((inputstring, input[1]))
            dollarvalue = self.convert_currency(input[0], input[1], "dollar")
            if europe:
                converted = (self.convert_currency(input[0], input[1], "euro"), "euro")
            else:
                converted = (dollarvalue, "dollar")

            convertedstring = self.number_beautifier(converted[0]) + " " + converted[1] + "s"
            output.append((convertedstring, converted[1]))
            compstrings = self.relate_to(dollarvalue, self.money_comp)
            for comp in compstrings:
                output.append(comp)
        else:
            output.append((pretty_print_value(input), str(input.units)))
            converted = convert_uint(input, europe)
            if converted is not None:
                output.append((converted, "<dummy>"))

            compstrings = []
            ureg.default_system = 'mks'
            if input.to_base_units().units == "meter":
                compstrings = self.relate_to(input, self.length_comp)
            for comp in compstrings:
                output.append(comp)

        return output

    def convert_currency(self, value, source_currency, goal_currency):

        conv = self.money_conversion
        return (conv[source_currency] / conv[goal_currency]) * value

    def relate_to(self, value, comp_list): # expects value in Dollars
        comp_with_factors = list()
        for comp in comp_list:
            factor = value / comp[0]
            comp_with_factors.append((comp, factor))
        filtered_comp_with_factors = list(filter(lambda x: 0.01 <= x[1] <= 1000000, comp_with_factors))
        if len(filtered_comp_with_factors) > 2:
            filtered_comp_with_factors = [filtered_comp_with_factors[0], filtered_comp_with_factors[-1]]
        compstrings = []
        for element in filtered_comp_with_factors:
            showstring = element[0][2].format(element[1])
            icon = element[0][1]
            compstrings.append((showstring, icon))
        return compstrings


def convert_uint(value, europe):
    ureg.default_system = 'mks' if europe else 'imperial'

    # no conversion
    if value.units in (ureg.liter, ureg.degree, ureg.revolutions_per_minute):
        return None


    # default conversion
    output = value.to_base_units().to_compact()

    # custom conversions
    if value.units == ureg.horsepower:
        output = value.to(ureg.kilowatt)
    if value.units == ureg.force_pound * ureg.foot:
        output = value.to(ureg.newton * ureg.meter)
    if value.units == ureg.mile / ureg.gallon:
        output = (100 / value).to(ureg.l / ureg.kilometer)

    return pretty_print_value(output)


def pretty_print_value(value):
    num = int(value.magnitude) if int(value.magnitude) == value.magnitude else round(value.magnitude, 2)
    unit = pretty_print_unit(value)
    return f"{num} {unit}"

def pretty_print_unit(value):
    data = [
        (ureg.degree, "°"),
        (ureg.newton * ureg.meter, "Nm"),
        (ureg.revolutions_per_minute, "rpm"),
        (ureg.foot * ureg.force_pound, "lb-ft"),
        (ureg.liter, "l"),
        (ureg.horsepower, "hp"),
        (ureg.kilowatt, "kW"),
        (ureg.mile / ureg.gallon, "mpg"),
        (ureg.liter / ureg.kilometer, "l/100km"),
        (ureg.foot ** 2, "ft²"),
        (ureg.m ** 2, "m²"),
    ]
    for u, s in data:
        if value.units == u:
            return s
    return str(value.units)
