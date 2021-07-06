import time
from datetime import timedelta
import platform, os, sys, subprocess
import argparse
from dictionary import *
from sentences import *
from io import StringIO
import logging
import os.path
import json


# 1. Script Inputs
parser = argparse.ArgumentParser(
    description='Script to generate anagrams from a given string.')

parser.add_argument('--string', type=str, help='The original string, from which anagram is formed.')
parser.add_argument('--verbose', action='store_true', help='[Optional] The verbose log flag... to debug issues.')
parser.add_argument('--dict', type=str, default="brown", help='[Optional] The dictionary to use. One of wordnet_syn, words, brown')
parser.add_argument('--wordCount', type=str, default="4,5", help='[Optional] The number of words to use in a sentence.')
parser.add_argument('--outFile', type=str, help='[Optional] The path where the output file is written.')
parser.add_argument('--timeout', type=int, default="20", help='[Optional] Stop processing after these many seconds.')
parser.add_argument('--sessionId', type=str, default="unknown", help='[Optional] Session ID for this query.')
#parser.add_argument('-h', '--help', help='[Optional] Show options and exit', required=False)


# 2. Parse the arguments
args = parser.parse_args()

if(args.verbose):
    print("Verbose logging chosen")
    logging.basicConfig(level=logging.DEBUG)
else:
    print("Basic logging chosen")
    logging.basicConfig(level=logging.INFO)

args.combinations = {};
addedWords = {}


def areWeOutOfTime(arg_):
    end = time.time() - arg_.opStartedTime
    end = timedelta(seconds=end)
    if(end >= arg_.stopAfterTheseManySeconds):
        arg_.outOfTime = True
        return True

    return False 

# Takes the input string and removes special characters and spaces
def prepareString(in_str):
    ret_str = ""

    for i in in_str:
        i = ord(i)
        if(i >= ord('A') and i <= ord('Z')):
            i = ord('a') + (i - ord('A'))
            i = chr(i)
            ret_str = ret_str + str(i)
            continue

        if (i >= ord('a') and i <= ord('z')):
            i = chr(i)
            ret_str = ret_str + str(i)
            continue

    return ret_str


def formWords(in_str, args):
    start = time.time()
    all_words = { }
    slen = len(in_str)
    iLen = 0
    jStats = {}
    while(iLen < slen):
        sInner = time.time();        

        iLen += 1
        r1 = math.factorial(slen) / math.factorial(slen - iLen)
        logging.info("No. of combinations: Total length = %d, Current length = %d, Total = %d" % (slen, iLen, r1))

        args.combinations[str(iLen)] = int(round(r1))
        all_words[str(iLen)] = getWordsCombination(in_str, slen, iLen)

        eInner = time.time() - sInner
        eInner = str(timedelta(seconds=eInner))
        logging.info("Total time taken to form words with (r=%d, n=%d) = %s (H:M:S.Millis)" % (iLen, slen, eInner))
        jStats[iLen] = { "timeSpent": eInner }
        #args.fileOutput.write("Total time taken to form words with (r=%d, n=%d) = %s (H:M:S.Millis)\n" % (iLen, slen, eInner))

        if(areWeOutOfTime(args)):
            break

    elapsed = time.time() - start
    elapsed = str(timedelta(seconds=elapsed))
    logging.info("Total time taken to form words = %s (H:M:S.Millis)" % (elapsed))
    #args.fileOutput.write("Total time taken to form words = %s (H:M:S.Millis)\n" % (elapsed))

    args.logJsonToFileStats["words"] = { "timeFormat": "(H:M:S.Millis)", "n": slen, "totalTime": elapsed, "data" : jStats }

    return all_words


# Function to print permutations of string
    # saved_words --> the saved words array
    # in_str[] - --> Input Array
    # n      ---> Size of 'in_str' array
    # l --> Starting index of the string
    # r - --> Size of a combination to be fetched
    # depth ---> Current recursion depth
