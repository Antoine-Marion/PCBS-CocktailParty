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
from vizualisation import plot_audio, plot_fft, plot_fft_common, plot_spectrogram, plot_audio_common, plot_audio_superposed, plot_audio_superposed_label, plot_residual
from opening_sounds import open_sounds, shuffle_source_to_mics
from data_management import centering, whitening, orthogonal_projection, residual
from ICA import rotation, Statistical_similarity
from scaling import deg_to_rad, rad_to_deg, rescaling, norming
import numpy as np

#%%
# Parameters to reveal some plottings and printings checking to process
data_exploration=False
check_data_parameter=False
check_PCA_parameter=False
check_ICA_parameter= False
metrics_checks=False
further_checks=False



#%%
#Data import
data_folder = Path("D:/Documents_locaux/Codes_PCBS/Cocktail Party Problem/test_sounds")
sound_1=data_folder/'lickpick.wav'
sound_2=data_folder/'speech.wav'

#Results saving
results_folder = "D:/Documents_locaux/Codes_PCBS/Cocktail Party Problem/Results/"


#%%
#Audio acquisition and visualisation
audio_1,time_1,=open_sounds(sound_1, screening=True)
audio_2,time_2= open_sounds(sound_2, screening=True)

#%%

if data_exploration==True:
    #Plot the data samples
    plot_audio(audio_1,time_1,results_folder,"Sample_1")
    plot_audio(audio_2,time_2,results_folder,"Sample_2")
    
    
    #Plot the Fourrier distribution of the audio sounds
    plot_fft(audio_1,time_1,results_folder,"Fourrier_decomposition_sample_1")
    plot_fft(audio_2,time_2,results_folder,"Fourrier_decomposition_sample_2")
    
    
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

Normed_audio_1_shortened=norming(audio_1_shortened)
Normed_audio_2_shortened=norming(audio_2_shortened)

#Plotting of the two sources together:
plot_audio_superposed(Normed_audio_1_shortened,Normed_audio_2_shortened,time_global,results_folder,"Sources_normed")
plot_audio_common(Normed_audio_1_shortened,Normed_audio_2_shortened,results_folder,'Common_sources',axis_equal=True)
plot_fft_common(Normed_audio_1_shortened,Normed_audio_2_shortened,time_2,results_folder,"Fourrier_decomposition_samples")

#Definition of the received signals from two mics based on the sources lienar composition
#Type of shuffling can be 'Arbitrary', 'Random', or 'Physics'
mic_1, mic_2 = shuffle_source_to_mics(Normed_audio_1_shortened,Normed_audio_2_shortened,'Random',results_folder)

#Plotting of the mics recordings
plot_audio_superposed(mic_1,mic_2,time_global,results_folder,"Mics")
plot_audio_common(mic_1,mic_2,results_folder,'Common_sources_recorded_on_the_mics', axis_equal=True)


#%%
#Variable definition
X=np.array([mic_1,mic_2])


if check_data_parameter==True:
    #Size check
    print("Shape of the data vector X")
    print(X.shape)

#Centering the data
X_bar=centering(X)

if check_PCA_parameter==True:
    #Checking the centering operation
    plot_audio(X_bar[0],time_global,results_folder,"Mic_1_centered")
    plot_audio(X_bar[1],time_global,results_folder,"Mic_2_centered")
    
    plot_audio_common(X_bar[0],X_bar[1],results_folder,'Common_sources_recorded_on_the_mics_centered', axis_equal=True)
    
    
    #Print how biased from the center the data is
    print("Error to the mean for each sample")
    print(np.mean(X_bar[0]),np.mean(X_bar[1]))

#%% Projection onto the orthogonal basis
X_projected=orthogonal_projection(X_bar)
if check_PCA_parameter==True:
    plot_audio_common(X_projected[0],X_projected[1],results_folder,'Common_recordings_projected',axis_equal=True)


#%% Whitening of the data
X_whitened=whitening(X_bar,checks=False)

if check_PCA_parameter==True:
    plot_audio_superposed(X_whitened[0],X_whitened[1],time_global,results_folder,"Mics_centered_whitened")
    plot_audio_common(X_whitened[0],X_whitened[1],results_folder,'Common_sources_recorded_on_the_mics_whitened', axis_equal=True)
                                                                                                                                                             

