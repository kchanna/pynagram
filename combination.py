import math


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




def genCombinationsEx3(n, r):
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