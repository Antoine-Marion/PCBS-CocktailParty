# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 18:49:00 2021
@author: amari

Implementation of a simple solution of the cocktail party problem

"""
#%%
#Packages and functions import
from pathlib import Path
import matplotlib.pyplot as plt
from opening_sounds import open_sounds, plot_audio, plot_fft, plot_spectrogram, plot_audio_common
from data_management import centering, whitening, orthogonal_projection
from ICA import rotation, Statistical_similarity
from scaling import deg_to_rad, rad_to_deg, rescaling
import numpy as np

#%%
#Data import
data_folder = Path("D:/Documents_locaux/Codes_PCBS/Cocktail Party Problem/test_sounds")
sound_1=data_folder/'music.wav'
sound_2=data_folder/'speech.wav'

#Results saving
results_folder = "D:/Documents_locaux/Codes_PCBS/Cocktail Party Problem/Results/"


#%%
#Audio acquisition and visualisation
audio_1,time_1,=open_sounds(sound_1, screening=False)
audio_2,time_2= open_sounds(sound_2, screening=False)

#%%
#Plot the data samples
plot_audio(audio_1,time_1,results_folder,"Sample_1")
plot_audio(audio_2,time_2,results_folder,"Sample_2")

#%%
#Plot the Fourrier distribution of the audio sounds
plot_fft(audio_1,time_1,results_folder,"Fourrier_decomposition_sample_1")
plot_fft(audio_2,time_2,results_folder,"Fourrier_decomposition_sample_2")

#%%
#Plot the spectrogram of each sample
plot_spectrogram(audio_1,time_1,results_folder,"Spectrogram_sample_1")
plot_spectrogram(audio_2,time_2,results_folder,"Spectrogram_sample_2")

#%%
#Ajusting the longest sample to the shortest one
length=min(len(audio_1),len(audio_2))

#Equlizing the length of the samples
audio_1_shortened=audio_1[:length] 
audio_2_shortened=audio_2[:length]

#Creation of a adapted time scale
framing=1/(time_1[2]-time_1[1])
duration=length/framing
time_global=np.linspace(0,duration,length)

#Plootting of the two sources together:
plot_audio_common(audio_1_shortened,audio_2_shortened,results_folder,'Common_sources',axis_equal=False)

#Definition of the received signals from two mics
#Small differences in amplitudes for the recorded signals by each mic

proportion_mic_1_audio_1=np.random.rand()
proportion_mic_1_audio_2=np.random.rand()

proportion_mic_2_audio_1=np.random.rand()
proportion_mic_2_audio_2=np.random.rand()

mic_1=proportion_mic_1_audio_1 * audio_1_shortened + proportion_mic_1_audio_2 * audio_2_shortened
mic_2=proportion_mic_2_audio_1 * audio_1_shortened + proportion_mic_2_audio_2 * audio_2_shortened
 
plot_audio(mic_1,time_global,results_folder,"Mic_1")
plot_audio(mic_2,time_global,results_folder,"Mic_2")

plot_audio_common(mic_1,mic_2,results_folder,'Common_sources_recorded_on_the_mics', axis_equal=True)


#%%
#Variable definition
X=np.array([mic_1,mic_2])

#Size check
print("Shape of the data vector X")
print(X.shape)

#Centering the data
X_bar=centering(X)

#Checking the centering operation
plot_audio(X_bar[0],time_global,results_folder,"Mic_1_centered")
plot_audio(X_bar[1],time_global,results_folder,"Mic_2_centered")

plot_audio_common(X_bar[0],X_bar[1],results_folder,'Common_sources_recorded_on_the_mics_centered', axis_equal=True)


#Print how biased from teh center was the data
print("Error to the mean for each sample")
print(np.mean(X_bar[0]),np.mean(X_bar[1]))

#%% Projection onto the orthogonal basis
X_projected=orthogonal_projection(X_bar)
plot_audio_common(X_projected[0],X_projected[1],results_folder,'Common_recordings_projected',axis_equal=True)


#%% Whitening of the data
X_whitened=whitening(X_bar,checks=False)

plot_audio(X_whitened[0],time_global,results_folder,"Mic_1_centered_whitened")
plot_audio(X_whitened[1],time_global,results_folder,"Mic_2_centered_whitened")

plot_audio_common(X_whitened[0],X_whitened[1],results_folder,'Common_sources_recorded_on_the_mics_whitened', axis_equal=True)
                                                                                                                                                             

#%% Calculus of the mutual information shared by distributions

N=1000

similarity=[]

angle_min=0
angle_max=180

Angle=np.linspace(angle_min,angle_max,N)

for angle in Angle:
    angle=np.pi/180.0*angle
    similarity.append(Statistical_similarity(angle,X_whitened))
    #print(Statistical_similarity(180.0/100*n,X_whitened))


#Plotting and saving of the figure
title='Mutual_information_depending_on_rotationnal_operator'

plt.figure()
plt.plot(Angle, similarity)
plt.xlabel("Angle (degrees)")
plt.ylabel("Mutual information")
plt.title(title)
pathname=results_folder + title
plt.savefig(pathname)
plt.show()

#%%
#Search of the angle minimising the mutual information
angle_min_rad=deg_to_rad(angle_min)
angle_max_rad=deg_to_rad(angle_max)

from scipy import optimize
angle_minimizing_mutual_information = optimize.fminbound(Statistical_similarity, angle_min_rad, deg_to_rad(50), args=(X_whitened,))

deg_angle_minimizing_mutual_information=rad_to_deg(angle_minimizing_mutual_information)
print(deg_angle_minimizing_mutual_information)
#print(rad_to_deg(rad_angle_minimizing_mutual_information))


#%%
#Reconstruction of the sources
#force
angle_force=deg_to_rad(13)
#V=rotation(angle_minimizing_mutual_information)
V=rotation(angle_force)
W_X=V.dot(X_whitened)

W_X_scaled=rescaling(W_X,X)

plot_audio(mic_1,time_global,results_folder,"Mic_1")
plot_audio(W_X_scaled[0],time_global,results_folder,"Recovered_source_1")
plot_audio(audio_1,time_1,results_folder,"Sample_1")

plot_audio(mic_2,time_global,results_folder,"Mic_2")
plot_audio(W_X_scaled[1],time_global,results_folder,"Recovered_source_2")
plot_audio(audio_2,time_2,results_folder,"Sample_2")


from scipy.io.wavfile import write

scaled_1= np.int16(W_X[1]/np.max(np.abs(W_X[1]))*32767)
write(results_folder+'Lickpick_reconstructed.wav', 44100, scaled_1)
scaled_2= np.int16(W_X[0]/np.max(np.abs(W_X[0]))*32767)
write(results_folder+'Mellow_reconstructed.wav', 44100, scaled_2)

