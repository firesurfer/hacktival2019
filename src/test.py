import pytest
from extractor import extract_inner, extract

from pint import UnitRegistry
ureg = UnitRegistry()


@pytest.mark.parametrize("input_str, expected", [
    ("  90 degree  ", 90 * ureg.degree),
    ("460 horsepower", 460 * ureg.horsepower),
    ("25 horsepower", 25 * ureg.horsepower),
    ("420 pound-feet", 420 * (ureg.pound * ureg.feet)),
    ("20 pound feet", 20 * (ureg.pound * ureg.foot)),
    ("4600 rpm", 4600 * ureg.revolution / ureg.minute),
    # ("7,000 rpm", 7000 * ureg.revolution / ureg.minute),
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
    ("fifty two billion dollar ", (52_000_000_000, "dollar")),
    ("38 billion dollar", (38_000_000_000, "dollar")),
    ("hundred and forty three billion dollars", (143_000_000_000, "dollar")),
    ("four billion dollars", (4_000_000_000, "dollar")),
])
def test_numbers(input_str, expected):
    res = extract_inner([input_str])
    print(res)
    assert len(res) == 1
    assert len(res[0]) == 1
    assert res[0][0] == expected


def test_second_line():
    # spanning
    assert extract_inner(["hello two", "hundred dollars for something"]) == [[(200, "dollar")], []]

    # second only
    assert extract_inner(["hello foo", "fifty dollars for something"]) == [[], [(50, "dollar")]]

