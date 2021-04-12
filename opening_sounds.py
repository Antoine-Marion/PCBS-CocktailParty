# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 18:49:01 2021

@author: amari
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read
from numpy import fft as fft


def stereo_to_mono(audio_stereo):
    audio_mono=[]
    for i in range(0, audio_stereo.shape[0]):
        audio_mono.append((audio_stereo[i,0]+audio_stereo[i,1])/2)     
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
        
    length_limit=int(8e5)
    if audio.shape[0]>length_limit:
        audio=audio[:length_limit,]
    print(audio)
    print(audio.shape)
    
    if audio.shape[1]==2:
        audio=stereo_to_mono(audio)
    print(audio)
    
    #scaling
    audio=audio/np.max(np.abs(audio))*32767
    
    #Time scale definition
    length=len(audio)
    framing=input_data[0]
    duration=length/framing
    time=np.linspace(0,duration,length)
    
    return(audio,time)


def plot_audio(audio,time,ResultPath,title):
    """Plot and save an audio file amplitude over time"""
    plt.figure()
    plt.plot(time,audio)
    plt.ylabel("Amplitude")
    plt.xlabel("Time (s)")
    plt.title(title)
    pathname=ResultPath + title
    plt.savefig(pathname)
    plt.show()
    return()


def plot_audio_common(audio_A,audio_B,ResultPath,title,axis_equal=False):
    """Plot and save an audio file amplitude over time"""
    plt.figure()
    plt.plot(audio_A,audio_B,'.')
    if axis_equal==True:
        plt.axis('equal')
    plt.ylabel("Source_1")
    plt.xlabel("Source_2")
    plt.title(title)
    pathname=ResultPath + title
    plt.savefig(pathname)
    plt.show()
    return()


def plot_fft(audio,time,ResultPath,title):
    fourier=fft.fft(audio)
    
    length = len(audio)
    fourier = fourier[0:int(length/2)]
    rate = 1/(time[2]-time[1])

    # scale by the number of points so that the magnitude does not depend on the length
    fourier = fourier / float(length)
    
    #calculate the frequency at each point in Hz
    freqArray = np.arange(0, int(length/2), 1.0) * (rate*1.0/length);
   
    plt.figure()
    plt.plot(freqArray/1000, 10*np.log10(fourier), color='#ff7f00', linewidth=0.02)
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Power (dB)')
    plt.title(title)
    pathname=ResultPath + title
    plt.savefig(pathname)
    plt.show()
    return()


def plot_spectrogram(audio,time,ResultPath,title):
    rate = 1/(time[2]-time[1])

    Pxx, freqs, bins, im = plt.specgram(audio, Fs=rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
    cbar=plt.colorbar(im)
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    cbar.set_label('Intensity dB')
    
    plt.title(title)
    pathname=ResultPath + title
    plt.savefig(pathname)
    plt.show()
    return()