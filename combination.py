import math
import logging
import time
from datetime import timedelta

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


def areWeOutOfTime(arg_):
    end = time.time() - arg_.opStartedTime
    end = timedelta(seconds=end)
    if(end >= arg_.stopAfterTheseManySeconds):
        arg_.outOfTimeSentences = True
        return True

    return False 
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

def howManyCombinations(n,r):
    return int(math.factorial(n)) / int(int((math.factorial(n - r))) * int((math.factorial(r))))

def genCombinations(n, r):
    retSet = []
    s = []
    for i in range(0, r):
        s.append(i)

    retSet.append(s[:r]);

    totalC = int(howManyCombinations(n, r))
    for i in range(1,totalC):
        m = r-1
        max_val = n-1

        while s[m] == max_val:
            # Find the rightmost element not at maximum value
            m = m - 1
            max_val = max_val - 1

        # Increment the above rightmost element
        s[r-1] = s[r-1] + 1


        # All others are the successors of this element
        for j in range(m+1, r):
            s[j] = s[j - 1] + 1

        retSet.append(s[:r]);

    return retSet


def genCombinationsEx(n, r):
    retSet = []
    s = []
    for i in range(0, r):
        s.append(i)

    retSet.append(s[:r]);

    first = 0
    last = r;
    n = n-1

    totalC = int(howManyCombinations(n, r))
    while s[first] != (n - r + 1):
        mt = last

        mt = mt - 1
        while s[mt] >= (n - (last - mt) + 1):
            mt = mt - 1
        s[mt] = s[mt] + 1

        mt = mt + 1
        while mt != last:
            s[mt] = s[(mt-1)] + 1;
            mt = mt + 1

        retSet.append(s[:r]);

    return retSet


def genCombinationsEx2(originalString, originalStringLength, allWords, n, r, args):
    retSet = []
    s = []

    calculateOriginalSentenceHash(originalString)

    for i in range(0, r):
        s.append(i)

    retSet.append(s[:r]);

    first = 0
    last = r;
    totalC = int(howManyCombinations(n, r))
    n = n - 1
    bCheckSkip = False
    bCheckSkip2 = False
    actualIters = 0

    while s[first] != (n - r + 1):
        actualIters = actualIters + 1
        mt = last

        mt = mt - 1
        while s[mt] >= (n - (last - mt) + 1):
            mt = mt - 1
            bCheckSkip = True

        s[mt] = s[mt] + 1

        if bCheckSkip:
            bCheckSkip = False
            while True:
                sl = 0
                for i in range(0, (mt+1)):
                    sl += len(allWords[s[i]])
                if sl > originalStringLength:
                    s[mt] = s[mt] + 1
                    if s[mt] >= (n-1):
                        break
                else:
                    break

        mt = mt + 1
        while mt != last:
            s[mt] = s[(mt-1)] + 1;
            if s[mt] >= n:
                s[mt] = n
            mt = mt + 1
            bCheckSkip2 = True

        if bCheckSkip2:
            bCheckSkip2 = False

        n_s = ""
        for i in range(0, r):
            n_s += allWords[s[i]] + " "
        if not isSentenceAllowed(originalStringLength, n_s, args):
            continue

        retSet.append(n_s);

    return retSet

# Takes all the words and tries to form sentences.
def logSentences(s, logAll, args):
    logging.info("Logging all sentences:")
    for ss in s:
        logging.info(" ** " + str(ss) + ", count = " + str(len(s[ss])))
        if logAll:
            for sss in s[ss]:
                logging.info("       " + str(sss));
    logging.info(" --------- ")
# ----------------------------------------------------

def getSentence(start, end, s, allWords, n, r):
    n_s = ""
    for iA in range(start, end):
        if(s[iA] >= n):
            n_s += " --OOR-- "
        else:
            n_s += allWords[s[iA]] + " "

    return n_s;

def getSentenceLength(start, end, s, allWords, n, r):
    n_l = 0
    for iA in range(start, end):
        if(s[iA] >= n):
            n_l += 9
        else:
            n_l += len(allWords[s[iA]])

    return n_l;