"""
def test_full():

    # from youtube_transcript_api import YouTubeTranscriptApi
    # print(YouTubeTranscriptApi.get_transcript("7Rjm5Fn1Zcg"))

    sanders_captions = [{'text': 'mr. chairman thank you very much and', 'start': 0.089, 'duration': 4.621}, {'text': 'director Mulvaney thanks very much for', 'start': 2.36, 'duration': 3.82}, {'text': 'being with us this morning', 'start': 4.71, 'duration': 4.53}, {'text': 'and I would agree with the chairman at', 'start': 6.18, 'duration': 7.2}, {'text': 'one point we must restore faith with the', 'start': 9.24, 'duration': 5.869}, {'text': 'American people and their government', 'start': 13.38, 'duration': 4.59}, {'text': 'sadly this budget does exactly the', 'start': 15.109, 'duration': 5.83}, {'text': 'opposite the Trump budget that was', 'start': 17.97, 'duration': 5.13}, {'text': 'introduced this week constitutes a', 'start': 20.939, 'duration': 5.701}, {'text': 'massive transfer of wealth from working', 'start': 23.1, 'duration': 6.419}, {'text': 'families the elderly the children the', 'start': 26.64, 'duration': 4.799}, {'text': 'sick the poor the most vulnerable people', 'start': 29.519, 'duration': 6.06}, {'text': 'in our country to the top one percent it', 'start': 31.439, 'duration': 6.21}, {'text': 'follows in the footsteps of the Trump', 'start': 35.579, 'duration': 4.441}, {'text': 'Ryan health care bill which gives', 'start': 37.649, 'duration': 4.98}, {'text': 'massive tax breaks to the people on top', 'start': 40.02, 'duration': 6.12}, {'text': 'while throwing 23 million people off of', 'start': 42.629, 'duration': 5.971}, {'text': 'the health insurance they currently have', 'start': 46.14, 'duration': 5.16}, {'text': 'and dramatically raising premiums for', 'start': 48.6, 'duration': 6.209}, {'text': 'older workers this is a budget which', 'start': 51.3, 'duration': 5.64}, {'text': 'says that if you are the wealthiest', 'start': 54.809, 'duration': 5.581}, {'text': 'family in America the Walton family of', 'start': 56.94, 'duration': 8.63}, {'text': 'Walmart you can get up to a fifty two', 'start': 60.39, 'duration': 8.37}, {'text': 'billion dollar tax break through the', 'start': 65.57, 'duration': 5.799}, {'text': 'repeal of the estate tax let me repeat', 'start': 68.76, 'duration': 5.94}, {'text': 'that wealthiest family in America could', 'start': 71.369, 'duration': 6.991}, {'text': 'get up to a fifty two billion dollar tax', 'start': 74.7, 'duration': 7.05}, {'text': 'break but at the same time this budget', 'start': 78.36, 'duration': 5.61}, {'text': 'says that if you are a lower income', 'start': 81.75, 'duration': 5.28}, {'text': 'senior citizen you will not be able to', 'start': 83.97, 'duration': 6.6}, {'text': 'get one hot nutritious meal a day that', 'start': 87.03, 'duration': 5.549}, {'text': 'is currently provided to you by the', 'start': 90.57, 'duration': 5.189}, {'text': 'Meals on Wheels program this is a budget', 'start': 92.579, 'duration': 4.921}, {'text': 'that says that if you are the second', 'start': 95.759, 'duration': 4.141}, {'text': 'wealthiest family in America the Koch', 'start': 97.5, 'duration': 4.74}, {'text': 'brothers a family by the way that has', 'start': 99.9, 'duration': 4.53}, {'text': 'contributed hundreds and hundreds of', 'start': 102.24, 'duration': 4.86}, {'text': 'millions of dollars into the Republican', 'start': 104.43, 'duration': 6.06}, {'text': 'Party your family can get up to a 38', 'start': 107.1, 'duration': 6.42}, {'text': 'billion dollar tax break but at the same', 'start': 110.49, 'duration': 5.489}, {'text': 'time if you are a working-class young', 'start': 113.52, 'duration': 5.22}, {'text': 'person trying to figure out how you can', 'start': 115.979, 'duration': 6.541}, {'text': 'possibly go to college your dream of a', 'start': 118.74, 'duration': 6.449}, {'text': 'college education will disappear because', 'start': 122.52, 'duration': 4.62}, {'text': 'of a hundred and forty three billion', 'start': 125.189, 'duration': 4.91}, {'text': 'dollars in cuts the student financial', 'start': 127.14, 'duration': 6.209}, {'text': 'assistance programs this is a budget', 'start': 130.099, 'duration': 3.941}, {'text': 'which says', 'start': 133.349, 'duration': 2.431}, {'text': 'that if you are a member of the Trump', 'start': 134.04, 'duration': 6.179}, {'text': 'family you may receive a tax break of up', 'start': 135.78, 'duration': 7.2}, {'text': 'to four billion dollars but if you are a', 'start': 140.219, 'duration': 5.671}, {'text': 'child of a low-income family you could', 'start': 142.98, 'duration': 5.31}, {'text': 'well lose the health insurance you', 'start': 145.89, 'duration': 4.56}, {'text': "currently have through the Children's", 'start': 148.29, 'duration': 4.44}, {'text': 'Health Insurance Program and massive', 'start': 150.45, 'duration': 5.069}, {'text': 'cuts to Medicaid when Donald Trump', 'start': 152.73, 'duration': 4.649}, {'text': 'campaigned for president he told the', 'start': 155.519, 'duration': 4.11}, {'text': 'American people that he would be a', 'start': 157.379, 'duration': 4.5}, {'text': 'different type of Republican that he', 'start': 159.629, 'duration': 4.59}, {'text': 'would take on the political and economic', 'start': 161.879, 'duration': 4.5}, {'text': 'establishment that he would stand up for', 'start': 164.219, 'duration': 4.11}, {'text': 'working people that he understood the', 'start': 166.379, 'duration': 4.08}, {'text': 'pain that families all across this', 'start': 168.329, 'duration': 5.071}, {'text': 'country were feeling well sadly this', 'start': 170.459, 'duration': 6.691}, {'text': 'budget exposes all of that verbiage for', 'start': 173.4, 'duration': 6.929}, {'text': 'what it really was just cheap campaign', 'start': 177.15, 'duration': 5.82}, {'text': 'rhetoric that was some notes nothing', 'start': 180.329, 'duration': 4.891}, {'text': 'more than that at a time when the very', 'start': 182.97, 'duration': 4.139}, {'text': 'rich are already getting much richer', 'start': 185.22, 'duration': 3.54}, {'text': 'while the middle class continues to', 'start': 187.109, 'duration': 4.71}, {'text': 'shrink this is a budget of the', 'start': 188.76, 'duration': 5.67}, {'text': 'billionaire class by the billionaire', 'start': 191.819, 'duration': 6.0}, {'text': 'class and for the billionaire class this', 'start': 194.43, 'duration': 5.19}, {'text': 'is a budget which will make it harder', 'start': 197.819, 'duration': 3.621}, {'text': 'for our kids to get a decent education', 'start': 199.62, 'duration': 4.229}, {'text': 'harder for working families to get the', 'start': 201.44, 'duration': 4.629}, {'text': 'health care they desperately need harder', 'start': 203.849, 'duration': 4.621}, {'text': 'to protect our environment and harder', 'start': 206.069, 'duration': 3.931}, {'text': 'for the elderly to live out their', 'start': 208.47, 'duration': 4.71}, {'text': 'retirement years in dignity this is not', 'start': 210.0, 'duration': 5.069}, {'text': 'a budget that takes on the political', 'start': 213.18, 'duration': 4.86}, {'text': 'establishment this is a budget of the', 'start': 215.069, 'duration': 5.28}, {'text': 'political establishment this is the', 'start': 218.04, 'duration': 5.339}, {'text': 'Robin Hood principle in Reverse you take', 'start': 220.349, 'duration': 5.371}, {'text': 'from the poor and you give to the very', 'start': 223.379, 'duration': 5.161}, {'text': 'rich the reality is that the budget the', 'start': 225.72, 'duration': 5.099}, {'text': 'president Trump has proposed would break', 'start': 228.54, 'duration': 4.02}, {'text': 'virtually every promise he made to', 'start': 230.819, 'duration': 9.151}, {'text': 'working people of this country among', 'start': 232.56, 'duration': 10.079}, {'text': 'many other promises that it breaks is', 'start': 239.97, 'duration': 5.699}, {'text': 'not only massive cuts to Medicaid but', 'start': 242.639, 'duration': 5.791}, {'text': 'cuts to Social Security this budget', 'start': 245.669, 'duration': 4.47}, {'text': 'would make massive cuts to the Social', 'start': 248.43, 'duration': 3.989}, {'text': 'Security for people who have severe', 'start': 250.139, 'duration': 3.99}, {'text': 'disabilities children who have lost', 'start': 252.419, 'duration': 4.68}, {'text': 'their parents and the poor and direct', 'start': 254.129, 'duration': 4.561}, {'text': "them will Vandy please don't tell me", 'start': 257.099, 'duration': 3.931}, {'text': 'that Social Security disability', 'start': 258.69, 'duration': 4.8}, {'text': 'insurance program is not part of Social', 'start': 261.03, 'duration': 5.759}, {'text': "Security let's be clear Social Security", 'start': 263.49, 'duration': 4.44}, {'text': 'is not just the', 'start': 266.789, 'duration': 3.511}, {'text': 'Ament program it is insurance program', 'start': 267.93, 'duration': 4.44}, {'text': 'that protects millions of Americans who', 'start': 270.3, 'duration': 4.35}, {'text': 'become disabled to lose their parents at', 'start': 272.37, 'duration': 5.25}, {'text': 'a young age the chairman said we have', 'start': 274.65, 'duration': 4.26}, {'text': 'got to restore faith with the American', 'start': 277.62, 'duration': 4.169}, {'text': "people he's exactly right the way to do", 'start': 278.91, 'duration': 5.819}, {'text': 'that is to totally reject this budget', 'start': 281.789, 'duration': 5.1}, {'text': 'and create a budget that works for', 'start': 284.729, 'duration': 4.051}, {'text': 'working families in this country not', 'start': 286.889, 'duration': 4.171}, {'text': 'just the billionaire class Thank You mr.', 'start': 288.78, 'duration': 4.52}, {'text': 'chairman', 'start': 291.06, 'duration': 2.24}]

    for line in extract(sanders_captions):
        print(line)

    assert False
"""