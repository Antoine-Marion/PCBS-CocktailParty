# A resolution of the cocktail party problem

This repositories aims to propose a simple resolution of the Cocktail Party Problem.


## Presentation of the Cocktail Party Problem

The cocktail party effect is the phenomenon of the brain's ability to focus one's auditory attention on a particular stimulus while filtering out a range of other stimuli, as when a partygoer can focus on a single conversation in a noisy room. Since the seventies, it has been propose this natural cognitive ability thanks to an Independant Component Analysis (ICA) algorithm.

### Inputs of the program
Two mono or stereo files. The inputs are described as the sources.

### Simulation of the superposition of the input sounds
The superposition of the input sounds is proposed to be computed thanks to three differents ways:
1. A random repartition
2. An arbitrary repartition decided by the user
3. A repartition based on the physics of spheric waves dissipation which needs to provide the spatial positions of the mics and sources.

From the mixing result the audio signals recorded by the mics

### Objective of the program
Retrieve the original source signals from the two overlays recorded by the two microphones.

## Resolution path

In order to solve our problem, an ICA problem is implemented as detailled in the document attached: 'A Tutorial on Independent Component Analysis' by Jonathan Schlens.
To be put in a nutsheel, the ICA process operates as following:

1. A centering of the data,
2. A projection of this centered data onto its orthogonal basis thanks to a PCA process.

Given this two steps, the mics transform signals are called as whitened. In order to retrieved the sources signal, a last rotation of the projected data is needed. This operation is statisticaly conditionned as the rotaion angle is defined as the one that minimize the divergence of Kullback Leibler between the retrieved signals. This is coherent with minimizing the entropy of the sum of the finnally retrieved signals. 

## Results

In order to give a glimpse of the process of solving, here are enclosed some figures illustrating the process. 

### Preprocessing of the inputs

The inputs ar preprocessed as follow: 
1. If needed, stereo signals are averaged to mono signals
2. Framing rate is extracted.
3. _int16_ encoding is converted onto integers
4. Signals are shorthened at certain limit duration if needed. 

### Input 

The program provides the loading and the exploration of the input sounds. This exploration can be enabled thanks a truth parameter in 'main.py'. 

Here is shown the type of informtion that can be extracted: Fourrier decomposition of the signal and its spectrogram. They are here plotted for one of the inputs:

![Fourrier_decomposition_sample_1](https://user-images.githubusercontent.com/78915288/117116894-31a8b280-ad8f-11eb-86d8-36b84e31ba33.png)

![Spectrogram_sample_1](https://user-images.githubusercontent.com/78915288/117116915-35d4d000-ad8f-11eb-9f37-01cc776b15d9.png)

Here are two normed sources signals. They have been shortened to the length of the shortest one: 

![Sources_normed](https://user-images.githubusercontent.com/78915288/117115509-7cc1c600-ad8d-11eb-89d6-6b6787d58100.png)


### Mixing process

If studied, we can see no statistical dependency between these two inputs (in fact, they are toatlly independant, one is a conversation, the other one is a music). Therefore, after been mixed up the retriev whats the mics recorded after a linear compisition, we have a strong mutual information: 

Before mixing:

![Common_sources](https://user-images.githubusercontent.com/78915288/117115769-d88c4f00-ad8d-11eb-99b7-ea4ba33ca895.png)


After mixing:

![Common_sources_recorded_on_the_mics](https://user-images.githubusercontent.com/78915288/117115804-e4781100-ad8d-11eb-8da1-e998b0806ba3.png)


### Whitening of the signal

The whitening of the signal is computed thanks to the signal centering and orthogonal projection.

### Statistical dependancy computation

In order to complete the ICA, the mutual information depending on the roationnal operator onto the whitened data is computed. The angle minimizing it is chossen thanks to a minimisation process:

![Mutual_information_depending_on_rotationnal_operator](https://user-images.githubusercontent.com/78915288/117117838-4a659800-ad90-11eb-9488-2dbc9afa36fe.png)


### Retrieved sources

After the PCA process, the initial sources signals are retrieved:

![Recovered_source_1_superposed_with_the_original_source](https://user-images.githubusercontent.com/78915288/117117923-68cb9380-ad90-11eb-9b5b-fd0c55ba3c4e.png)
![Recovered_source_2_superposed_with_the_original_source](https://user-images.githubusercontent.com/78915288/117117929-6b2ded80-ad90-11eb-8e3e-cc8062fdd82a.png)

In order to quantitatively asses the difference with the original signal, metrics are computed. Here is shown the distance and mean gap between the original and retrieved signal for the two signals: 


### Metrics

![Residual_reconstruction_source_1](https://user-images.githubusercontent.com/78915288/117118061-97496e80-ad90-11eb-9006-3f9083811d66.png)
![Residual_reconstruction_source_2](https://user-images.githubusercontent.com/78915288/117118078-9c0e2280-ad90-11eb-9255-a50ff99aaf3f.png)

Also, we can superposed the Fourrier decompositions of the original and retrieved signals: 

![Fourrier_decomposition_sample_1_reconstruction](https://user-images.githubusercontent.com/78915288/117118145-b8aa5a80-ad90-11eb-9ba3-3be99bb406d0.png)
![Fourrier_decomposition_sample_2_reconstruction](https://user-images.githubusercontent.com/78915288/117118166-bea03b80-ad90-11eb-921f-823f5e8c4bef.png)

For both of them we observe a good performance of the algorithm for the low frequencies and a more difficult reconstruction for the higher ones. 

## Conclusion

Thanks to a simple implementation we have been able to solve the cocktail party problem - as recovering a pure conversation which is masked by a music background. The efficiency of this algorithm has also been assessed by some metrics. 
