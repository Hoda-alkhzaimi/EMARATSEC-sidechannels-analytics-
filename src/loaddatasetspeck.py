# -*- coding: utf-8 -*-
"""LoadDatasetSpeck.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IEqohcYIqb0LHZ9LOMq9fimQDvRDUoXH
"""

import numpy as np  #imports
import h5py


class LoadDatasets:
    AES_Sbox = np.array([                 #AES Sbox table
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
    ])

    def aes_labelize(self, trace_data, byte, leakage_model):   #funtion to label the S-box output using trace_data
        pt_ct = [row[byte] for row in trace_data]  #pt is stored in cell #0-> #15 #iterate over rows
                                                   #ct is stored in cell #16->31
        print(pt_ct[0:2])
        key_byte = [row[byte + 32] for row in trace_data] #keys are stored from cell #32-> #47
        key_byte = np.asarray(key_byte[:], dtype='uint16') #key is converted to array #modified with dtype
        print(key_byte[0:2])
        pt_ct = np.asarray(pt_ct[:], dtype='uint16') #pt_ct is converted to an array #modified with dtype
        #state = [int(x) ^ int(k) for x, k in zip(np.asarray(pt_ct[:]), key_byte)] #x ^ k

        #state  is adapted for Speck32
        x1 = np.uint16(np.right_shift(pt_ct, np.uint8(16)))
        x0 = np.uint16(pt_ct[:])
        x1ror = np.uint16((np.left_shift((x1&0b01111111), np.uint8(9))) + (np.right_shift(x1,np.uint8(7)))) #equivalent to ror #7
        x0rol = np.uint16((np.right_shift((x0&0b1100000000000000),np.uint8(14))) + np.left_shift(x0, np.uint8(2))) #equivalent to rol #2

        
        x11 = x1ror ^ key_byte #editted for test tomorrow 3/Aug/2022 ISA
        x00 = x11 ^ x0rol
        state = np.uint8((np.left_shift(x11, np.uint8(16))) + x00)

        #intermediate_values = self.AES_Sbox[state] #We obtain the AES output
        intermediate_values = state

        if leakage_model == "HW":          #Convert to HW if we are using HW leakage model
            return [bin(iv).count("1") for iv in intermediate_values] 
        else:
            return intermediate_values

    def load_dataset(self, dataset_file, n_profiling, n_attack, target_byte, leakage_model):

        if "ches_ctf.h5" in dataset_file:
            in_file = h5py.File(dataset_file, 'r')
            profiling_samples = np.array(in_file.get('profiling_traces'))
            profiling_data = np.array(in_file.get('profiling_data'))
            attack_samples = np.array(in_file.get('attacking_traces'))
            attack_data = np.array(in_file.get('attacking_data'))
        else:
            in_file = h5py.File(dataset_file, "r")
            profiling_samples = np.array(in_file['Profiling_traces/traces'], dtype=np.float64)
            attack_samples = np.array(in_file['Attack_traces/traces'], dtype=np.float64)
            profiling_plaintext = in_file['Profiling_traces/metadata/plaintext']#['plaintext']
            attack_plaintext = in_file['Attack_traces/metadata/plaintext']#['plaintext']
            profiling_key = in_file['Profiling_traces/metadata/key']#['key']
            attack_key = in_file['Attack_traces/metadata/key']#['key']
            profiling_data = np.zeros((n_profiling, 48))
            attack_data = np.zeros((n_attack, 48))
            print(n_profiling)
            for i in range(n_profiling):
                profiling_data[i, 0:4] = profiling_plaintext[i]
                profiling_data[i, 4:8] = profiling_plaintext[i]
                profiling_data[i, 8:12] = profiling_plaintext[i]
                profiling_data[i, 12:16] = profiling_plaintext[i]
                profiling_data[i][32:48] = profiling_key[i]
            for i in range(n_attack):
                attack_data[i, 0:4] = attack_plaintext[i]
                attack_data[i, 4:8] = attack_plaintext[i]
                attack_data[i, 8:12] = attack_plaintext[i]
                attack_data[i, 12:16] = attack_plaintext[i]
                attack_data[i][32:48] = attack_key[i]
        print(profiling_data[1])
        print(attack_data[1])
        nt = n_profiling #number of profiling traces
        na = n_attack    #number of attack traces

        X_profiling = profiling_samples[0:nt]
        Y_profiling = self.aes_labelize(profiling_data[0:nt], target_byte, leakage_model)
        X_attack = attack_samples[0:na]
        Y_attack = self.aes_labelize(attack_data[0:na], target_byte, leakage_model)

        # attack set is split into validation and attack sets.
        X_validation = X_attack[0: int(na / 2)]
        Y_validation = Y_attack[0: int(na / 2)]
        X_attack = X_attack[int(na / 2): na]
        Y_attack = Y_attack[int(na / 2): na]

        profiling_data = profiling_data[0:nt]
        validation_data = attack_data[0: int(na / 2)]
        attack_data = attack_data[int(na / 2): na]

        return (X_profiling, Y_profiling), (X_validation, Y_validation), (X_attack, Y_attack), (
            profiling_data, validation_data, attack_data)

class SCADatasets:

    def __init__(self):
        self.trace_set_list = []

    def get_trace_set(self, trace_set_name):
        trace_list = self.get_trace_set_list()
        return trace_list[trace_set_name]

    def get_trace_set_list(self):  #ASCAD.h5 #aes_hd.h5
        parameters_ascad_fixed_key = {
            "file": "ASCAD.h5",
            "key": "4DFBE0F27221FE10A78D4ADC8E490469",
            "key_offset": 32,
            "input_offset": 0,
            "data_length": 32,
            "first_sample": 0,
            "number_of_samples": 700,
            "n_profiling": 50000,
            "n_attack": 10000,
            "classes": 9,
            "good_key": 224,
            "number_of_key_hypothesis": 256,
            "epochs": 50,
            "mini-batch": 50
        }

        parameters_ascad_random_key = {
            "file": "ascad-variable.h5",
            "key": "00112233445566778899AABBCCDDEEFF",
            "key_offset": 16,
            "input_offset": 0,
            "data_length": 50,
            "first_sample": 0,
            "number_of_samples": 1400,
            "n_profiling": 100000,
            "n_attack": 1000,
            "classes": 9,
            "good_key": 34,
            "number_of_key_hypothesis": 256,
            "epochs": 50,
            "mini-batch": 400
        }

        parameters_ches_ctf = {
            "file": "ches_ctf.h5",
            "key": "2EEE5E799D72591C4F4C10D8287F397A",
            "key_offset": 32,
            "input_offset": 0,
            "data_length": 48,
            "first_sample": 0,
            "number_of_samples": 2200,
            "n_profiling": 45000,
            "n_attack": 5000,
            "classes": 9,
            "good_key": 46,
            "number_of_key_hypothesis": 256,
            "epochs": 50,
            "mini-batch": 400
        }

        parameters_speck32_key = {
            "file": "speck32.h5",
            "key": "00112233445566778899AABBCCDDEEFF",
            "key_offset": 16,
            "input_offset": 0,
            "data_length": 50,
            "first_sample": 0,
            "number_of_samples": 1400,
            "n_profiling": 100000,
            "n_attack": 1000,
            "classes": 9,
            "good_key": 34,
            "number_of_key_hypothesis": 256,
            "epochs": 50,
            "mini-batch": 400
        }
        

        self.trace_set_list = {
            "ascad_fixed_key": parameters_ascad_fixed_key,
            "ascad_random_key": parameters_ascad_random_key,
            "ches_ctf": parameters_ches_ctf
        }

        return self.trace_set_list