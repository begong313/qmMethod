from find_logic import *
import copy

# subEPI를 사용자 입력을 직접받아? or자동으로 입력받아 빼는 code구현, subEPI,EPI는 결과식으로 들어가고 rowd,Cold로 사라지는 pi는 결과식에 도출 x
# minterm=[4, 8, 0, 4, 8, 10, 12, 11, 13, 15] 4 8 0 4 8 10 12 11 13 15
switch = True
resultEPI=[]
while True:
    if switch:  # 처음과 초기화하고싶을때 true로바뀜
        try:
            firstminterm = list(map(int, input("[input의 수, minterm의 수, minterm들을 한칸의 공백을 두고 입력하시오]").split()))
            minterm = copy.deepcopy(firstminterm[2:])
            piAndEpi = findPiEpi(firstminterm)
            sepN = piAndEpi.index('EPI')
            pi = piAndEpi[:sepN]
            epi = piAndEpi[sepN + 1:]
            resultEPI.extend(epi)
            printTable(minterm, pi)
            print("resultEPI",resultEPI)
            switch = False
            continue
        except:
            print("잘못된값이 입력되어 종료니다.")
            break

    try:
        order = input("원하는동작을 입력하시오. (delEPI, subEPI subDcare, rowD, colD, petrick(실행시 종료), exit)").strip()

        if order == "delEPI":
            minterm = delEpiMinterm(minterm, epi)
            pi = subEPI(pi, epi)

        elif order=="subEPI":
            inputSubEPI=input("subEPI를 하나만 입력하시오 (따움표 제외)")
            pi.remove(inputSubEPI)
            minterm=delEpiMinterm(minterm,[inputSubEPI])
            resultEPI.append(inputSubEPI)

        elif order == "subDcare":
            dcare = map(int, input("한칸의 공백을 두고 dCare을 입력하시오").split())
            minterm = subDcareMinterm(minterm, dcare)

        elif order == "rowD":
            pi = checkRowD(minterm, pi)

        elif order == 'colD':
            minterm = checkColumnD(minterm, pi)

        elif order == 'exit':
            print("종료합니다")
            break

        elif order == 'petrick':
            resultEPI.extend(pi)
            print("PETRICK", findPetrick(resultEPI))
            print("종료합니다")
            break
        else:
            print('정확한값을 다시입력해주십시오')

        printTable(minterm, pi)
        print("resultEPI", resultEPI)
        print("-----------------------------------------------------------")
    except :
        print("예상치못한 동작이 감지되어 프로그램을 종료합니다.")
        break