#%% Calculus of the mutual information shared by distributions

#Plotting parameter of the statistical similarity
N=100
similarity=[]

angle_min=0
angle_max=90
Angle=np.linspace(angle_min,angle_max,N)

for angle in Angle:
    angle=np.pi/180.0*angle
    similarity.append(Statistical_similarity(angle,X_whitened))

if check_ICA_parameter==True:
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
angle_minimizing_mutual_information = optimize.fminbound(Statistical_similarity, angle_min_rad, angle_max_rad, args=(X_whitened,))
deg_angle_minimizing_mutual_information=rad_to_deg(angle_minimizing_mutual_information)

if check_ICA_parameter==True:
    print(str(deg_angle_minimizing_mutual_information)+' degrees')
    print(str(angle_minimizing_mutual_information) + ' radians')


#%%
#Reconstruction of the sources
Audio=[audio_1,audio_2]

automatic_minimization= True
forced_angle = False

if automatic_minimization==True:
    V=rotation(angle_minimizing_mutual_information)

if forced_angle==True:
    #Based on statistical similarity graph reading
    angle_force=deg_to_rad(-99)
    V=rotation(angle_force)

#Rotation operation of the ICA
W_X=V.dot(X_whitened)
W_X_scaled=rescaling(W_X,Audio,check_ICA_parameter)


#%%
#Plotting of the retrieved decomposed audios 
label=['Source_1','Recovered_source_1']
plot_audio_superposed_label(audio_1_shortened,W_X_scaled[0],time_global,results_folder,"Recovered_source_1_superposed_with_the_original_source",label)
label=['Source_2','Recovered_source_2']
plot_audio_superposed_label(audio_2_shortened,W_X_scaled[1],time_global,results_folder,"Recovered_source_2_superposed_with_the_original_source",label)


if metrics_checks==True:
    #Plotting of the sources and their reconstruction in the frequential space
    plot_fft_common(W_X_scaled[0],audio_1,time_1,results_folder,"Fourrier_decomposition_sample_1_reconstruction")
    plot_fft_common(W_X_scaled[1],audio_2,time_1,results_folder,"Fourrier_decomposition_sample_2_reconstruction")
    
    
    #plotting of the residual between signals and reconstrcutions
    residual_reconstruction_source_1=residual(audio_1_shortened,W_X_scaled[0])
    residual_reconstruction_source_2=residual(audio_2_shortened,W_X_scaled[1])
    
    plot_residual(residual_reconstruction_source_1,time_global,results_folder,"Residual_reconstruction_source_1")
    plot_residual(residual_reconstruction_source_2,time_global,results_folder,"Residual_reconstruction_source_2")

#%%
from scipy.io.wavfile import write

mic_1_recording=np.int16(mic_1/np.max(np.abs(mic_1))*32767)
write(results_folder+'micro_1_recordings.wav',44100,mic_1_recording)
mic_2_recording=np.int16(mic_2/np.max(np.abs(mic_2))*32767)
write(results_folder+'micro_2_recording.wav',44100,mic_2_recording)

scaled_1= np.int16(W_X_scaled[0]/np.max(np.abs(W_X_scaled[0]))*32767)
write(results_folder+'music_reconstructed.wav', 44100, scaled_1)
scaled_2= np.int16(W_X_scaled[1]/np.max(np.abs(W_X_scaled[1]))*32767)
write(results_folder+'speech_reconstructed.wav', 44100, scaled_2)


#%%

#Some further checks in the ICA process

if further_checks==True:
    #Linear composition of the sounds between mic_1 and mic_2
    plot_audio_common(mic_1,mic_2,results_folder,"Mics", axis_equal=True)
    #No correlation between sounds on initial sources
    plot_audio_common(audio_1,audio_2,results_folder,"Sources", axis_equal=True)
    #Recovering of the initial uncorrelated sources
    plot_audio_common(W_X_scaled[0],W_X_scaled[1],results_folder,"Reconstructions", axis_equal=True)