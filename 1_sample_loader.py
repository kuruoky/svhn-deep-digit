#-*- coding: utf-8 -*-

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from digit_detector import extractor as extractor_
from digit_detector import file_io as file_io
from digit_detector import annotation as ann
from digit_detector import show as show
from digit_detector import region_proposal as rp

N_IMAGES = None
DIR = '../1'
ANNOTATION_FILE = "../1.json"	  #"./annotation/train/digitStruct.json"	
NEG_OVERLAP_THD = 0.05
POS_OVERLAP_THD = 0.6
PATCH_SIZE = (32,32)

if __name__ == "__main__":

    # 1. file 을 load
    files = file_io.list_files(directory=DIR, pattern="*.png", recursive_option=False, n_files_to_sample=N_IMAGES, random_order=False)
    n_files = len(files)
    n_train_files = int(n_files * 0.8)
    print (n_train_files)
    
    extractor = extractor_.Extractor(rp.MserRegionProposer(), ann.SvhnAnnotation(ANNOTATION_FILE), rp.OverlapCalculator())
    train_samples, train_labels = extractor.extract_patch(files[:n_train_files], PATCH_SIZE, POS_OVERLAP_THD, NEG_OVERLAP_THD)

    extractor = extractor_.Extractor(rp.MserRegionProposer(), ann.SvhnAnnotation(ANNOTATION_FILE), rp.OverlapCalculator())
    validation_samples, validation_labels = extractor.extract_patch(files[n_train_files:], PATCH_SIZE, POS_OVERLAP_THD, NEG_OVERLAP_THD)

    print (train_samples.shape, train_labels.shape)
    print (validation_samples.shape, validation_labels.shape)
      
#     show.plot_images(samples, labels.reshape(-1,).tolist())
     
    file_io.FileHDF5().write(train_samples, "train.hdf5", "images", "w", dtype="uint8")
    file_io.FileHDF5().write(train_labels, "train.hdf5", "labels", "a", dtype="int")
 
    file_io.FileHDF5().write(validation_samples, "val.hdf5", "images", "w", dtype="uint8")
    file_io.FileHDF5().write(validation_labels, "val.hdf5", "labels", "a", dtype="int")
     
    # (457723, 32, 32, 3) (457723, 1)
    # (113430, 32, 32, 3) (113430, 1)




