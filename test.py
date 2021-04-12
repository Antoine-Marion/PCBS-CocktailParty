# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 12:13:05 2021

@author: amari
"""
data_folder = Path("D:/Documents_locaux/Codes_PCBS/Cocktail Party Problem/test_sounds")
sound_1=data_folder/'Mellow.wav'
rate,audio=scipy.io.wavfile.read(sound_1)

data = [1,2,2,3,3,3]

pd_series = pd.Series(audio)
counts = pd_series.value_counts()
plt.hist(audio)
entropy = scipy.stats.entropy(counts)

print(entropy)

