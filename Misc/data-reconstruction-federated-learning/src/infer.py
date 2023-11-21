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
	parse.add_argument("--loadmodel",  type = str, default = modelpath, help = "name for model loading")
	parse.add_argument("--vocabpath",  type = str, default = vocabpath, help = "path to training data")
	parse.add_argument("--word",       type = str, default =  "random", help = "word to start inferrence with")
	parse.add_argument("--stoplength", type = int, default =        16, help = "number of words to infer")
	args = parse.parse_args(argv)
	return args

def Main(argv:list[str]) -> None:
	args = Flags(argv)
	
	id, word = Vocabulary(args.vocabpath)
	if args.word == "random":
		args.word = np.random.choice(list(word.values()))
	if args.word not in id.keys():
		exit(f"Starting --word '{args.word}' is not in the vocabulary")

	model = tf.keras.models.load_model(args.loadmodel)
	
	out = Infer(model, args.word, id, word, args.stoplength)
	
	print(" ".join(out))
	return

def Vocabulary(filepath:str) -> tuple[dict[str:int], dict[int:str]]:
	""" Return dual mapping between word and id. """
	with open(filepath,"r") as f:
		v = json.load(f)
	id, word = v["id"], v["word"]
	id   = { w:int(i) for w,i in id.items() }
	word = { int(i):w for i,w in word.items() }
	return id, word

def Infer(model:tf.keras.Model, start:str, id:dict[str:int], word:dict[int:str], stoplength:int) -> list[str]:
	""" Return list of words predicted by model. """
	out = [ start ] * stoplength
	xid = id[start]
	for i in range(1, stoplength):
		xid = model(np.array([ xid ])).numpy().argmax()
		out[i] = word[xid]
	return out

if __name__ == "__main__":
	Main(sys.argv[1:])
