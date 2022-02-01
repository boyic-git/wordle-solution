from loadWords import loadFiveLetterWords, loadFromWordle
from getFrequency import getProbWithoutRepeatDeep
from random import randint
from collections import Counter, defaultdict

def solve(bank, word, result, wrong):
    correct, maybe, wrong = decodeResult(word, result, wrong)
    print(correct, maybe, wrong)

    newBank = []
    for w in bank:
        temp = defaultdict(int)
        for c in wrong:
            if c in set(w) and (c not in correct.values())\
                and (c not in maybe):
                break
            if c in correct.values():
                for i in range(5):
                    if i not in correct and w[i] == c:
                        break
        else:
            for i in correct:
                if w[i] != correct[i]:
                    break
            else:
                for i in range(5):
                    if i not in correct:
                        temp[w[i]] += 1
                for c in maybe:
                    if c not in temp or maybe[c] > temp[c]:
                        break
                else:
                    newBank.append(w)
    return newBank, newBank[randint(0, len(newBank)-1)]


    return bank, word

def decodeResult(word, result, wrong):
    correct = {}
    maybe = defaultdict(int)
    for i, r in enumerate(result):
        if r == "y":
            correct[i] = word[i]
        elif r == ".":
            maybe[word[i]] += 1
        else:
            wrong.add(word[i])
    return correct, maybe, wrong

def randomGuess():
    words = getProbWithoutRepeatDeep(20)
    return words[randint(0,19)][0]

if __name__ == "__main__":
    i = 1
    bank = loadFromWordle()
    result = None
    word = None
    wrong = set()
    print("erato" in bank)
    while True:
        if i == 1:
            word = randomGuess()
        else:
            bank, word = solve(bank, word, result, wrong)
        if len(bank) == 0:
            print("The word is not included in my dictionary.")
            break
        print("Guess #{}: {}, out of {} words.".format(i, word, len(bank)))
        if len(bank) < 10:
            print(bank)

        result = input("What's the result?\n")
        if result == "yyyyy":
            print("Congraduations! The result is {}.".format(word))
            break
        i += 1
    print("The correct word is {}".format("apple"))