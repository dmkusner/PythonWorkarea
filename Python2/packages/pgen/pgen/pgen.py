#!/bin/env python2.7

import string
import random
import pandas as pd
from argparse import ArgumentParser


def random_lower():
    return random.choice(string.ascii_lowercase)
# end def

def random_upper():
    return random.choice(string.ascii_uppercase)
# end def

def random_vowel():
    return random.choice('aeiouy')
# end def

def random_digit():
    return random.choice(string.digits)
# end def

def random_special():
    return random.choice('!@#$%^&*()-=_+[]{}|')
# end def


func_dict = { '0': random_lower, '1': random_upper, '2': random_vowel, '3': random_digit, '4': random_special }

def generate_codes():
    code = func_dict[random.choice('01')]()
    code += func_dict[random.choice('2')]()
    code += func_dict[random.choice('0123')]()
    code += func_dict[random.choice('1')]()
    code += func_dict[random.choice('4')]()
    return code
# end def


def main():
    parser = ArgumentParser(description = "Generate password element tables")
    parser.add_argument('-s', '--seed', help="seed argument for random module")
    args = parser.parse_args()
    
    if args.seed:
        random.seed(args.seed)

    for _ in range(10):
        data = []
        for _ in range(16):
            data.append([generate_codes() for _ in range(10)])

        df = pd.DataFrame(data,index=list('0123456789ABCDEF'),columns=list('0123456789'))
        print("{}\n\n\n".format(df))

# end def


if __name__ == "__main__":
    main()
