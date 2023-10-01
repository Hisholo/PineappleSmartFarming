import pandas as pd
from datetime import datetime
from Pineapple import Pineapple

def findStage(dayOfYear,year): 
    months = {'1' : 31, '2' : 28, '3' : 31, '4' : 30, '5' : 31, '6' : 30, '7' : 31, '8' : 31, '9' : 30, '10' : 31, '11' : 30, '12' : 31}
    if(year % 4 == 0):
        months['2'] = 29
    month = 0
    sum = 0
    while(True):
        month = month + 1
        if month > 12:
            break
        sum = sum + months[f'{month}']
        if sum > dayOfYear:
            sum = sum - months[f'{month}']
            break
    day = dayOfYear - sum
    #print(f"{day}-{month}-{year}")

    if (year == 2021 and month >= 5) or (year == 2022 and month <= 2):
        return 1
    elif(year == 2022 and month > 2 and month <= 5):
        return 2
    else:
        return 3

df = pd.read_csv("Medziphema weather dataset.csv")
yearList = df.iloc[:,0].values
dayOfYearList = df.iloc[:,1].values
solarRadiationList = df.iloc[:,2].values
minTempList = df.iloc[:,3].values
maxTempList = df.iloc[:,4].values
relativeHumidityList = df.iloc[:,5].values
windSpeedList = df.iloc[:,6].values
EToList = []
stageList = []
ETcList = []
waterRequirementList = []

for i in range(len(dayOfYearList)):
    stageList.append(findStage(dayOfYearList[i], yearList[i]))
    EToList.append(Pineapple.referenceEvapotranspiration(minTempList[i], maxTempList[i], windSpeedList[i], relativeHumidityList[i], solarRadiationList[i], dayOfYearList[i]))

for i in range(len(EToList)):
    ETcList.append(Pineapple.cropEvapotranspiration(stageList[i],EToList[i]))

for i in range(len(ETcList)):
    waterRequirementList.append(Pineapple.waterRequirement(ETcList[i]))

AWRStage1 = 0
countForS1 = 0

AWRStage2 = 0
countForS2 = 0

AWRStage3 = 0
countForS3 = 0

for i in range(len(stageList)):
    if stageList[i] == 1:
        AWRStage1 = AWRStage1 + waterRequirementList[i]
        countForS1 += 1
    elif stageList[i] == 2:
        AWRStage2 = AWRStage2 + waterRequirementList[i]
        countForS2 += 1
    else:
        AWRStage3 = AWRStage3 + waterRequirementList[i]
        countForS3 += 1

print("Average water required by each stage in pineapple per Plant per Liter: ")
print(f"1.Vegetative Stage : {round(AWRStage1/countForS1,3)}\n2.Flowering Stage : {round(AWRStage2/countForS2,3)}\n3.Fruit Maturation Stage : {round(AWRStage3/countForS3,3)}")

'''csvFile = {"Year" : yearList, "Day_Of_Year" : dayOfYearList, "Solar_Radiation" : solarRadiationList, "Minimum_Temperature" : minTempList,
            "Maximum_Temperature" : maxTempList, "Relative_Humidity_List" : relativeHumidityList, "Wind_Speed" : windSpeedList,
            "ETo" : EToList, "ETc" : ETcList, "ETc" : ETcList, "Stage" : stageList, "Water_Requirement" : waterRequirementList}

csvFile = pd.DataFrame(csvFile)

csvFile.to_csv("Result.csv",index=False)'''