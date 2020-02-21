import timeit
start = timeit.default_timer()

libTable = []
busy = 0
booksProcessed = set()

def solution(books, libs, days, scores, libDetails, libBooks):
    global libTable, busy

    for iL in range(libs):
        libTable.append([iL, False, libDetails[iL][1], 0, set()])

    #main processing
    for currday in range(days):

        for iL in range(libs):
            if libTable[iL][2] > 0 and libTable[iL][1] == True:
                #print(libTable[iL])
                libTable[iL][2] -= 1

        if busy > 0:
            busy -= 1
            
        if busy == 0:
            iL = findBestLib(libDetails, currday, days)

            if iL is not None:
                libTable[iL][1] = True
                busy = libDetails[iL][1]

                clearBestLibBooksFromOtherLibs(iL, libBooks)

        for iL in range(libs):
            if libTable[iL][2] == 0 and libTable[iL][1] == True:
                for ibpd in range(libDetails[iL][2]):
                    bestBook = findBestBook(libBooks[iL], scores)

                    if bestBook is not None:
                        booksProcessed.add(bestBook)
                        libTable[iL][3] += 1
                        libTable[iL][4].add(bestBook)
                        #clearScannedBookFromAllLibs(bestBook, libBooks)
                        libBooks[iL].discard(bestBook)

        formatOutput(libs, libTable)
        print(currday)
        
    return formatOutput(libs, libTable)


#format final output
def formatOutput(libs, libTable):
    
    libCount = 0
    for iL in range(libs):
        if libTable[iL][3] > 0:
            libCount += 1

    final = []
    final.append([libCount])

    for iL in range(libs):
        if libTable[iL][3] > 0:
            final.append([iL, libTable[iL][3]])
            final.append(libTable[iL][4])

    write_file(final, "temp.out")
    return final


def clearScannedBookFromAllLibs(scannedBook, libBooks):

    for books in libBooks:
        books.discard(scannedBook)


def clearBestLibBooksFromOtherLibs(myLibId, libBooks):

    for myLibBook in libBooks[myLibId]:
        for iL, books in enumerate(libBooks):
            if iL != myLibId:
                books.discard(myLibBook)
                

def findBestBook(books, scores):
    global booksProcessed

    maxBookPoint = 0
    bestBookId = None

    for book in books:
        if True: #book not in booksProcessed:
            if maxBookPoint <= scores[book]:
                maxBookPoint = scores[book]
                bestBookId = book

    return bestBookId


def findBestLib(libDetails, currday, days):
    global libTable, busy
    minSignupDays = days
    bestLibIndex = None

    for iL, libDetail in enumerate(libDetails):
        if (libTable[iL][1] == False):
            if minSignupDays >= libDetail[1]:
                minSignupDays = libDetail[1]
                bestLibIndex = iL

    return bestLibIndex


def read_file(filename):
    """Reading input file."""

    with open(filename, 'r') as fin:
        line = fin.readline()
        books, libs, days = [int(num) for num in line.split()]

        line = fin.readline()
        scores = tuple([int(num) for num in line.split()])

        libDetails = []
        libBooks = []
        for i in range(0, libs * 2, 2):
            line = fin.readline()
            libDetails.append(tuple([int(num) for num in line.split()]))

            line = fin.readline()
            libBooks.append(set([int(num) for num in line.split()]))

    return books, libs, days, scores, libDetails, libBooks


def write_file(grid, filename):
    """Write output file."""
    with open(filename, 'w') as fout:
        for v in grid:
            fout.write(" ".join("" + str(r) + "" for r in v) + '\n')


def main():
    """Main function"""
    filename = "c_incunabula.txt"

    print('Running on file: %s' % filename)

    # read input file
    books, libs, days, scores, libDetails, libBooks = read_file(filename)
    try:
        grid_out = solution(books, libs, days, scores, libDetails, libBooks)
    except KeyboardInterrupt:
        pass

    # write output file
    write_file(grid_out, "c.out")
    print("finish")


if __name__ == '__main__':
    main()

print('Time:', round(timeit.default_timer() - start, 5), "seconds.")
