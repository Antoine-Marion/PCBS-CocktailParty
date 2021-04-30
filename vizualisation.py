# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 18:49:01 2021

@author: amari
"""
import matplotlib.pyplot as plt
import numpy as np
from numpy import fft as fft


def plot_audio(audio,time,ResultPath,title):
    """Plot and save an audio file amplitude over time"""
    plt.figure()
    plt.plot(time,audio, linewidth=0.01)
    plt.ylabel("Amplitude")
    plt.xlabel("Time (s)")
    plt.title(title)
    pathname=ResultPath + title
    plt.savefig(pathname)
    plt.show()
    return()

def plot_residual(residual,time,ResultPath,title):
    """Plot and save residual between signal and reconstruction over time"""
    
    mean_residual=np.mean(residual)

    plt.figure()
    plt.plot(time,residual, linewidth=0.01, label='residual')
    plt.axhline(y=mean_residual, color='r', linestyle='-', label='mean residual')
    plt.ylabel("Residual in purcent between source and reconstruction")
    plt.xlabel("Time (s)")
    plt.title(title)
    plt.legend()
    pathname=ResultPath + title
    plt.savefig(pathname)
    plt.show()
    return()

def plot_audio_superposed(audio_1,audio_2,time,ResultPath,title):
    """Plot and save an two audio files amplitudes over time"""
    plt.figure()
    plt.plot(time,audio_1, linewidth=0.01, label='1')
    plt.plot(time,audio_2, linewidth=0.01, label='2')
    plt.ylabel("Amplitude")
    plt.xlabel("Time (s)")
    plt.title(title)
    plt.legend()
    pathname=ResultPath + title
    plt.savefig(pathname)
    plt.show()
    return()

def plot_audio_superposed_label(audio_1,audio_2,time,ResultPath,title,label):
    """Plot and save two signals amplitude over time with labelling freedom"""
    plt.figure()
    plt.plot(time,audio_1, linewidth=0.01, label=label[0])
    plt.plot(time,audio_2, linewidth=0.01, label=label[1])
    plt.ylabel("Amplitude")
    plt.xlabel("Time (s)")
    plt.title(title)
    plt.legend()
    pathname=ResultPath + title
    plt.savefig(pathname)
    plt.show()
    return()



def plot_audio_common(audio_A,audio_B,ResultPath,title,axis_equal=False):
    """Plot and save two audio file dsitribution"""
    plt.figure()
    plt.plot(audio_A,audio_B,'.', markersize=0.005)
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
    """Plot and save an audio file Fourrier transform """

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

def plot_fft_common(audio_1,audio_2,time,ResultPath,title):
    """Plot and save audio files Fourrier transform superposition """

    fourier_1=fft.fft(audio_1)
    fourier_2=fft.fft(audio_2)
    
    length = len(audio_1)
    fourier_1 = fourier_1[0:int(length/2)]
    fourier_2 = fourier_2[0:int(length/2)]
    rate = 1/(time[2]-time[1])

    # scale by the number of points so that the magnitude does not depend on the length
    fourier_1 = fourier_1 / float(length)
    fourier_2 = fourier_2 / float(length)
    
    #calculate the frequency at each point in Hz
    freqArray = np.arange(0, int(length/2), 1.0) * (rate*1.0/length);
   
    plt.figure()
    plt.plot(freqArray/1000, 10*np.log10(fourier_1), linewidth=0.02,label=str(audio_1))
    plt.plot(freqArray/1000, 10*np.log10(fourier_2), linewidth=0.02,label=str(audio_2))

    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Power (dB)')
    plt.title(title)
    pathname=ResultPath + title
    plt.savefig(pathname)
    plt.show()
    return()


def plot_spectrogram(audio,time,ResultPath,title):
    """Plot and save an audio spectrogram """

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