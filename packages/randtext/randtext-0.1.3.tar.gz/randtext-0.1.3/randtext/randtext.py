#!/usr/bin/env python

"""
How to define the 'format' strig:

Combinable characters
    - nc: generate n number of lower case characters
    - nC: generate n number of upper case characters
    - ni: generate n number of integer characters between 0 and 9
    - n#: generate n number of special characters defined in the {} after the n
        Valid characters: ! @ # $ % & ? _ - / \ ( ) { } [ ] < > 
    
    For example: 
    if format = 8cC!@#$%()[],2i
    The generator would produce something: doW%eR@p76 
    This is because
    - The first 8 characters to be randomly picked from c (any lower case english alphabet),
      C (any upper case english alphabet), !, @, #, $, %, (, ), [, or ] characters. 
    - The last 2 characters are defined to be integers
    
Non-combinable characters
- npc: generate n number of characters arranged in a pronouncable order. All characters will be lowercase
- npC: generate n number of characters arranged in a pronouncable order. All characters will be uppercase
- npcC: generate n number of characters arranged in a pronouncable order. The characters will be randomly lower or uppercase
- ndc: randomly pick a dictionary word with n number of characters in it. All characters will be lowercase
- ndC: randomly pick a dictionary word with n number of characters in it. All characters will be uppercase
- ndcC: randomly pick a dictionary word with n number of characters in it. The characters will be randonly lower or uppercase

    For example
    if format = 1C#$&,6p,1-,6w,2i
    The generator would produce something like: $reghim-swirls41
    This is because the various pieces of the format are:
    - 1 charactor randomly selected from C (any upper case english alphabet), #, $, or & characters
    - 6 lowercase pronouncable characters
    - 1 - character (it will always resolve to only the - character)
    - A dictionary word with 6 characters
    - 2 integers
"""

import logging
import string
import random
import sys
import os
from pathlib import Path

logging.basicConfig(level=logging.ERROR)

# GLOBALS -----------------------------------------------------------------------------------------

# Need to do this in case the script is run from a symlink
ABS_DIR = os.path.dirname(str(Path(__file__).resolve()))
DICT_DIR = ABS_DIR + '/dictionary'
AVAILABLE_DICTIONARY_LENGTHS = [int(dict_name) for dict_name in os.listdir(DICT_DIR)]

# Characters for pronouncability. Adapted from http://www.blackwasp.co.uk/PronounceablePasswords.aspx
VOWELS = 'a,ai,au,e,ea,ee,i,ia,io,o,oa,oi,oo,ou,u'.split(',')
CONSONANTS = 'b,c,ch,cl,d,f,ff,g,gh,gl,j,k,l,ll,m,mn,n,p,ph,ps,r,rh,s,sc,sh,sk,st,t,th,v,w,x,y,z'.split(',')

# PRIVATE FUNCTIONS -------------------------------------------------------------------------------

def _split_generand(generand):
    try:
        if not generand[0].isdigit():
            logging.error('Skipping \'{}\'. First character for each generand in format must be a number.'.format(generand))
            return 0, ''
    except:
        logging.error('Format included an empty generand. Please ensure that you are not trying to use a \',\' character in your generand')
        return 0, ''

    # Get the multi digit count in the generand
    for i, char in enumerate(generand):
        if not char.isdigit():
            # Break out of the loop when the characters stop being digits
            break

    try:
        count = int(generand[0:i])
    except:
        # An exception will be raised if generand only had a single digit character in the generand
        logging.error('Skipping \'{}\'. Each generand needs atleast a count and a character option to generate from.'.format(generand))
        return 0, ''

    char_options = generand[i:]

    return count, char_options

def _set_case(text, case_type):
    if case_type == 'c':
        return text.lower()
    elif case_type == 'C':
        return text.upper()
    elif case_type == 'cC':
        new_text = ''
        for char in text.lower():
            # randomly change to upper case or not
            if random.randint(0,2):
                new_text = new_text + char
            else:
                new_text = new_text + char.upper()
        return new_text

def _generate_pronouncable(count, case_type='c'):
    prev_was_vowel = (random.randint(0,2) == 0)
    generated_str = ''

    while len(generated_str) < count:
        str_to_append = ''
        if prev_was_vowel:
            # this one will be a consonant
            str_to_append = random.choice(CONSONANTS)
        else:
            # this one will be a vowel
            str_to_append = random.choice(VOWELS)
        
        if (len(generated_str) + len(str_to_append)) > count:
            # The resulting string would be too long. Try again
            continue
        
        # Append the string
        generated_str = generated_str + str_to_append
        
        # Flip the boolean
        prev_was_vowel = not prev_was_vowel
  
    #return generated_str
    return _set_case(generated_str, case_type)

def _generate_dictionary(count, case_type='c'):
    if count in AVAILABLE_DICTIONARY_LENGTHS:
        # We can directly get a random word from the dictionary that matches the count
        dictionary_words = open('{}/{}'.format(DICT_DIR, count)).read().splitlines()
        return _set_case(random.choice(dictionary_words), case_type)
    else:
        # Can't find a dictionary word with the required length
        logging.error('Could not find a valid dictionary word with the required length of {}'.format(count))
        return ''
        

# PUBLIC FUNCTIONS --------------------------------------------------------------------------------

def generate(format):
    format = format.split(',')
    password = ''

    for generand in format:
        count, char_options = _split_generand(generand)
        if not count:
            continue
        
        # pronouncable characters
        if   char_options == 'pc':
            password = password + _generate_pronouncable(count, 'c')
        elif char_options == 'pC':
            password = password + _generate_pronouncable(count, 'C')
        elif char_options == 'pcC':
            password = password + _generate_pronouncable(count, 'cC')
        # dictionary characters
        elif char_options == 'dc':
            password = password + _generate_dictionary(count, 'c')
        elif char_options == 'dC':
            password = password + _generate_dictionary(count, 'C')
        elif char_options == 'dcC':
            password = password + _generate_dictionary(count, 'cC')
        # combinable characters
        else:
            for i in range(0,count):
                char_option = random.choice(char_options)
                if   char_option == 'c':
                    password = password + random.choice(string.ascii_lowercase)
                elif char_option == 'C':
                    password = password + random.choice(string.ascii_uppercase)
                elif char_option == 'i':
                    password = password + random.choice(string.digits)
                else:
                    password = password + char_option

    return password
