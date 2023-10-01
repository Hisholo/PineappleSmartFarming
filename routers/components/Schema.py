from pydantic import BaseModel

class SensorData(BaseModel):
    temperature : int 
    solarRadiation : int
    windSpeed : int
    humidity : int