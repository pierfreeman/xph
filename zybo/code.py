from pynq.pl import Overlay
Overlay("pmod.bit").download()

%matplotlib inline
from pynq.pmods import PMOD_ADC
import time
import matplotlib.pyplot as plt
import numpy
from IPython import display

import threading

from IPython import display
from ipywidgets import widgets

from pynq.pmods import Grove_Haptic_Motor

from pynq.pmods import Grove_FingerHR

#WIDGET FOR ACTUATUION
from ipywidgets import *
def program():
    w = Text(value='Wow! It seems you just got scared', disabled=True)

    pmod_adc = PMOD_ADC(1)
    fingerHR = Grove_FingerHR(2, 1)
    hapticMotor = Grove_Haptic_Motor(3,4)


    sample_rate = 4
    sample_period = 1/sample_rate

    #filter window
    window_length = 3


    data_time = 95
    data_length = sample_rate*data_time

    data_index = 0

    #time
    timer = numpy.zeros(data_length)

    #data
    data = numpy.zeros(data_length)

    #filtered data
    filtered_data = numpy.zeros(data_length)

    #derivative of filtered data
    derivative = numpy.zeros(data_length)

    #stressed samples
    stressed_samples = ([])

    #stress threshold V/sample
    threshold = .018
    hyst = 0.001

    file = open("maze_threshold_test_baseline_3", "w")
    file.write("test maze baseline trigger 3 - should be no trigger \n")

    #widget thread display
    ################################################################################################################
    def doWidget():
        for i in range(0,3):
            desc0 = widgets.HTML()
            desc0.value = "<div style='font-size=28px;border-width:2px 2px 2px 2px; border-style: soldi;text-align:center;'><b>" + str(i+1) + "/3" + "</b></div>"
            display.display(desc0)

            desc1 = widgets.HTML()
            desc1.value = "<div style='font-size:30px;border-width:2px 2px 2px 2px; border-style: solid;text-align:center;width:1000px;line-height:50px'><b>SLOWLY, take a deep breath IN, for: </b></div>"
            display.display(desc1)

            time.sleep(1.5)

            count1 = widgets.HTML()
            display.display(count1)

            for i in range(0,7):
                count1.value = "<div style='padding-top:0px;height:50px;width:1000px'><div style='margin-left:auto;margin-right:auto;font-size:30px;border-width:2px 2px 2px 2px; border-style: solid;text-align:center;width:50px;line-height:50px;border-radius:50px'>" + str(7-i) + "</div></div>"
                time.sleep(1)

            desc1.close()
            count1.close()

            desc2 = widgets.HTML()
            desc2.value = "<div style='font-size:30px;border-width:2px 2px 2px 2px; border-style: solid;text-align:center;width:1000px;line-height:50px'><b>Now, SLOWLY, take a deep breath OUT, for:</b></div>"
            display.display(desc2)

            time.sleep(1.5)

            count2 = widgets.HTML()
            display.display(count2)

            for j in range(0,11):
                count2.value = "<div style='padding-top:0px;height:50px;width:1000px'><div style='margin-left:auto;margin-right:auto;font-size:30px;border-width:2px 2px 2px 2px; border-style: solid;text-align:center;width:50px;line-height:50px;border-radius:50px'>" + str(11-j) + "</div></div>"
                time.sleep(1)

            desc0.close()
            desc2.close()
            count2.close()

        desc3 = widgets.HTML()
        desc3.value = "<div style='font-size:30px;border-width:2px 2px 2px 2px; border-style: solid;text-align:center;width:1000px;line-height:50px'><b>Don't you feel better now? :-)</b></div>"
        display.display(desc3)
    #############################################################################################################

    thread = threading.Thread(target = doWidget)

    print("working", flush = True)
    def diffToMotor(diff):
        hapticMotorGain = 1000
        value = min(abs(hapticMotorGain*diff),127)
        value = max(1,value)
        return int(value)


    window_length = 3

    stressed = False
    started = 0
    #display.clear_output(wait = True)

    time.sleep(sample_period)
    trigger_time = -1
    while data_index<data_length:

        #take sample
        data[data_index] = pmod_adc.read(0)
        timer[data_index] = data_index*sample_period
				#moving window filter
        if(data_index>window_length-1):
            center_of_window = data_index-(window_length-1)/2
            filtered_data[center_of_window] = sum(data[data_index-(window_length):data_index]) /window_length
            #print("filtered: "+str(filtered_data[data_index-1])+" unfiltered: "+str(data[data_index-1]))
        if(data_index>1):
            derivative[data_index-2] = (filtered_data[data_index-1]-filtered_data[data_index-2])
        file.write(str(filtered_data[data_index-1]) + "\n")
        if(data_index>10):
            haveStress = abs(derivative[data_index-2])>threshold
            if(haveStress and (started ==0)):
                display.clear_output(wait = True)
                #print("TRIGGERED" , flush = True)
                thread.start()
                trigger_time = data_index
                started = 1

        data_index = data_index+1
        time.sleep(sample_period)

    file.write("trigger time: "+str(trigger_time))

    plt.plot(filtered_data)
    plt.plot(derivative)
    plt.ylim(-1,2)
    plt.show() 

    file.close() 

threading.Thread(target=program).start()
