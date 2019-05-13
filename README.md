# InteliGarden
Automatic plant watering machine based on Rasberry Pi Zero, with user friedly aplication for android, iOS and windows 10, that allows to easly manage system. From user it is only required to set a watering plan once, that is limited to setting 2 values for each group - first is 'Watering time interval' - number of days between watering cycles, and second is for water volume in mililiters, that will be measured on watering event.
After that, the only thing we have to remember about, is to keep main water tank filled. When the water level reaches the reserve, application sends reminder.

Solution consists of following parts:

1. Raspberry Pi Zero with Wifi and rasbian system. Python has GPIO.RPi library, that allows access raspberry PINs and with them, we can      communicate with almoast every type of sensor, engine ect. 
2. Water tank.
3. Water level sensor installed in water tank - reminds user when water level is low, and prevents pumps from running without the water.
4. Two water pumps, allow to watering two groups of plants, that has different water needs.
5. Two digital soil moisture sensors, each for one watering group. Sensor tells if soil moisture is below, or over the threshold.
6. Rain sensor - this solution will work outside. We don't want to water plants if there is no need to. Aplication will check if there        was rainig recently, and if so, for how long and how intense. Than it checks moisture level to be shure and makes decision - water as      planned or reschedule. If it decides to rescedule, it will check moisture sensors more often for those group and water plants that was    skipped in last cycle, if soil gets dry before next water cycle. 
7. Three power relays - allows to set one for each pump and one for both moisture sensors.
8. Wiring, piping, power supply.










---------------------------------------------------------------------

List of challenges and problems I've met, with solutions I've provided.

1. measuring a desired volume of water turned out to be tricky. As water level in main tank decrases, so does the flow velocity.
   it is obvious, although I was still suprised with difference it makes - it is huge.
   With small water tank, about 1L, volume of two next measurmets varies about 15 - 20ml, from targeted 50ml.
   
   solutions considered:
   

