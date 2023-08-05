import random
from crossywords.crossywords import algorithm as a

# path to russian and english vocabulary bank (1000 words each)
pathRussian = "russian.txt"
pathEnglish = "english.txt"


def deleteEqualValues(words):
    deletedEqualValues = {}
    for comb in words:
        areUnique = True
        for item in words[comb]:
            for initialList in [item for item in list(deletedEqualValues.values())]:
                for initialItem in initialList:
                    if item == initialItem:
                        areUnique = False
        if areUnique:
            deletedEqualValues[comb] = words[comb]
    return deletedEqualValues


def bubbleSort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if len(items[j]) < len(items[j + 1]):
                items[j], items[j + 1] = items[j + 1], items[j]
    return items


def sortWordsInRelevantWay(words):
    # sorting dict by length of the comb
    listOfKeys = [item for item in words]
    listOfKeys = bubbleSort(listOfKeys)
    # having a sorted list instead of dict
    wordsList = [{item: words[item]} for item in listOfKeys]

    # splitting list in the middle into two parts
    # and getting a new list sorted in a relevant way
    sortedWordsList = []
    num = 1
    middle = len(wordsList) // 2
    for index in range(middle - 1):
        for k, v in wordsList[middle + num - 1].items():
            sortedWordsList.append({k: v})
        for k, v in wordsList[middle - num].items():
            sortedWordsList.append({k: v})
        num += 1
    return sortedWordsList


def selectCombinations(words):
    # all the possible letters combinations in all the words
    combinations = [word[start:end] for word in words for start in range(len(word) + 1)
                    for end in range(len(word) + 1) if len(word[start:end]) != 0]

    wordsDict = {}  # {comb: [allOfTheWordsThatContainSuchComb]}
    for word in words:
        for comb in combinations:
            if word.find(comb) != -1:  # if comb in the word
                if comb in wordsDict:  # if combination already in the the dict
                    if word not in wordsDict[comb]:  # if particular word not in the list
                        wordsDict[comb].append(word)
                else:
                    wordsDict[comb] = [word]
    # delete words which have no matches
    return {k: v for k, v in wordsDict.items() if len(v) > 1}


def getWords(path):
    with open(path, "r", encoding="windows-1251") as f:
        allWords = [word.replace("\n", "") for word in f]
        allWords = [word for word in allWords if word.find("-") == -1]
        random.shuffle(allWords)
        return allWords[:100]  # shuffling all of the words and getting 100 of them


def fillEmptySpaces(matrix, lang):
    russian = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
               'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    english = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'g', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    letters = russian if lang == pathRussian else english
    for rowIndex in range(len(matrix)):
        for columnIndex in range(len(matrix[rowIndex])):
            if matrix[rowIndex][columnIndex] is None:
                matrix[rowIndex][columnIndex] = letters[random.randint(0, 9)]
    return matrix


def getMatrix(lang):
    lang = pathRussian if lang == "ru" else pathEnglish
    words = getWords(lang)  # getting all words

    # selecting words combinations {partOfTheWord: [allOfTheWordsThatContainSuchPart]}
    words = selectCombinations(words)
    # deleting equal values (some comb could refer to the same value)
    words = deleteEqualValues(words)
    # sorting words by length of comb and getting a new list starting from the middle
    words = sortWordsInRelevantWay(words)

    # getting only first half of the list and shuffle it
    random.shuffle(words[:len(words) // 2])

    # getting a matrix and [allWordsInTheMatrix] from Algorithm file
    matrix, words = a.getMatrixAndWords(words)
    matrix = fillEmptySpaces(matrix, lang)
    return matrix, words
