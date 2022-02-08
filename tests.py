from collections import Counter
from loadWords import loadFromWordle
from random import randint
from solve import randomGuess, solve

def check(guess, answer):
    ## result - 0: Wrong
    ##          1: Correct
    ##          2: Maybe
    result = [0 for _ in range(5)]
    count = Counter(answer)
    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = 1
            count[guess[i]] -= 1

    for i in range(5):
        if result[i] == 1:
            continue
        if guess[i] != answer[i]:
            if count[guess[i]] == 0:
                result[i] = 0
            else:
                result[i] = 2
                count[guess[i]] -= 1
    
    resultStr = ""
    for c in result:
        if c == 0:
            resultStr += "x"
        elif c == 1:
            resultStr += "y"
        else:
            resultStr += "."
    return resultStr
        

def test(n=10):
    total = 0
    for i in range(n):
        bank = loadFromWordle()
        answer = bank[randint(0, len(bank)-1)]
        guess = randomGuess()
        wrong = set()
        times = 0
        while guess != answer:
            result = check(guess, answer)
            bank, guess = solve(bank, guess, result, wrong)
            times += 1
        total += times
        print(i, guess, times)
    print("Average guess times: {:.2f}".format(float(total/n)))


if __name__ == "__main__":
    bank = loadFromWordle()
    print(len(bank))
    # for i in range(10):
    #     guess = bank[randint(0, len(bank)-1)]
    #     answer = bank[randint(0, len(bank)-1)]
    #     result = check(guess, answer)
    #     print(guess, answer, result)
    # print(check("bbbca", "aabba"))
    # test(100)
