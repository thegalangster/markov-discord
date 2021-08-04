"""Generate Markov text from text files."""

from random import choice
import sys
import string

combined_chains = {}

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    file_object = open(file_path)
    file_as_string = file_object.read()

    return file_as_string.replace("\n", " ").rstrip()


def make_chains(chains, text_string, key_length):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    value_list = ["text"]
    words = text_string.split()

    # iterate through each index in words until the length of index minus 2
    # (value at index, value at index + 1): append to list value at index + 2

    for index in range(0, len(words) - key_length):
        key = []
        for count in range(index, index + key_length):
            key.append(words[count])
        key = tuple(key)
        value = words[index + key_length]

        existing_value = chains.get(key, [])
        existing_value.append(value)
        chains[key] = existing_value

    return chains


def find_capitol_keys(chains):
    capitol_keys = []
    keys = chains.keys()
    for key in keys:
        if key[0][0] in string.ascii_uppercase:
            capitol_keys.append(key)
    return capitol_keys

def find_punc_end_keys(chains):
    punc_end_keys = set()
    values = chains.values()
    for value in values:
        for item in value:
            if item[-1] in string.punctuation:
                punc_end_keys.add(item)
    return punc_end_keys

def make_text(chains, key_length):
    """Return text from chains."""

    words = []

    #pick random key
    capitol_keys = find_capitol_keys(chains)
    selected_key = choice(capitol_keys)
    words.extend(selected_key)
    
    #pick random value from that key
    #loop until error
    while True:
        #from that key, pick random value
        if chains.get(selected_key) is not None:
            random_word = choice(chains[selected_key])
            words.append(random_word)
        else:
            return ' '.join(words)

        punc_end_keys = find_punc_end_keys(chains)
        if random_word in punc_end_keys:
            return ' '.join(words)

        #from the string that's created, pick the last two words - find that key in the dictionary
        new_key_position = 0 - key_length
        selected_key = words[new_key_position:]
        selected_key = tuple(selected_key)


length = input("What is the key length?\n > ")
length = int(length)

for index in range(1, len(sys.argv)):
    input_path = sys.argv[index]

    # Open the file and turn it into one long string
    input_text = open_and_read_file(input_path)
    # Get a Markov chain
    chains = make_chains(combined_chains, input_text, length)

# Produce random text
random_text = make_text(chains, length)

print(random_text)
