import pytest
from extractor import extract

from pint import UnitRegistry
ureg = UnitRegistry()


def my_function(input_str):
    return ureg(input_str)


@pytest.mark.parametrize("input_str, expected", [
    ("  90 degree  ", 90 * ureg.degree),
    ("460 horsepower", 460 * ureg.horsepower),
    ("25 horsepower", 25 * ureg.horsepower),
    ("420 pound-feet", 420 * (ureg.pound * ureg.feet)),
    ("20 pound feet", 20 * (ureg.pound * ureg.foot)),
    ("4600 rpm", 4600 * ureg.revolution / ureg.minute),
    ("7,000 rpm", 7000 * ureg.revolution / ureg.minute),
    ("5.0 liter", 5 * ureg.liter),
    ("5.0 liters", 5 * ureg.liter),
    ("five liter", 5 * ureg.liter),
    ("four point nine five one liters", 4.951 * ureg.liter),
    # ("5.0 three seven six liters", 5.0376),
    ("three hundred two cubic inches", 302 * ureg.inch**3),
    ("307 cubic inches", 307 * ureg.inch**3),
    ("four inches", 4 * ureg.inch),
    ("ninety two point two millimeters", 92.2 * ureg.millimeter),
    ("1 millimeter", 1 * ureg.millimeter),
    ("12 millimeters", 12 * ureg.millimeter),
    ("93 millimeters", 93 * ureg.millimeter),
    ("15 miles per gallon", 15 * ureg.mile / ureg.gallon),
    ("1 mile per gallon", 1 * ureg.mile / ureg.gallon),
])
def test_numbers(input_str, expected):
    res = extract(input_str)
    assert len(res) == 1
    assert res[0][0] * res[0][2] == expected
