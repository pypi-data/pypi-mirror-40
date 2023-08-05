import random
isDone = False
matrix = [[None for j in range(5)] for i in range(5)]


def neighbourFunction(i, j, x, y):
    # distance between two points formula
    return (j ** 2 - 2 * j * x + x ** 2) + (i ** 2 - 2 * i * y + y ** 2)


def getFreeNeighbours(i, j):
    global matrix
    # getting all the accessible cells using neighbour function
    # to check whether cell accessible or not
    accessibleCells = [[y, x] for y in range(5) for x in range(5)
                       if neighbourFunction(i, j, x, y) == 1
                       or neighbourFunction(i, j, x, y) == 2]

    # returning free cells only (if they are equal to None)
    freeNeighbours = [pair for pair in accessibleCells if matrix[pair[0]][pair[1]] is None]
    random.shuffle(freeNeighbours)
    return freeNeighbours


def getStackFreeInitialCells():
    global matrix
    # stack of free cells at the beginning
    stackFreeInitialCells = [[i, j] for j in range(len(matrix)) for i in range(len(matrix[j])) if matrix[i][j] is None]
    random.shuffle(stackFreeInitialCells)
    return stackFreeInitialCells


def fillWord(stackLetters, stackWay, stackFreeCells):
    global isDone  # global variable True if the word has been successfully inserted

    # Step 1 - pick i and j to insert the letter
    # getting the first item from free cells from the end
    stackFreeCellsIJ = stackFreeCells[-1].pop(0) \
        if stackFreeCells[-1] and len(stackFreeCells[-1]) != 0 else [None, None]
    i, j = stackFreeCellsIJ[0], stackFreeCellsIJ[1]

    # Step 2 - insert the letter
    # or delete the previous letter if there are no free accessible cells
    if i is not None and j is not None:
        matrix[i][j] = stackLetters.pop(0)  # inserting to the matrix
        stackWay.append([i, j])  # adding coordinates to the stack way
        if len(stackLetters) != 0:
            stackFreeCells.append(getFreeNeighbours(i, j))  # adding free neighbours to the stack of free cells
            fillWord(stackLetters, stackWay, stackFreeCells)
            return stackWay if isDone else None
        else:
            # once stackLetters is empty (we have successfully inserted the word) we mark isDone variable as True
            isDone = True
            return stackWay if isDone else None
    else:
        for place in reversed(stackWay):
            deletedLetter = matrix[place[0]].pop(place[1])
            matrix[place[0]].insert(place[1], None)
            stackLetters.insert(0, deletedLetter)  # adding to the stack of letters the last letter
            # deleting the last element on the way and of free cells (it is always an empty list)
            stackWay.pop(), stackFreeCells.pop()
            fillWord(stackLetters, stackWay, stackFreeCells)
            return stackWay if isDone else None
        return False


def getMatrixAndWords(words):
    global matrix

    combinations = [comb for item in words for comb in item]  # all the combinations
    words = [item[comb] for item in words for comb in item]  # all the words with such combination

    filledWords = {}  # {word in the matrix: [coordinates]}

    for index in range(len(combinations)):
        stackWay = []  # stack with coordinates of way filling the word
        stackFreeCells = [getStackFreeInitialCells()]  # stack with free cells in each step of insertion
        way = fillWord([letter for letter in combinations[index]], stackWay, stackFreeCells)
        if way:
            comb = combinations[index]
            for word in words[index]:
                i1, j1 = way[0][0], way[0][1]  # first coordinate
                i2, j2 = way[len(comb) - 1][0], way[len(comb) - 1][1]  # last coordinate
                # getting indexes of starting and ending comb
                endIndexFirstLetter = word.find(comb)
                startIndexLastLetter = endIndexFirstLetter + len(comb)

                # getting the first and the second part of the word
                # (the first should be reversed as we are going to insert the word backwards)
                firstPartStackLetters = list(reversed([word[index] for index in range(endIndexFirstLetter)]))
                a = fillWord(firstPartStackLetters, stackWay=[], stackFreeCells=[getFreeNeighbours(i1, j1)]) \
                    if len(firstPartStackLetters) != 0 else True

                secondPartStackLetters = [word[index] for index in range(startIndexLastLetter, len(word))]
                b = fillWord(secondPartStackLetters, stackWay=[], stackFreeCells=[getFreeNeighbours(i2, j2)]) \
                    if len(secondPartStackLetters) != 0 else True
                if not a and b and len(getStackFreeInitialCells()) < 5:
                    return matrix, filledWords
                elif a and b:
                    a = list(reversed(a)) if not isinstance(a, bool) else []
                    b = b if not isinstance(b, bool) else []
                    filledWords[word] = a + way + b  # adding word and path to the dict
        else:
            return matrix, filledWords
    return matrix, filledWords
