import math
import nltk
from nltk.corpus import wordnet
from nltk.corpus import words
from nltk.corpus import brown
import logging
import enchant


setofwords = set()
wordsHashSet = {}
MAX_WORD_LENGTH_FOR_HASH = 12
USE_WHICH_DICTIONARY = "brown"    # Possible values: wordnet_syn (synsets), words, brown, d1 (dwyl)


def getCurrentDictionary():
    return USE_WHICH_DICTIONARY
# ----------------------------------------------------

def initDictionary(args):
    global USE_WHICH_DICTIONARY
    global setofwords

    USE_WHICH_DICTIONARY = args.dict
    if USE_WHICH_DICTIONARY == "wordnet_syn":
        pass
    else:
        if (USE_WHICH_DICTIONARY == "words") | (USE_WHICH_DICTIONARY == "brown"):
            pass
        else:
            if (USE_WHICH_DICTIONARY == "d1"):
                with open('dict/d1_words_alpha.txt') as word_file:
                    setofwords = set(word_file.read().split())
# ----------------------------------------------------

# Processes the "theWord" and adds the range of characters into the hash map
def prepareWordHashList(theWord):
    global wordsHashSet

    retC = 0;
    wL = len(theWord)
    if wL > MAX_WORD_LENGTH_FOR_HASH:
        wL = MAX_WORD_LENGTH_FOR_HASH + 1

    n_word = ""
    start = 1
    for iW in range(0, start):
        n_word = n_word + str(theWord[iW])

    for iW in range(start, wL):
        n_word = n_word + str(theWord[iW])

        #n_word = str(n_word)
        nRet = wordsHashSet.get(n_word)
        if None == nRet:
            wordsHashSet[n_word] = 1;
        else:
            wordsHashSet[n_word] = (nRet + 1);
        retC = retC + 1

    return retC;
# ----------------------------------------------------

# Prepares the word list, basically preprocess it.
def prepareWordList_Words():
    global setofwords
    global setofwordsN

    if USE_WHICH_DICTIONARY == "words":
        setofwords = set(words.words())
    else:
        if USE_WHICH_DICTIONARY == "brown":
            setofwords = set(brown.words())
        else:
            if USE_WHICH_DICTIONARY == "d1":
                # We would have already initializewd set of words...
                pass
            else:
                logging.error("Invalid dictionary source... exiting...")
                exit(-45)

    wC = 0;
    wHashes = 0;
    for w in setofwords:
        w = w.lower()
        wC = wC + 1

        wHashes += prepareWordHashList(w);

    logging.info("Dictionary being used: " + USE_WHICH_DICTIONARY)
    logging.info("Set of words: count = " + str(wC))
    logging.info("Set of word hashes: count = " + str(wHashes))
# ----------------------------------------------------

# Prepares the word list, basically preprocess it.
def prepareWordList_SynSet():
    prepareWordList_Words()
# ----------------------------------------------------


# Prepares the word list, basically preprocess it.
def prepareWordList():
    if USE_WHICH_DICTIONARY == "wordnet_syn":
        return prepareWordList_SynSet()
    else:
        if (USE_WHICH_DICTIONARY == "words") | (USE_WHICH_DICTIONARY == "brown"):
            return prepareWordList_Words()
        else:
            if (USE_WHICH_DICTIONARY == "d1"):
                return prepareWordList_Words()

    logging.error("Invalid dictionary source... exiting...")
    exit(-32)
# ----------------------------------------------------


# Checks if the given word exists in dictionary.
def doesWordExistInDictionary_Words(theWord, args):
    if not (theWord in setofwords):
        if args.verbose:
            logging.debug("Not an English word: " + str(theWord))
    else:
        if args.verbose:
            logging.debug(" ---  Found an English word: " + str(theWord))
        return True

    return False
# ----------------------------------------------------


# Checks if the given word exists in dictionary.
def doesWordExistInDictionary_SynSet(theWord, args):
    if not wordnet.synsets(theWord):
        if args.verbose:
            logging.debug("synsets: Not an English word: " + str(theWord))
    else:
        if args.verbose:
            logging.debug("synsets:    ---  Found an English word: " + str(theWord))
        return True

    return False
# ----------------------------------------------------

# Checks if the given word exists in dictionary.
def doesWordExistInDictionary(theWord, args):
    if USE_WHICH_DICTIONARY == "wordnet_syn":
        return doesWordExistInDictionary_SynSet(theWord)
    else:
        if USE_WHICH_DICTIONARY == "words" | USE_WHICH_DICTIONARY == "brown":
            return doesWordExistInDictionary_Words(theWord)
        else:
            if USE_WHICH_DICTIONARY == "d1":
                return doesWordExistInDictionary_Words(theWord)

    logging.error("Invalid dictionary source... exiting...")
    exit(-32)
# ----------------------------------------------------

# Returns if the base word + remaining letters can form a possible word.
def canFormMeaningfulWord(word, startIndex, length):
    #return True

    aWord = ""
    bWord = ""
    for iW in range(0, startIndex):
        aWord = aWord + str(word[iW])

    if startIndex >= MAX_WORD_LENGTH_FOR_HASH:
        bWord = aWord[:MAX_WORD_LENGTH_FOR_HASH]
        # If the length of the incoming word is very large (> MAX_WORD_LENGTH_FOR_HASH), then
        # check to see if the base word (i.e. the length of the first MAX_WORD_LENGTH_FOR_HASH letters) is valid.
        # If it's not, then most likely you can't form a proper word.
        # Because of the very long word, we are adopting this strategy.
        if wordsHashSet.get(bWord) is None:
            return False

        # Else for large words, return TRUE...
        return True

    if wordsHashSet.get(aWord) is not None:
        return True

    for iW in range(startIndex, length):
        bWord = aWord + str(word[iW])

        nRet = wordsHashSet.get(bWord)
        if nRet is not None:
            return True

    return False
# ----------------------------------------------------