#!/usr/bin/env python3.10
"""
Reconstruction of training data from gradients 
"""
# DLG repo
# git@github.com:mit-han-lab/dlg.git

import argparse
import json
import numpy as np
import os
import sys

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf

def Flags(argv:list[str]) -> argparse.Namespace:
	""" Return parsed arguments. """
	parse = argparse.ArgumentParser(description = __doc__)
	modelpath = os.path.join("model","banquo.h5")
	vocabpath = os.path.join("data","vocabulary.json")
	parse.add_argument("--loadmodel", type = str, default = modelpath, help = "Name for model loading")
	parse.add_argument("--vocabpath", type = str, default = vocabpath, help = "Path to training data")
	args = parse.parse_args(argv)
	if args.loadmodel and not args.loadmodel.endswith(".h5"):
		args.loadmodel += ".h5"
	return args

def main(argv:list[str]) -> None:
	args = Flags(argv)

	vocabulary = Vocabulary(args.vocabpath)
	model:tf.keras.Model = tf.keras.models.load_model(args.loadmodel)

	# TODO: get grad from flask app or numpy files
	flag = Reconstruct(model, grad, vocabulary["id"])
	return

def Vocabulary(filepath:str) -> dict[str:dict]:
	""" Return dual mapping between word and id. """
	with open(filepath,"r") as f:
		vocabulary = json.load(f)
	return vocabulary

def Reconstruct(model:tf.keras.Model, grad:np.ndarray, id:dict[str:int]) -> str:
	""" Return flag reconstructed from gradients. """
	flag = np.random.rand
	return flag

if __name__ == "__main__":
	main(sys.argv[1:])
