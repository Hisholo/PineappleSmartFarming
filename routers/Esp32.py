from fastapi import APIRouter, status, HTTPException
from .components.Firebase import Connect
from .components.Pineapple import Pineapple
from time import sleep
from .components import Schema
from datetime import datetime


router = APIRouter(
    prefix="/Esp32",
    tags=["Esp32"]
)

def currentMonthAndDay():
    currentMonth = datetime.now().strftime("%m")
    listOfMonths = ["January","Febuary","March","April","May","June","July","Auguast","September","October","November","December"]
    return f"{listOfMonths[int(currentMonth)-1]} {datetime.now().strftime('%d')}"

def currentYear():
    return datetime.now().strftime("%Y")

@router.post("/SensorData")
async def getSensorData(sensorData : Schema.SensorData):
    #Connection to firebase (real time database)
    try:
        firebase = Connect()
        DB = firebase.database()
        search = DB.child(currentYear()).child(currentMonthAndDay()).get().val()

        temperatureList = [] if search == None else search["Temperature"]
        solarRadiationList = [] if search == None else search["SolarRadiation"]
        windSpeedList = [] if search == None else search["WindSpeed"]
        humidityList = [] if search == None else search["Humidity"]

        temperatureList.append(sensorData.temperature)
        solarRadiationList.append(sensorData.solarRadiation)
        windSpeedList.append(sensorData.windSpeed)
        humidityList.append(sensorData.humidity)

        DB.child(currentYear()).child(currentMonthAndDay()).child("Temperature").set(temperatureList)
        DB.child(currentYear()).child(currentMonthAndDay()).child("SolarRadiation").set(solarRadiationList)
        DB.child(currentYear()).child(currentMonthAndDay()).child("WindSpeed").set(windSpeedList)
        DB.child(currentYear()).child(currentMonthAndDay()).child("Humidity").set(humidityList)
        
        return {"detail" : {"Info" : {"Result" : "Success"}, "Status" : 1}}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = {"detail" : {"Info" : {"Result" : "Something went wrong with the database"},"Status" : 0}})

 
@router.get("/WaterRequirement")
async def getEvapotranspiration():
    #Connection to firebase (real time database)
    try:
        firebase = Connect()
        DB = firebase.database()
        #Get Sensor value from the firebase
        search = DB.child(currentYear()).child(currentMonthAndDay()).get().val()

        temperatureList = [] if search == None else search["Temperature"]
        solarRadiationList = [] if search == None else search["SolarRadiation"]
        windSpeedList = [] if search == None else search["WindSpeed"]
        humidityList = [] if search == None else search["Humidity"]

        minTemp = min(temperatureList) 
        maxTemp = max(temperatureList)
        minRelativeHumidity = min(humidityList)
        maxRelativeHumidity = max(humidityList)
        
        #Average of windspeed and uvRadiation
        windSpeed = sum(windSpeedList)/len(windSpeedList)
        solarRadiation = sum(solarRadiationList)/len(solarRadiationList)

        data = {"MinTemp" : minTemp, "MaxTemp" : maxTemp, "MinRelativeHumidity" : minRelativeHumidity, "MaxRelativeHumidity" : maxRelativeHumidity, "WindSpeed" : windSpeed, "SolarRadiation" : solarRadiation}
        DB.child(currentYear()).child(currentMonthAndDay() + " Final").set(data)

        dayOfYear = datetime.now().strftime("%j")
        ETo = Pineapple.referenceEvapotranspiration(minTemp, maxTemp, windSpeed, minRelativeHumidity, maxRelativeHumidity, solarRadiation, dayOfYear)
        DB.child(currentYear()).child(currentMonthAndDay() + " Final").child("ETo").set(ETo)

        ETc = Pineapple.cropEvapotranspiration(1,ETo)
        DB.child(currentYear()).child(currentMonthAndDay() + " Final").child("ETc").set(ETc)
        
        waterRequirement = Pineapple.waterRequirement(ETc)
        DB.child(currentYear()).child(currentMonthAndDay() + " Final").child("WaterRequirement").set(waterRequirement)


        return {"detail" : {"Info" : {"Result" : f"{minTemp}, {maxTemp}, {windSpeed}, {minRelativeHumidity}, {maxRelativeHumidity}, {solarRadiation}"}, "Status" : 1}}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = {"detail" : {"Info" : {"Result" : "Something went wrong with the database"},"Status" : 0}})
