# randtext

This module can be used to generate random text in python. It can be used to generate text with
- Meaningless mishmash of characters
- Pronouncable mishmash of characters
- Random dictionary words

## Usage

Import the module in your project like this

```
from randtext import randtext
```

You only need to use the following method to generate random text. The `format` argument is a string containing the instructions for generating the random text. The structure of the `format` argument is discussed below.

```
randtext.generate(format)
```

## Format argument

The `format` argument is a comma separated list of instructions that will be used by randtext to generate the random text. 

The instruction must be a number followed by the operation type or a list of characters to randomly choose from. The number represents the number of characters that you want within that sequence. The other half of the instruction can be of two types
- **Combinable operations** - The following operations can be combined together to define the list of characters that randtext will randomly choose from to generate the text
    - `c` - All lowercase ascii alphabets
    - `C` - All uppercase ascii alphabets
    - `i` - All integers from 0-9
    - special characters - Any special character can be used based on your need other than `,` because it is used to delimit the instructions in the `format` argument. You can even use a space if you want.
- **Non combinable operations** - These operations can not be combined with other operations. If you do try to combine them with other operations then they will regarded as just another character in the list of characters to randomly generate meaningless text from
    - `pc` - Generate lowercase pronouncable text
    - `pC` - Generate uppercase pronouncable text
    - `pcC` - Generate pronouncable text with characters that are randomly lower or uppercase
    - `dc` - Generate lowercase dictionary text
    - `dC` - Generate uppercase dictionary text
    - `dcC` - Generate dictionary text with characters that are randomly lower or uppercase

## Examples

- Simple meaningless random text with 14 ascii lowercase and uppercase characters

    ```
    randtext.generate('14cC')

    # 5 sample outputs:
    # ZWUvhxquyeNlWh
    # SarqpCypLJrEWe
    # GhFLSmQWyMISaN
    # gdDcRzOthCqUpw
    # oGUbsyHHfcaNeB
    ```
- Start the text with 2 of `#$%&()[]{}<>` characters, then 2 numbers, then 1 random uppercase letter, then 5 intergers, or lowercase and uppercase letters

    ```
    randtext.generate('2#$%&()[]{}<>,2i,1C,5icC')

    # 5 sample outputs:
    # %>62F9134f
    # }%12FaLe5j
    # {{11H82R2i
    # [%73UOVuk3
    # %{01EG8rG6 
    ```
- Create 2 pronouncable (but still meaningless) words with 8 characters each and separated by a space. The first word must start with a random uppercase letter and the rest of the letters should be all lowercase. The second word must have random lowercase and uppercase characters.

    ```
    randtext.generate('1C,7pc,1 ,8pcC')

    # 5 sample outputs:
    # Ceaskeff aUcLavio
    # Dbaidirh eagHAusk
    # Uiayausk eENAUSTO
    # Zshaiweb aistEayA
    # Hiweegup NougUGhA
    ```
- Create 2 dictionary words with 10 characters each separated by a space

    ```
    randtext.generate('10dc,1 ,10dc')

    # 5 sample outputs:
    # courteous sumptuous
    # brimstone riverbank
    # memoranda embroider
    # stimulant promenade
    # proselyte conqueror
    ```

## Notes

- The dictionary uses words found [here](http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain) and I take no responsibility for the words output by the dictionary operation. 
    - Feel free to delete or add your own words from the files in the `dictionary` directory of your local cloned copy of the repo.
    - The name of each file in the `dictionary` directory is the same as the number of characters in each line of the file. The `organize_dictionary.py` script can be used to read a raw dictionary file with words of all lengths and create the numbered files required by randtext
    - The number of words with a given length in the dictionary used here is as follows:
        
        ```
        Length | # of words
        -------+------------
        2      | 26
        3      | 136
        4      | 783
        5      | 2207
        6      | 3210
        7      | 3910
        8      | 4126
        9      | 3708
        10     | 3151
        11     | 2021
        12     | 1140
        13     | 588
        14     | 288
        15     | 113
        16     | 44
        17     | 19
        18     | 8
        19     | 4
        21     | 2
        22     | 2
        23     | 1

        ```
