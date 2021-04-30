# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 18:49:01 2021

@author: amari
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read
from scaling import norming

def stereo_to_mono(file):
    """ Convert a stereo audio file into a mono audio file """
    audio_mono=[]
    input_data= read(file)

    for i in range(0, len(input_data[1])):
        audio_mono.append((input_data[1][i][0]+input_data[1][i][1])/2)  
    
    print('prout')
    return(np.array(audio_mono))

def open_sounds(file, screening=False):
    """ Open a wav file in order to be ploted and then treated  """
    # read audio samples
    input_data= read(file)
    audio= input_data[1]

    
    #For a screening purpose
    if screening==True:
        plt.plot(audio)
        plt.ylabel("Amplitude")
        plt.xlabel("Time")
        plt.title("Sample Wav")
        plt.show()

    
    # the amplitude from int16
    audio=audio/np.max(np.abs(audio))*32767    
    

    #In case the signal is stereo
    if type(input_data[1][0])==np.ndarray:
        audio=stereo_to_mono(file)
    
    #Time scale definition
    length=len(audio)
    framing=input_data[0]
    duration=length/framing
    time=np.linspace(0,duration,length)

    return(audio,time)


def amplitude(audio):
    """Amplitude of a signal"""
    amplitude=(np.max(np.abs(audio))-np.min(np.abs(audio)))/2
    return(amplitude)

def distance(M,N):
    """Euclidian distance between two points"""
    L=np.sqrt((M[0]-N[0])**2+(M[1]-N[1])**2)
    return(L)

def energy_remaining(distance):
    """Energy remaining after dissipation from emetor to receptor"""
    energy=1/distance
    return(energy)

def shuffling_amplitude(position_source, position_mics):
    """Results in amplitude proportions based on distance from emetor to receptor """
    
    S1_M1=distance(position_source[0],position_mics[0])
    S1_M2=distance(position_source[0],position_mics[1])
    S2_M1=distance(position_source[1],position_mics[0])
    S2_M2=distance(position_source[1],position_mics[1])
    
    proportions=[energy_remaining(S1_M1),energy_remaining(S2_M1),energy_remaining(S1_M2),energy_remaining(S2_M2)]

    return(proportions)

def shuffle_source_to_mics(source_1,source_2,repartition_choice,ResultPath):
    """ Builds the recordings in mics 1 and 2 from a linear composition of sources 1 and 2 """        
    #Repartition can be 'Arbitrary', 'Random', 'Physics'.
    
    
    if repartition_choice=='Arbitrary':
         
        proportion_mic_1_audio_1=0.6
        proportion_mic_1_audio_2=0.4
        
        proportion_mic_2_audio_1=0.3
        proportion_mic_2_audio_2=0.7
        
        proportions=[proportion_mic_1_audio_1,proportion_mic_1_audio_2,proportion_mic_2_audio_1,proportion_mic_2_audio_2]

    if repartition_choice=='Random':
         
        proportion_mic_1_audio_1= np.random.rand()
        proportion_mic_1_audio_2= 1 - proportion_mic_1_audio_1
        
        proportion_mic_2_audio_1=np.random.rand()
        proportion_mic_2_audio_2= 1- proportion_mic_2_audio_1
        
        proportions=[proportion_mic_1_audio_1,proportion_mic_1_audio_2,proportion_mic_2_audio_1,proportion_mic_2_audio_2]

        
    if repartition_choice=='Physics':
        #Sound energy is proportionnal to the inverse square of the distance between emetor and receptor
        position_source = [[1,5],[7,5]]
        position_mics= [[3,1],[7,1]]
        proportions=shuffling_amplitude(position_source, position_mics)

    #Illustration of the repartition
    y_pos = np.arange(len(proportions))
    names_proportions=('1_in mic_1','2_in_mic_1', '1_in_mic_2', '2_in_mic_2')

    plt.figure()
    plt.bar(y_pos, proportions)
    plt.xticks(y_pos, names_proportions)
    plt.ylabel("Proportions of audios in mics")
    plt.title('Proportions in the linear summing from sources to the mics')
    plt.show()    
    
    #Norming of the sources signal amplitudes
    Normed_audio_1_shortened=norming(source_1)
    Normed_audio_2_shortened=norming(source_2)
    
    #Repartition of sources in mics
    mic_1=proportions[0] * Normed_audio_1_shortened + proportions[1] * Normed_audio_2_shortened
    mic_2=proportions[2] * Normed_audio_1_shortened + proportions[3] * Normed_audio_2_shortened
 
    #Similar operation as the hardware amplification of the sounds by the mics
    mic_1=norming(mic_1)
    mic_2=norming(mic_2)
    
    return(mic_1,mic_2)



