import copy
import math
from tabulate import tabulate


def toBin(minterm,length):
    toBinArr=[]
    for i in range(len(minterm)):
        temp = bin(minterm[i])[2:]
        while len(temp) != length:
            temp = "0" + temp
        toBinArr.append(temp)
    return toBinArr

def findPiEpi(minterm):
    BinArr=toBin(minterm[2:],minterm[0])
    answer = []
    # 1의 개수로 나누기
    sepByOne = [[] for i in range(minterm[0] + 1)]
    for i in BinArr:
        iCount = 0
        for j in range(len(i)):
            if i[j] == "1":
                iCount += 1
        sepByOne[iCount].append(i)
        answer.append(i)

    for kk in range(minterm[0]):
        doDo = [[] for i in range(minterm[0] + 1)]
        for i in range(len(sepByOne) - 1):

            for j in sepByOne[i]:  # j,k=정렬된 배열안원소들
                for k in sepByOne[i + 1]:
                    sepCount = 0
                    sepIndex = 0
                    for z in range(len(j)):
                        if sepCount >= 2:
                            break;
                        if j[z] != k[z]:
                            sepCount += 1
                            sepIndex = z
                    else:
                        changedPI = j[:sepIndex] + "-" + j[sepIndex + 1:]  # -로 바꾼것
                        if sepCount == 1:
                            if changedPI not in doDo[i]:
                                doDo[i].append(changedPI)
                            if changedPI not in answer:
                                answer.append(changedPI)
                            try:
                                answer.remove(j)
                            except:
                                pass
                            try:
                                answer.remove(k)
                            except:
                                pass

        sepByOne = copy.deepcopy(doDo)

    answer.sort(key=lambda x: x.replace("-", "2"))

    # 여기까진 pi 구한것
    epiCheck = [-1 for i in range(int(math.pow(2, minterm[0])))]
    for i in minterm[2:]:
        epiCheck[i] = 0
    plusArr = ["EPI"]
    a=1
    ii=0
    while ii<2:
        for i in answer:
            check_ = 0
            for j in i:
                if j == "-":
                    check_ += 1
            for k in BinArr:
                difchek = 0
                for kk in range(minterm[0]):
                    if i[kk] != k[kk]:
                        difchek += 1
                if a:
                    if difchek == check_ and epiCheck[int(k, 2)] != -1:
                        epiCheck[int(k, 2)] += 1
                else :
                    if difchek == check_ and epiCheck[int(k, 2)] == 1 and (i not in plusArr):
                        plusArr.append(i)
        ii+=1
        a=0
    answer.extend(plusArr)

    return answer

def delEpiMinterm(minterm, EPI):
    BinArr = toBin(minterm,len(EPI[0]))
    tempMinterm =copy.deepcopy(minterm)
    for pis in EPI:
        checkDesh = 0
        for j in pis:
            if j == "-":
                checkDesh += 1
        for binNum in BinArr:
            difchek = 0
            for kk in range(len(pis)):
                if pis[kk] != binNum[kk]:
                    difchek += 1
            if difchek == checkDesh and tempMinterm.count(int(binNum, 2))!=0:
                tempMinterm.remove(int(binNum, 2))
    return tempMinterm


def subDcareMinterm(minterm,dcareNum):
    tempMinterm=copy.deepcopy(minterm)
    for i in dcareNum:
        if i in tempMinterm:
            tempMinterm.remove(i)
    return tempMinterm

def subEPI(pi,epi):
    temppi=copy.deepcopy(pi)
    for i in epi:
        temppi.remove(i)
    return temppi

def checkRowD(minterm, pi):
    binArr = toBin(minterm,len(pi[0]))
    tempdict = {}

    # 임시 list생성
    for i in pi:
        tempdict[i] = []
    # Pi들이 어떤 minterm을 가지나 체크 후 dict에 저장
    for i in range(len(pi)):
        count_ = pi[i].count('-')
        for j in range(len(binArr)):
            defcount = 0
            for k in range(len(pi[i])):
                if pi[i][k] != binArr[j][k]:
                    defcount += 1
            if defcount == count_:
                tempdict[pi[i]].append(int(binArr[j], 2))
    # dict를 활용해, 한 pi가 다른 pi를 포함한다면 포함되는 pi의 원소를 없에주기 (만약에 하나의 1>2>3의 경우 1이 모든것을 포함하니 사라지는 순서는 상관없음)
    for i in pi:
        for j in pi:
            if i != j:
                for ele in tempdict[i]:
                    if ele in tempdict[j]:
                        pass
                    else:
                        break
                else:
                    tempdict[i] = []
    # dic의 value에 값이 남아있을 경우만 리턴
    answer = []
    for i in pi:
        if tempdict[i] != []:
            answer.append(i)
    return answer

def checkColumnD(minterm, pi):
    binArr = toBin(minterm,len(pi[0]))
    tempdict = {}
    # 임시 dict생성
    for i in minterm:
        tempdict[i] = []
    # Pi들이 어떤 minterm을 가지나 체크 후 dict에 저장
    for i in range(len(binArr)):
        for j in range(len(pi)):
            count_ = pi[j].count('-')
            defcount = 0
            for k in range(len(pi[j])):
                if pi[j][k] != binArr[i][k]:
                    defcount += 1
            if defcount == count_:
                tempdict[int(binArr[i], 2)].append(pi[j])

    # dict를 활용해, 한 pi가 다른 pi를 포함한다면 포함되는 pi의 원소를 없에주기 (만약에 하나의 1>2>3의 경우 1이 모든것을 포함하니 사라지는 순서는 상관없음)
    for i in minterm:
        for j in minterm:
            if i != j and tempdict[i] != [] and tempdict[j] != []:
                for ele in tempdict[i]:
                    if ele in tempdict[j]:
                        pass
                    else:
                        break
                else:
                    tempdict[j] = []
    # dic의 value에 값이 남아있을 경우만 리턴
    answer = []
    for i in minterm:
        if tempdict[i] != []:
            answer.append(i)
    return answer

#print table in console
def printTable(minterm,pi):
    topArr =['----']
    Binminterm=[]
    for i in range(len(minterm)):
        temp = bin(minterm[i])[2:]
        while len(temp) != len(pi[0]):
            temp = "0" + temp
        Binminterm.append(temp)

    for i in minterm:
        topArr.append(i)
    data = [[]for x in range(len(pi))]
    for i in range(len(pi)):
        data[i].append(pi[i])


    for k in range(len(pi)):
        count_=pi[k].count('-')
        for i in range(len(Binminterm)):
            diffCount = 0
            for j in range(len(pi[k])):
                if pi[k][j]!=Binminterm[i][j]:
                    diffCount+=1
            if diffCount==count_:
                data[k].append('0')
            else:
                data[k].append(' ')
    print(tabulate(data,headers=topArr))

def findPetrick(pi):
    result=[]
    for i in range(len(pi)):
        temp=''
        for j in range(len(pi[i])):
            if pi[i][j]=='1':
                temp+=chr(65+j)
            elif pi[i][j]=='0':
                temp+="!"+chr(65+j)
        result.append(temp)

    return '+'.join(result)