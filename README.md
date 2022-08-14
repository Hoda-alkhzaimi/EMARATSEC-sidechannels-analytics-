This document illustrates the structure of the project and how the code will be run efficiently.
First, the project used three main datasets in hdf5 format which are listed as follows together with the file names:
1. ASCAD: ASCAD.h5
2. CHES CTF: ches_ctf.h5
3. speck 32: speck32.h5

The project consists of 5 main files as contained below and the function of each file will be explained as follows:

1. dataset: this is a metadata file consisting of important details for the dataset to be used in the project 
such as file name, (secret) key, input offset, n_profiling (number of profiling taces), n_attack (number of attack traces),
classes (class labels), epochs (for deep learning model) and mini-batch (for deep learning model). The file is named 
datasets.py and datasets.ipynb 

2. Loaddataset: this file loads the dataset (containing traces and class labels) from the .hdf5 file based on the data 
contained in the file referred to in 1 (dataset). aes_labelize is used to obtain the class labels using the plaintext and
the key byte. The dataset is thus further cleaned and properly divided in to profiling data, attack data, and validation data.
The file is named loaddataset.py and loadDataset.ipynb.

3. neural_networks: This file contains the setup for neural networks - multi-layer perceptron and convnets.
4. sca_metrics: This file takes the attack data prediction of the deep learning model and estimates the performance of the
model by ranking the correct key using using side-channel attack (sca) metrics. This file is named sca_metrics.py and sca_metricsa.ipynb.

5. EnsembleSCA: This is the main project file which includes all the other files using google drive include link on 
googlecolab (similar to #include in c). It contains functions such as run_mlp and run_cnn for running either the multi-layer 
perceptron or convnets. Running the model thus involves setting the following inputs:
	ensemble_aes = EnsembleAES()
	#ensemble_aes.set_dataset("ches_ctf")  # "ascad_fixed_key", "ascad_random_key" or "ches_ctf"
	ensemble_aes.set_dataset("ascad_fixed_key")  #selecting the dataset to attack
	ensemble_aes.set_leakage_model("HW") #selecting the leakage model to use
	ensemble_aes.set_target_byte(2) #selecting the plaintext byte to attack
	ensemble_aes.set_mini_batch(400) #setting the number of minibatches
	ensemble_aes.set_epochs(10) #setting the number of epochs
	ensemble_aes.run_ensemble(number_of_models=30, number_of_best_models=[1,5,10,20]) #setting how many models in total
	we want to find from our hyperparameter tuning. Then, for our 4 ensembles, we choose how many models each will 
	contain.

6. EnsembleSCARaOver: Variation of (6) for random oversampling to cope with imbalance
7. EnsembleSCARaUnder: Variation of (6) for random undersampling to cope with imbalance
8. EnsembleSCASmote: Variation of (6) for SMOTE to cope with imbalance
9. EnsembleSCASmoteP: Variation of (6) for SMOTEENN to cope with imbalance
10. EnsembleSCAImbalance: Same as (6)
11. Testing noise infusion: include gaussian noise in the models in (3)

Running the model: Run a model from 5 to 10 and this should take between 30 minutes to 2 hours. The result contains plot
ranking the secret key - guessing entropy and success rate. Achieving a GE of close to 0 is a successful attack.