def combine(s, n, r, index, originalString, originalStringLength, allWords, args):
    retSet = []

    if(areWeOutOfTime(args)):
        return retSet

    if (index == (r - 1)) & (s[index] < n):
        #print("Found C (Index = %d): %s", (index, str(s)))
        #retSet.append(s[:r]);
        n_s = getSentence(0, r, s, allWords, n, r)
        if isSentenceAllowed(originalStringLength, n_s, args):
            retSet.append(n_s)
        else:
            #if (allWords[s[0]] == "harvests") & (allWords[s[1]] == "ham"):
            #    pass
            #print("(2) Invalid string at: index=" + str(index) + ", indices = " + str(s) + ", s = " + n_s)
            pass

    #print(("Combine called: (Index = %d): %s"), (index, str(s)))
    while True:
        args.combineIterator += 1

        if(areWeOutOfTime(args)):
            break

        if index < (r - 1):
            n_l = getSentenceLength(0, index+1, s, allWords, n, r)
            if n_l <= originalStringLength:
                ar = combine(s, n, r, index + 1, originalString, originalStringLength, allWords, args)
                retSet.extend(ar)
            else:
                #if (allWords[s[0]] == "harvests") & (allWords[s[1]] == "ham"):
                #    pass
                #print("Invalid string at: index=" + str(index) + ", indices = " + str(s) + ", s = " + n_s)
                pass

            s[index] = s[index] + 1

            if s[index] < n:
                for iA in range(index+1, r):
                    s[iA] = s[iA-1] + 1
            else:
                break;
        else:
            s[index] = s[index] + 1

            if s[index] >= n:
                break

            #print("Found C (Index = %d): %s", (index, str(s)))
            #retSet.append(s);
            n_s = getSentence(0, r, s, allWords, n, r)
            if isSentenceAllowed(originalStringLength, n_s, args):
                retSet.append(n_s);
            else:
                #if (allWords[s[0]] == "harvests") & (allWords[s[1]] == "ham"):
                #    pass
                #print("(3) Invalid string at: index=" + str(index) + ", indices = " + str(s) + ", s = " + n_s)
                pass

    return retSet
# ----------------------------------------------------

def genCombinationsEx4Internal(originalString, originalStringLength, allWords, n, r, args):
    retSet = []
    s = []

    for i in range(0, r):
        s.append(i)

    args.combineIterator = 1
    totalC = int(howManyCombinations(n, r))
    logging.info("No. of combinations: N = %d, R = %d, Total = %d." % (n, r, totalC))

    retSet = combine(s, n, r, 0, originalString, originalStringLength, allWords, args)

    logging.info("No. of combinations: N = %d, R = %d, Total = %d. Actual iterations done = %d" % (n, r, totalC, args.combineIterator))
    #args.fileOutput.write("No. of combinations: N = %d, R = %d, Total = %d. Actual iterations done = %d\n" % (n, r, totalC, args.combineIterator))

    args.logJsonToFileStats["nCr"] = { "N": n, "R": r, "nCr": totalC, "actual-nCr": args.combineIterator }

    return retSet
# ----------------------------------------------------

def genCombinationsEx4(originalString, originalStringLength, allWords, n, args):
    retSet = {}

    startT = time.time()

    calculateOriginalSentenceHash(originalString)

    counts = args.wordCount.split(',')
    if len(counts) <= 0:
        logging.error("Invalid word count to form sentences. Exiting....")
        exit(-55)

    jStats = {}
    for ii in counts:
        iLen = int(ii)
        if(iLen > n):
            break

        start = time.time()
        retSet[ii] = genCombinationsEx4Internal(originalString, originalStringLength, allWords, n, iLen, args)
        end = time.time()

        elapsed = end - start
        elapsed = str(timedelta(seconds=elapsed))
        logging.info("Total time taken to form sentences with (r=%d, n=%d) = %s (H:M:S.Millis)" % (iLen, n, elapsed))
        #args.fileOutput.write("(C.py) Total time taken to form sentences with (r=%d, n=%d) = %s (H:M:S.Millis)\n" % (iLen, n, elapsed))

        jStats[iLen] = { "timeSpent": elapsed }

        if(areWeOutOfTime(args)):
            break

    logSentences(retSet, False, args)

    endT = time.time()
    elapsed = endT - startT
    elapsed = str(timedelta(seconds=elapsed))
    args.logJsonToFileStats["sentences"] = { "timeFormat": "(H:M:S.Millis)", "n": n, "totalTime": elapsed, "data" : jStats }

    return retSet
# ----------------------------------------------------

def combineOrg(s, n, r, index):
    retSet = []

    if (index == (r - 1)) & (s[index] < n):
        print("Found C (Index = %d): %s", (index, str(s)))
        retSet.append(s[:r]);

    #print(("Combine called: (Index = %d): %s"), (index, str(s)))
    while True:
        if index < (r - 1):
            ar = combine(s, n, r, index + 1)
            retSet.append(ar)

            s[index] = s[index] + 1

            if s[index] < n:
                for iA in range(index+1, r):
                    s[iA] = s[iA-1] + 1
            else:
                break;

        #if index == (r - 1):
        else:
            s[index] = s[index] + 1

            if s[index] >= n:
                break

            print("Found C (Index = %d): %s", (index, str(s)))
            retSet.append(s[:r]);

    return retSet

def genCombinationsEx3(n, r):
    s = []
    retSet = []

    for i in range(0, r):
        s.append(i)
    #retSet.append(s[:r]);

    retSet = combine(s, n, r, 0)

    return retSet