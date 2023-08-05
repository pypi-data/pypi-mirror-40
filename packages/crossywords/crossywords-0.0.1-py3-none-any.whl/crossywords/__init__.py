import main as m

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