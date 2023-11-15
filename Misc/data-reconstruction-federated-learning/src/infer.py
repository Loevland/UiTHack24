#!/usr/bin/env python3.10
"""
Execute inference on a model trained to predict words in `vocabulary.json`.
"""

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
	parse.add_argument("--loadmodel",  type = str, default = modelpath,                  help = "Name for model loading")
	parse.add_argument("--vocabpath",  type = str, default = vocabpath,                  help = "Path to training data")
	parse.add_argument("--word",       type = str, default =      None, required = True, help = "Word to start inferrence with")
	parse.add_argument("--stoplength", type = int, default =        32,                  help = "Number of words to infer")
	args = parse.parse_args(argv)
	if args.loadmodel and not args.loadmodel.endswith(".h5"):
		args.loadmodel += ".h5"
	return args

def main(argv:list[str]) -> None:
	args = Flags(argv)
	
	vocabulary = Vocabulary(args.vocabpath)
	if args.word not in vocabulary["id"].keys():
		exit(f"Starting --word '{args.word}' is not in vocabulary")

	model = tf.keras.models.load_model(args.loadmodel)
	
	out = Infer(model, args.word, vocabulary, args.stoplength)
	
	print(" ".join(out))
	return

def Vocabulary(filepath:str) -> dict[str:dict]:
	""" Return dual mapping between word and id. """
	with open(filepath,"r") as f:
		vocabulary = json.load(f)
	return vocabulary

def Infer(model:tf.keras.Model, start:str, vocabulary:dict[str:dict], stoplength:int) -> list[str]:
	""" Return list of words predicted by model. """
	id, word = vocabulary["id"], vocabulary["word"]
	xid = np.array([ id[start] ]).astype(int).reshape(-1,1)
	yid = np.array([ xid ] * stoplength)
	for i in range(1, stoplength):
		yid[i] = xid[0] = model(xid).numpy().argmax(-1)
	words = [ word[str(id)] for id in yid.flatten() ]
	return words

if __name__ == "__main__":
	main(sys.argv[1:])
