import itertools
import openpyxl
from pathlib import Path
import sys

def createInitial(T):
    elemSet = list()
    for transaction in T:
        for item in transaction:
            elemSet.append(item)
    return list(set(elemSet))

def createCandicates(L):
    newList = list()
    if isinstance(L[0], tuple):
        for item in L:
            for jitem in L:
                temp1 = set(item)
                temp2 = set(jitem)
                new = temp1.union(temp2)
                if len(new) == len(item)+1:
                    if not any(x in newList for x in itertools.permutations(tuple(new))):
                        newList.append(tuple(new))
    else:
        newList = list(itertools.combinations(L, 2))
    return newList


def Apriori(T, minSup, minConfidance):
    L=dict()
    L[1] = createInitial(T)
    L[1] = sorted(L[1])
    k = 2
    while len(L[k-1]) >0:
        C = createCandicates(L[k-1])
        supports = {item:0 for item in C}
        sSupports = {item[:-1]:0 for item in C}
        for transaction in T:
            for candicate in C:
                if all(x in transaction for x in candicate):
                    supports[candicate] += 1
                if all(x in transaction for x in candicate[:-1]):
                    sSupports[candicate[:-1]] += 1
        supports = {item:sup for item,sup in supports.items() if sup > 0}
        confidance = {item:sup/sSupports[item[:-1]] for item,sup in supports.items()}
        if minSup == None and minConfidance == None:
            L[k] = [item for item,sup,conf in zip(list(supports.keys()),list(supports.values()),list(confidance.values())) if sup > min(list(supports.values())) and conf > min(list(confidance.values()))]
        elif minSup == None:
            L[k] = [item for item,sup,conf in zip(list(supports.keys()),list(supports.values()),list(confidance.values())) if sup > min(list(supports.values())) and conf >minConfidance]
        elif minConfidance == None:
            L[k] = [item for item,sup,conf in zip(list(supports.keys()),list(supports.values()),list(confidance.values())) if sup > minSup and conf > min(list(confidance.values()))]
        else:
            L[k] = [item for item,sup,conf in zip(list(supports.keys()),list(supports.values()),list(confidance.values())) if sup > minSup and conf > minConfidance]
        L[k] = sorted(L[k])
        k += 1
    return L[len(L)-1]


filename = sys.argv[1]
try:
    minSup = float(sys.argv[2])
except IndexError:
    minSup = 1.0
try:
    minConf = float(sys.argv[3])
except IndexError:
    minConf = 0.05

extension = filename.split(".")[1]
if extension == "txt":
    transactionsFile = open(filename, "r")

    transactions = list()
    for line in transactionsFile:
        line = line[:-1].split(",")
        transactions.append(line)

    transactionResults = Apriori(transactions, minSup, minConf)
    outf = open("output.txt", "w+")
    for item in transactionResults:
        outf.write(str(list(item)) + "\n")
    outf.close()

elif extension == "xlsx":
    transactionsFile = Path(filename)
    wb_obj = openpyxl.load_workbook(transactionsFile)
    sheet = wb_obj.active
    transactions = list()
    temp = list()
    tempID = 0
    for i, row in enumerate(sheet.iter_rows(values_only=True)):
        if i == 0:
            continue
        elif i == 1:
            tempID = row[0]
            temp.append(row[1])
        else:
            if tempID == row[0]:
                temp.append(row[1])
            else:
                transactions.append(temp)
                temp = []
                tempID = row[0]
                temp.append(row[1])
    
    transactionResults = Apriori(transactions, minSup, minConf)
    outf = open("output.txt", "w+")
    for item in transactionResults:
        outf.write(str(list(item)) + "\n")
    outf.close()