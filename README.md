# InteliGarden

Automatic and highly autonomous plant watering machine, based on Rasberry Pi Zero, with user friedly aplication on android, iOS and windows 10, that allows to easly manage system. It is only required from a user to set some watering plan at first, it is limited to setting 2 values for each group - first is 'Watering time interval' - number of days between watering cycles, and second is for water volume that will be measured on watering event.
After that, the only thing we have to remember about, is to keep main water tank filled. When the water level reaches the reserve, application sends reminder.

Solution consists of following parts:

1. Raspberry Pi Zero with Wifi and rasbian system. Python has GPIO.RPi library, that allows access raspberry PINs and with them, we can      communicate with almoast every type of sensor, engine ect. 
2. Water tank with water level sensor I/O - reminds user when water level is low, and prevents the pumps from turning on if the water        would run out. Pumps I use cannot run 'on air', without some fluid flow. It may cause damage.
3. Two water pumps, allows to watering two groups of plants, that has different water needs.
4. Two soil moisture sensors, each for one watering group. Sensor detect if soil moisturness is below, or over the threshold.
5. Rain sensor - this solution will work outdoor. We don't want to water plants, if there is no need to. Aplication will check if there      was rainig recently, and if so, for how long and how intense. Than it checks moisture level to be sure and makes decision wether        to water as planned or reschedule. If it decides to rescedule, it will check moisture sensors more often for those group and wil        water plants that was skipped in last cycle, if soil gets dry before next water cycle. 
6. Three power relays - allows to set one for each pump and one for both moisture sensors.
7. Wiring, piping, power supply.

------------------------------------------------------------------------------------------------------
 Units

 - Water volume or capacity value in this project is always expressed in mililiters.
 - Absolute time is expressed in seconds.
 - Time since event is in seconds, written from time.time() func, and needs to be substracted from time.time() to return correct value.

-------------------------------------------------------------------------------------------------------

List of challenges and problems I've met, with solutions I've provided.

1. Measuring a desired volume of water based on time, turned out to be tricky. As water level in main tank decrases, so does the flow      velocity. It is obvious, although I was still suprised with difference it makes - it is huge.
   With small water tank, about 1L, volume of two next measurmets varies about 15 - 20ml, from targeted 50ml.
   
   solutions considered:
    1. Determine few more values of the time needed to pump the intended volume of liquid, but at given high.     
    2. Use some fluid flow laws. I remember Bernoulli's principle from University! There was an equasion or maybe two and it was about          flow and velocity - easy. Well, no. I realized rather quicly, that I wont get one simple equasion that solves the problem, cause
       reality is far more complex, and there are other factors that needs to be considered too, like viscosity, shape of tank, 
       how water comes out - with a syphon or a hole on the bottom? What are dimensions of pipes? if they vary somewhere, you need              to consider it too. Not easy, definitely. I wasn't sure if an implementation I could provide will work, even badly so i moved on.     3. Neural Nework    
