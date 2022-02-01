from loadWords import loadWords
from collections import Counter
from math import log

def getFreq():
    allWords = loadWords()
    freq = Counter()
    count = 0
    words = []

    # count how many 5-letter words and 
    # total frequency of letters of all 5-letter words
    for w in allWords:
        if len(w) == 5:
            freq += Counter(w)
            count += 1
            words.append(w)

    words.sort()
    return count, words, dict(freq.most_common(26))
    # print(count, freq.most_common(26))


def getProb(word=None):
    """
    get probability of all words as a dict,
    or get probability of a specific word
    """
    count, words, freqs = getFreq()
    for letter in freqs:
        freqs[letter] = freqs[letter]/count/5
    probs = {}
    for w in words:
        temp = 0
        for c in w:
            temp += log(freqs[c])
        probs[w] = temp

    if word and word in probs:
        return probs[word]
    elif word and word not in probs:
        print("{} is probably not a word".format(word))
    return probs

## penalize words with repeat letters by remove it from results
def getProbWithoutRepeat(word=None):
    count, words, freqs = getFreq()
    for letter in freqs:
        freqs[letter] = freqs[letter]/count/5
    probs = {}
    for w in words:
        temp = 0
        if len(set(w)) == 5:
            for c in w:
                temp += log(freqs[c])
            probs[w] = temp

    if word and word in probs:
        return probs[word]
    elif word and word not in probs:
        print("{} is probably not a word or contains repeat letters".format(word))
    
    sortedFreq = sorted(list(probs.items()), key=lambda x:x[1], reverse=True)
    return sortedFreq


def getProbWithoutRepeatDeep(n=None):
    """
    remove words with repeat letters;
    remove words with same five letter but different combinations
    """
    count, words, freqs = getFreq()
    for letter in freqs:
        freqs[letter] = freqs[letter]/count/5
    probs = {}
    wordSet = set()
    for w in words:
        temp = 0
        if len(set(w)) == 5:
            if tuple(sorted(set(w))) not in wordSet:
                wordSet.add(tuple(sorted(set(w))))
                for c in w:
                    temp += log(freqs[c])
                probs[w] = temp

    sortedFreq = sorted(list(probs.items()), key=lambda x:x[1], reverse=True)
    if not n:
        return sortedFreq
    else:
        return sortedFreq[:n]

if __name__ == "__main__":
    count, w, freq = getFreq()
    print(getProbWithoutRepeatDeep()[:20])
