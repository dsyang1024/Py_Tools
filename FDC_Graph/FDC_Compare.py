# Dongseok Yang.
# Kangwon National University
# Any issues can be reported to dongseok.yang@kangwon.ac.kr
# Have good day!

#유량 자료를 기준으로 유황별 정렬하기
from datetime import date
from matplotlib import pyplot as plt
import os
import sys
plt.rcParams["font.family"] = "Times New Roman"
plt.rc('font',size=12)

#유량 자료 입력 부분 / 파일 확장자는 입력하지마세요...
file1 = '20_streamflow'
file2 = '20_SRI_streamflow'

path = os.getcwd()

#	사용자가 업로드한 이름으로 변경 필요 ******
# 비교 대상 유량 산정하기
f = open(path + '/' + file1 + '.csv', 'r')
k = open(path + '/' + file2 + '.csv', 'r')

data = f.readlines()
data2 = k.readlines()


#	날짜와 유량자료 형태 변환 관행방법
for i in range(1,len(data)):
	data[i] = data[i].replace('\n','')
	data[i] = data[i].split(',')
	data[i][0] = data[i][0].split('-')
	
	#	날짜 정규식으로 변환
	for r in range(len(data[i][0])):
		data[i][0][r] = int(data[i][0][r])
	
	#	날짜 데이터로 정리
	data[i][0] = date(data[i][0][0],data[i][0][1],data[i][0][2])
	#	유량자료 실수로 변환
	data[i][1] = round(float(data[i][1]),3)


#	날짜와 유량자료 형태 변환 SRI 방법
for i in range(1,len(data)):
	data2[i] = data2[i].replace('\n','')
	data2[i] = data2[i].split(',')
	data2[i][0] = data2[i][0].split('-')
	
	#	날짜 정규식으로 변환
	for r in range(len(data2[i][0])):
		data2[i][0][r] = int(data2[i][0][r])
	
	#	날짜 데이터로 정리
	data2[i][0] = date(data2[i][0][0],data2[i][0][1],data2[i][0][2])
	#	유량자료 실수로 변환
	data2[i][1] = round(float(data2[i][1]),3)





#	FDC 리스트 정리
FDC = []
exist = []
for i in range(1,len(data)):
	if data[i][1] not in FDC:
		FDC.append(data[i][1])
		exist.append(1)
	else:
		exist[FDC.index(data[i][1])] = exist[FDC.index(data[i][1])]+1


#	FDC 값 만들어주기 // list로 작성할 경우 sorting에 어려움이 있어서 tuple로 작성 후 list로 변경
temp = []
for i in range(len(FDC)):
	temp.append((FDC[i],exist[i]/len(data)*100))

#	유량 크기순으로 정렬
FDCtuple = sorted(temp, key = lambda x : (-x[0]))

#	튜플을 리스트로 변경
FDClist = []
for i in range(len(FDCtuple)):
	FDClist.append(list(FDCtuple[i]))

#FDC 재현 빈도 누적으로 변경하기
for i in range(1,len(FDClist)):
	FDClist[i][1] = round(FDClist[i][1]+FDClist[i-1][1],3)

FDC = []
exist = []
for i in range(len(FDClist)):
	FDC.append(FDClist[i][0])
	exist.append(FDClist[i][1])




#	FDC2 리스트 정리
FDC2 = []
exist2 = []
for i in range(1,len(data2)):
	if data2[i][1] not in FDC2:
		FDC2.append(data2[i][1])
		exist2.append(1)
	else:
		exist2[FDC2.index(data2[i][1])] = exist2[FDC2.index(data2[i][1])]+1


#	FDC2 값 만들어주기 // list로 작성할 경우 sorting에 어려움이 있어서 tuple로 작성 후 list로 변경
temp = []
for i in range(len(FDC2)):
	temp.append((FDC2[i],exist2[i]/len(data2)*100))

#	유량 크기순으로 정렬
FDC2tuple = sorted(temp, key = lambda x : (-x[0]))

#	튜플을 리스트로 변경
FDC2list = []
for i in range(len(FDC2tuple)):
	FDC2list.append(list(FDC2tuple[i]))

#FDC2 재현 빈도 누적으로 변경하기
for i in range(1,len(FDC2list)):
	FDC2list[i][1] = round(FDC2list[i][1]+FDC2list[i-1][1],3)

FDC2 = []
exist2 = []
for i in range(len(FDC2list)):
	FDC2.append(FDC2list[i][0])
	exist2.append(FDC2list[i][1])








#	그래프 플로팅
plt.figure(figsize=(8,4))
# plt.title('FDC Graph')
plt.yscale('log')

plt.xlabel("Flow Exceedance(%)")
plt.xlim(0,100)
plt.xticks([0,10,40,60,90,100])
plt.ylabel("Streamflow (Log CMS)")

# 그래프 상의 Y축 제한
#plt.ylim(0.01,1000)
#plt.yticks([0.1,1,10,100,1000])
plt.grid()

#그래프 legend 이름 바꾸기
plt.plot(exist, FDC, color='blue', label = file1)
plt.plot(exist2,FDC2,color='red', label= file2)
plt.legend()
plt.tight_layout()
plt.savefig(path + '/FDC_graph.png', dpi=400)
plt.show()


#	FDC를 기반으로 75%, 50%, 25%로 기준이 되는 유량 파악하기
flow_criteria = []
flow_criteria2 = []
for i in [10, 40, 60, 90]:
	a = []
	for r in range(len(exist)):
		a.append(abs(i-exist[r]))
	flow_criteria.append(FDC[a.index(min(a))])

for i in [10, 40, 60, 90]:
	a = []
	for r in range(len(exist2)):
		a.append(abs(i-exist2[r]))
	flow_criteria2.append(FDC2[a.index(min(a))])


print('for first flow :: ', flow_criteria)
print('for second flow :: ', flow_criteria2)
