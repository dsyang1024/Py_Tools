#유량 자료를 기준으로 유황별 정렬하기
from datetime import date
from matplotlib import pyplot as plt
import os
import sys
plt.rcParams["font.family"] = "Times New Roman"
plt.rc('font',size=12)

path = os.getcwd()

#	사용자가 업로드한 이름으로 변경 필요 ******
f = open(path+'/streamflow.csv','r')
data = f.readlines()


#	날짜와 유량자료 형태 변환
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


#	그래프 플로팅
plt.figure(figsize=(8,4))
plt.title('FDC Graph')
plt.yscale('log')

plt.xlabel("Flow Exceedance(%)")
plt.xlim(0,100)
plt.xticks([0,10,40,60,90,100])
plt.ylabel("Streamflow (Log CMS)")

# 그래프 상의 Y축 제한
#plt.ylim(0.01,1000)
#plt.yticks([0.1,1,10,100,1000])

plt.grid()

plt.plot(exist,FDC,color='blue')
plt.tight_layout()
plt.savefig(path + '/FDC graph.png', dpi=300)
plt.show()



#	FDC를 기반으로 75%, 50%, 25%로 기준이 되는 유량 파악하기
flow_criteria = []
for i in [10, 40, 60, 90]:
	a = []
	for r in range(len(exist)):
		a.append(abs(i-exist[r]))
	flow_criteria.append(FDC[a.index(min(a))])

print(flow_criteria)

#	유황별 기준 유량 파일로 저장
result = open(path+'유황기준.csv','w')
result.write('\n')
for i in range(len(flow_criteria)):
	result.write(str(flow_criteria[i])+'\n')
result.close()
