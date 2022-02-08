from torch import ge
from loadWords import loadFromWordle, loadWords
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

def getFrequencyByPosition():
    words = loadFromWordle()
    countsAtPosition = [dict(zip([chr(ord("a")+i) for i in range(26)], [0 for _ in range(26)])) for _ in range(5)]
    for word in words:
        for i,w in enumerate(word):
            countsAtPosition[i][w] += 1
    numOfWords = len(words)
    for pos in countsAtPosition:
        for w in pos:
            pos[w] /= numOfWords
    return countsAtPosition

def getFreqOfWordsByPosition():
    counts = getFrequencyByPosition()
    freq = []
    words = loadFromWordle()
    for word in words:
        temp = 0
        tempSet = set()
        for i,w in enumerate(word):
            temp += log(counts[i][w])
            tempSet.add(w)
        if len(tempSet) != 5:
            temp -= 100
        freq.append([word, temp])
    return freq


if __name__ == "__main__":
    # count, w, freq = getFreq()
    # print(getProbWithoutRepeatDeep()[:20])
    # counts = getFrequencyByPosition()
    # print(counts[0]["a"])
    freq = getFreqOfWordsByPosition()
    freq.sort(key=lambda x:x[1], reverse=True)
    print(freq[:10])