def permute(saved_words, in_str, n, l, r, depth):
    global addedWords
    logging.debug("DEBUG: depth = %d, a = %s, l = %d, r = %d," % (depth, in_str, l, r))

    if(areWeOutOfTime(args)):
        return saved_words

    if (l == r):
        n_word = ""
        boolValid = False;
        for i in range(0, l):
            n_word = n_word + str(in_str[i])

        if doesWordExistInDictionary_SynSet(n_word, args):
            boolValid = True;

        # if not wordnet.synsets(n_word):
        #     print("synsets: Not an English word: " + str(n_word))
        # else:
        #     print("synsets:    ---  Found an English word: " + str(n_word))
        #     boolValid = True;
        #
        # if not (n_word in setofwords):
        #     print("Not an English word: " + str(n_word))
        # else:
        #     print(" ---  Found an English word: " + str(n_word))

        if(boolValid):
            if addedWords.get(n_word) is None:
                # logging.info("Adding word " + str(n_word) + " to dictionary.")
                saved_words.append(n_word)
                addedWords[n_word] = 1
    else:
        for i in range(l, n):
            # swap
            # printf("DEBUG: swapping l = %d, i = %d\n", l, i);
            tmp = in_str[l]
            in_str[l] = in_str[i]
            in_str[i] = tmp

            # Purely for debugging...
            #if (str(in_str[0]) == "b") & (str(in_str[1]) == "l") & (str(in_str[2]) == "i") & (str(in_str[3]) == "d") & (str(in_str[4]) == "a"):
            #    print("debug string found found")
            #    dbgS = str(in_str[:5])

            if canFormMeaningfulWord(in_str, l+1, n):
                saved_words = permute(saved_words, in_str, n, l+1, r, depth+1)
            else:
                if args.verbose:  # purely for debugging purpose...
                    logging.info("DEBUG: Cannot form meaningful word: (Start Index = %d, of string {%s}) -- %s - %s" % (l+1, str(in_str), str(in_str[:(l+1)]), str(in_str[(l+1):])))
                    canFormMeaningfulWord(in_str, l + 1, n)

            # backtrack
	        # printf("DEBUG: swapping l = %d, i = %d\n", l, i);
            tmp = in_str[l]
            in_str[l] = in_str[i]
            in_str[i] = tmp

    return saved_words


# Driver function to generate the strings...
def getWordsCombination(in_string, n, r):
    ret_data = []   # return value
    in_str = []

    for i in in_string:
        in_str.append(i)

    ret_data = permute(ret_data, in_str, n, 0, r, 0)

    return ret_data
# ----------------------------------------------------

def logToFile(fileToWriteTo, origString, alteredString, allWords, sentences):
    if (None != origString):
        fileToWriteTo.write("---- Original String: " + origString + ", Length = " + str(len(origString)) + "\n")
    if (None != alteredString):
        fileToWriteTo.write("---- Processed String: " + alteredString + ", Length = " + str(len(alteredString)) + "\n")
        fileToWriteTo.write("---- Which Dictionary?: " + getCurrentDictionary() + "\n")

    if(None != allWords):
        fileToWriteTo.write("---- Total number of words: " + str(len(allWords)) + "\n")
        lW = -1
        for w in allWords:
            if lW != len(w):
                lW = len(w)
                fileToWriteTo.write("---- Words with length: " + str(lW) + "\n")
            fileToWriteTo.write(w + "\n")
        fileToWriteTo.write("---- All Words written" + "\n")

    if (None != sentences):
        fileToWriteTo.write("---- Total number of sentence groups: " + str(len(sentences)) + "\n")
        for ss in sentences:
            fileToWriteTo.write("---- Total number of sentences in this group: " + str(len(sentences[ss])) + "\n")
            for s in sentences[ss]:
                fileToWriteTo.write(s + "\n")

        fileToWriteTo.write("---- All sentences written" + "\n")
    # ----------------------------------------------------


