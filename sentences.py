from dictionary import *
import logging
import itertools

theOrgStringHash = {}



# Returns if the base word + remaining letters can form a possible word.
def isSentenceAllowedEx(originalStringLength, input, startIndex, length, args):
    #return True

    aS = ""
    bS = ""
    for iW in range(0, startIndex):
        aS = aS + str(input[iW])

    if isSentenceAllowed(originalStringLength, aS, args):
        return True

    bS = aS
    for iW in range(startIndex, length):
        bS = aS + str(input[iW])

        if isSentenceAllowed(originalStringLength, bS, args):
            return True

    return False
# ----------------------------------------------------

# If you pass the word, it'll tell you if this word can be used in the current sentence
def isSentenceAllowed(originalStringLength, sentence, args):
    global theOrgStringHash

    sNew = sentence.replace(" ", "")
    if len(sNew) > originalStringLength:
        return False

    theNewHash = {}

    for l in sentence:
        if(str(l) == " "):
            continue

        lCount = theNewHash.get(str(l))
        if lCount is None:
            theNewHash[str(l)] = 1
        else:
            theNewHash[str(l)] = lCount + 1

    for l in theOrgStringHash:
        if(str(l) == " "):
            continue

        lCount = theNewHash.get(str(l))
        if lCount is None:
            return False
        else:
            r = theOrgStringHash.get(str(l))
            if r != lCount:
                return False

    return True
# ----------------------------------------------------


# Reset
def calculateOriginalSentenceHash(orgString):
    global theOrgStringHash

    theOrgStringHash = {}
    for l in orgString:
        lCount = theOrgStringHash.get(str(l))
        if lCount is None:
            theOrgStringHash[str(l)] = 1;
        else:
            theOrgStringHash[str(l)] = lCount + 1
# ----------------------------------------------------


# Takes all the words and tries to form sentences.
def logSentences(s, args):
    logging.info("Logging all sentences:")
    for ss in s:
        logging.info(" ** " + str(ss))
        for sss in s[ss]:
            logging.info("       " + str(sss));
    logging.info(" --------- ")
# ----------------------------------------------------

# Takes all the words and tries to form sentences.
def formSentences(orgString, theWords, args):
    allWords = []

    calculateOriginalSentenceHash(orgString)

    outer = len(theWords) - 1
    while outer > 0:
        for inner in theWords[str(outer)]:
            allWords.append(inner)

        outer = outer - 1

    # for L in range(0, len(allWords) + 1):
    #     for subset in itertools.combinations(allWords, L):
    #         n_s = ""
    #         # for s in subset:
    #         #     n_s = n_s + s + " "
    #         # if isSentenceAllowed(len(orgString), n_s, args):
    #         #     print(n_s)

    # for subset in itertools.combinations(allWords, 4):
    #     n_s = ""
    #     for s in subset:
    #         n_s = n_s + s + " "
    #     if isSentenceAllowed(len(orgString), n_s, args):
    #         print(n_s)

    allSentences = formSentencesInternal2(orgString, allWords, args)
    logSentences(allSentences, args)

    return
# ----------------------------------------------------

def formSentencesInternal2(orgString, allWords, args):
    allSentences = {}
    slen = len(allWords)

    counts = args.wordCount.split(',')
    if len(counts) <= 0:
        logging.error("Invalid word count to form sentences. Exiting....")
        exit(-55)

    for ii in counts:
        iLen = int(ii)
        ss = []
        r1 = math.factorial(slen) / math.factorial(slen - iLen)
        # logging.info("No. of combinations: Total length = %d, Current length = %d, Total = %d" % (slen, iLen, r1))

        for subset in itertools.combinations(allWords, iLen):
            n_s = ""
            for s in subset:
                n_s = n_s + s + " "
            if isSentenceAllowed(len(orgString), n_s, args):
                ss.append(n_s)

        allSentences[str(ii)] = ss

    return allSentences
# ----------------------------------------------------




def formSentencesInternal(orgString, allWords, args):
    allSentences = {}
    slen = len(allWords)

    counts = args.wordCount.split(',')
    if len(counts) <= 0:
        logging.error("Invalid word count to form sentences. Exiting....")
        exit(-55)

    for ii in counts:
        iLen = int(ii)

        r1 = math.factorial(slen) / math.factorial(slen - iLen)
        #logging.info("No. of combinations: Total length = %d, Current length = %d, Total = %d" % (slen, iLen, r1))

        allSentences[str(iLen)] = getSentencesCombination(orgString, allWords, slen, iLen, args)

    return allSentences
# ----------------------------------------------------

# Driver function to generate the strings...
def getSentencesCombination(orgString, allWords, n, r, args):
    ret_data = []   # return value
    in_str = []

    for i in allWords:
        in_str.append(i)

    ret_data = permuteForSentences(len(orgString), ret_data, in_str, n, 0, r, 0, args)

    return ret_data
# ----------------------------------------------------

# Function to print permutations of string
    # saved_words --> the saved words array
    # in_str[] - --> Input Array
    # n      ---> Size of 'in_str' array
    # l --> Starting index of the string
    # r - --> Size of a combination to be fetched
    # depth ---> Current recursion depth
def permuteForSentences(originalStringLength, saved_sentences, in_str, n, l, r, depth, args):
    logging.debug("DEBUG: depth = %d, a = %s, l = %d, r = %d," % (depth, in_str, l, r))

    if (l == r):
        n_sentence = ""
        for i in range(0, l):
            n_sentence = n_sentence + str(in_str[i]) + " "

        if isSentenceAllowed(originalStringLength, n_sentence, args):
            saved_sentences.append(n_sentence)
        else:
            #print("Not a proper sentence: " + str(n_sentence))
            pass
    else:
        for i in range(l, n):
            # swap
            # printf("DEBUG: swapping l = %d, i = %d\n", l, i);
            tmp = in_str[l]
            in_str[l] = in_str[i]
            in_str[i] = tmp

            if isSentenceAllowedEx(originalStringLength, in_str, l+1, n, args):
                saved_sentences = permuteForSentences(originalStringLength, saved_sentences, in_str, n, l+1, r, depth+1, args)
            else:
                if args.verbose:  # purely for debugging purpose...
                    #logging.info("DEBUG: Cannot form meaningful sentence: (Start Index = %d, of string {%s}) -- %s - %s" % (l+1, str(in_str), str(in_str[:(l+1)]), str(in_str[(l+1):])))
                    isSentenceAllowedEx(in_str, l+1, n, args)

            # backtrack
	        # printf("DEBUG: swapping l = %d, i = %d\n", l, i);
            tmp = in_str[l]
            in_str[l] = in_str[i]
            in_str[i] = tmp

    return saved_sentences
# ----------------------------------------------------
