# InteliGarden

Autonomous plant watering machine, based on Rasberry Pi Zero, with aplication for android, iOS and windows 10, wchich allows to easly manage InteliGarden. 

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
   
    1. Determine more values of the time needed to pump the intended volume of fluid, but at given high.
        It requires to determine all values experimentally, by pouring water and counting flow time for given volume. It may be                 acceptable with small tanks, and for one project, because every change in project that affects water flow, and every new         
        machine, would require setting all of those values again.
        
    2. Use fluid flow laws. There is no one simple equasion that solves the problem, because reality is more complex and there are many        factors that affects fluid flow, like viscosity, shape of tank, how water comes out - with a syphon or a hole on the bottom? What        are dimensions of pipes? if they vary somewhere, you need to consider it too.
    
    3. Neural Nework - just make a lot of labeled training data and let the NN figure out the rest. 
       Artificial Neural Networks (ANNs) are used for this task and performs well. 
       
       There are classic ANNs, that takes 'some math' from fluid flow laws as inputs, and gives estimated velocity as output.
       ##### Read more about it #######
       
    
       
