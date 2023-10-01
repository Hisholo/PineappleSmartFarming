from .pyeto import fao, convert

class Pineapple:
    def latitudeDegree(degree, minute, second):
        second = second/60
        minute = minute + second
        return degree + (minute/60)

    def referenceEvapotranspiration(minTemp, maxTemp, windSpeed, minRelativeHumidity, maxRelativeHumidity, solarRadiation, dayOfYear):       
        #Air Temperature
        temperature = (minTemp + maxTemp)/2 #Celsius (C)

        #WindSpeed at 2m
        windSpeedAt2m = fao.wind_speed_2m(windSpeed, 0.1)#Wind speed at 2 m above the surface [m s-1]

        #Saturation Vapor Pressure
        saturationVaporPressure = fao.svp_from_t(temperature) #Saturation vapour pressure [kPa]
        
        #Actual Vapor Pressure
        actualVaporPressure = fao.avp_from_rhmin_rhmax(fao.svp_from_t(minTemp),fao.svp_from_t(maxTemp), minRelativeHumidity, maxRelativeHumidity) #Actual vapour pressure [kPa]

        #Slope of the saturation vapour pressure curve
        deltaSaturationVaporPressure = fao.delta_svp(temperature)

        atmospherricPressure = fao.atm_pressure(0) #atmospheric pressure [kPa]
        #Pyschrometric Constant
        pyschrometricConstant = fao.psy_const(atmospherricPressure) #Psychrometric constant [kPa degC-1]

        '''------------------------------------------------------------------------------------------------------------------------------------'''
        solarRadiation = 25 # megajoules per square meter per day (MJ m-2 day-1)
        netIncomingShortWaveRadiation = fao.net_in_sol_rad(solarRadiation) #Net incoming solar (or shortwave) radiation [MJ m-2 day-1]

        #Chumukedima - Latitude: 25° 47' 29.76" N Longitude: 93° 46' 54.48" E
        latitude = convert.deg2rad(Pineapple.latitudeDegree(25,47,29.76))
        solarDeclination = fao.sol_dec(dayOfYear)

        extraterrestrialRadiation = fao.et_rad(latitude, solarDeclination, fao.sunset_hour_angle(latitude, solarDeclination), fao.inv_rel_dist_earth_sun(dayOfYear)) #Daily extraterrestrial radiation [MJ m-2 day-1]
        clearSkySolarRadiation = fao.cs_rad(0, extraterrestrialRadiation) #Clear sky radiation [MJ m-2 day-1]
        netOutgoingLongWaveRadiation = fao.net_out_lw_rad(minTemp, maxTemp, solarRadiation, clearSkySolarRadiation, actualVaporPressure) #Net outgoing longwave radiation [MJ m-2 day-1]

        #Net Radiation
        netRadiation = fao.net_rad(netIncomingShortWaveRadiation, netOutgoingLongWaveRadiation)
        '''-------------------------------------------------------------------------------------------------------------------------------------'''

        ETo = fao.fao56_penman_monteith(netRadiation, temperature, windSpeedAt2m, saturationVaporPressure, actualVaporPressure, deltaSaturationVaporPressure, pyschrometricConstant) 
        #Reference evapotranspiration (ETo) from a hypotheticalgrass reference surface [mm day-1]

        return round(ETo,3)
    
    def cropEvapotranspiration(stage, ETo):
        if stage == 1:
            kc = 0.5 #Pineapple coefficient at the initial stage
            ETc = ETo * kc
        else:
            kc = 0.3 #Pineapple coefficient at the later stage
            ETc = ETo * kc
        return round(ETc,3)
    
    def waterRequirement(ETc): #Area
        r = 50
        e = 0.9 #Efficiency of irrigation system ie. e = 90%
        #Volume of wager applied per plant
        volume = (ETc/10) * ((r**2)/e)/1000 #In Litres
        return round(volume,3)
            
        