import re
from num2words import num2words

def convert(input_string):
    numbers = re.findall(r'\d+', input_string)

    for number in numbers:
        word = num2words(int(number), lang="id")
        input_string = input_string.replace(number, word)
    
    return input_string
