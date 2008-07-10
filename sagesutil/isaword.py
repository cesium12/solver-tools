from sagesutil import export

DICTIONARY_FILENAME=""
DICTIONARY=set()

@export(description = "Is the specified string listed as a word in the specified dictionary file?",
        args = ["The string to test", "The dictionary file to compare against"],
        ret = "Boolean; True if the word is in the dictionary, False otherwise")
def isaword(word, dict):
    """ Returns False iff word is not listed in dict """
    if DICTIONARY_FILENAME != dict:
        f = open(dict)
        DICTIONARY = set( [ x.strip() for x in f ] )

    return (word in DICTIONARY)