def logToFileEx(jsonObject, origString, alteredString, allWords, sentences):
    incJ = { }
    if (None != origString):
        incJ = { "string" : origString, "length" : len(origString) }
    if (None != alteredString):
        inc = { "string" : alteredString, "length" : len(alteredString) }

        jsonObject["input"] = { 
            "session": args.sessionId,
            "dictionary" : getCurrentDictionary(), 
            "incoming" : incJ, 
            "altered" : inc, 
            "maxTimeAllowedToRun": args.stopAfter }

    if(None != allWords):
        wordJ = { "total" : len(allWords), "outOfTime": args.outOfTime }
        iLm = -1
        wordList = []
        currentWords = []
        for w in allWords:
            if iLm != len(w):
                if len(currentWords) > 0:
                    wordList.append({ iLm : { "count": len(currentWords), "words" : currentWords } })
                    currentWords = []

            currentWords.append(w)
            iLm = len(w)

        if len(currentWords) > 0:
            wordList.append({ iLm : { "count": len(currentWords), "words" : currentWords } })
            currentWords = []

        wordJ["listing"] = wordList
        jsonObject["words"] = wordJ


    if (None != sentences):
        sentJ = []
        currentS = []
        for ss in sentences:
            for s in sentences[ss]:
                currentS.append(s)

            sentJ.append({ len(sentences[ss]) : currentS })
            currentS = []

        jsonObject["sentences"] = { "total": len(sentences), "outOfTime": args.outOfTimeSentences, "listing" : sentJ }
    # ----------------------------------------------------



    # ----------------------------------------------------
#genCombinationsEx3(5, 3);


args.opStartedTime = time.time()
args.stopAfter = args.timeout
if(args.stopAfter > 30):
    args.stopAfter = 30
args.stopAfterTheseManySeconds = timedelta(seconds=args.stopAfter)
logging.info("Max time allowed to run = " + str(args.stopAfterTheseManySeconds) + " seconds.")
args.outOfTime = False
args.outOfTimeSentences = False

initDictionary(args);
prepareWordList();

logging.info("Incoming string:" + str(args.string))
args.nstring = prepareString(args.string)
logging.info("Prepared string:" + str(args.nstring))

total_words_formed = 0
if args.outFile == None:
    args.fileOutputName = os.path.join("output", args.nstring + "_" + args.wordCount + "_" + getCurrentDictionary() + ".txt")
else:
    args.fileOutputName = args.outFile

logging.info("Out file for writing: " + args.fileOutputName)

args.fileOutput = open(args.fileOutputName, "w")
if None == args.fileOutput:
    logging.error("Failed to open file for writing: " + args.fileOutputName)

# Data to be written
logJsonToFile = { }
args.logJsonToFileStats = { }

#logToFile(args.fileOutput, args.string, args.nstring, None, None)
logToFileEx(logJsonToFile, args.string, args.nstring, None, None)

args.words = formWords(args.nstring, args)
logging.info("Words = " + str(args.words))
args.allWordsArray = flattenWords(args.words, args)

#logToFile(args.fileOutput, None, None, args.allWordsArray, None)
logToFileEx(logJsonToFile, None, None, args.allWordsArray, None)

args.sentences = genCombinationsEx4(args.nstring, len(args.nstring), args.allWordsArray, len(args.allWordsArray), args)
#logToFile(args.fileOutput, None, None, None, args.sentences)
logToFileEx(logJsonToFile, None, None, None, args.sentences)

logJsonToFile["stats"] = args.logJsonToFileStats
  
# Serializing json 
str_io_obj = StringIO()
json.dump(logJsonToFile, str_io_obj)
#json_object = json.dumps(logJsonToFile, indent = 4)
args.fileOutput.write(str_io_obj.getvalue())


#formSentences(args.nstring, args.words, args)