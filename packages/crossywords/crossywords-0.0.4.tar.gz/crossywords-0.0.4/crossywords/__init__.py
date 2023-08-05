from crossywords.crossywords import main as m
from crossywords.crossywords import algorithm as a

def getMatrix(lang="en"):
	return (m.getMatrix(lang))


def printMatrix(matrix):
    for row in matrix:
        cellStr = ""
        for cell in row:
            cellStr += cell + ' '
        print(cellStr)


def printWords(words):
    for word in words:
        print(word + " - " + str(words[word]))