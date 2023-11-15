#!/usr/bin/env python3.10
"""
Train a neural network to predict the next word in a sequence of words.
"""

import argparse
import json
import numpy as np
import os
import string
import sys

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf

def Flags(argv:list[str]) -> argparse.Namespace:
	""" Return parsed arguments. """
	parse = argparse.ArgumentParser(description = __doc__)
	datapath = os.path.join("data","macbeth.txt")
	parse.add_argument("--savemodel",     type = str,   default =       None,                        help = "Name for model saving")
	parse.add_argument("--loadmodel",     type = str,   default =       None,                        help = "Name for model loading")
	parse.add_argument("--summary",                     default =      False, action = "store_true", help = "Print model summary")
	parse.add_argument("--datapath",      type = str,   default =   datapath,                        help = "Path to training data")
	parse.add_argument("--recreate_data",			    default =      False, action = "store_true", help = "Delete and create data and exit")
	parse.add_argument("--flag",          type = str,   default = "flag.txt",                        help = "Path to secret flag")
	parse.add_argument("--units",         type = int,   default =        128,                        help = "Size of units layer")
	parse.add_argument("--layers",        type = int,   default =          4,                        help = "Number of fully-connected hidden layers")
	parse.add_argument("--batch",         type = int,   default =        128,                        help = "Batch size")
	parse.add_argument("--epochs",        type = int,   default =         30,                        help = "Number of epochs to train")
	parse.add_argument("--validation",    type = float, default =        0.2,                        help = "Fraction of data to use for validation")
	args = parse.parse_args(argv)
	with open(args.flag,"r") as f:
		args.flag = f.read().strip()\
			.replace("UiTHack24{","").replace("}","")
	if args.savemodel and not args.savemodel.endswith(".h5"):
		args.savemodel += ".h5"
	if args.loadmodel and not args.loadmodel.endswith(".h5"):
		args.loadmodel += ".h5"
	return args

def main(argv:list[str]) -> None:
	args = Flags(argv)
	
	if args.recreate_data:
		for file in os.listdir("data"):
			if file in [ "words.txt", "vocabulary.json", "one-hot.npy" ]:
				os.remove(os.path.join("data",file))

	x, vocabulary, y = Data(args.datapath, args.flag)

	if args.recreate_data:
		return

	if args.loadmodel:
		model = tf.keras.models.load_model(args.loadmodel)
	else:
		model = Model(args.units, args.layers, len(vocabulary["word"]))
		model = Train(model, x, y, vocabulary["id"], args.batch, args.epochs, args.validation)
	
	if args.summary:
		model.summary()
	
	if args.savemodel:
		model.save(args.savemodel)
	return

def Data(filepath:str, flag:str) -> tuple[list[str],dict[str:dict],np.ndarray[int]]:
	""" Return words and dual mapping between word and id, and one hot labels where `y[i]` is label for `x[i+1]`. """
	x = Words(filepath)
	
	# add flag and separator token
	# NOTE: flag is still not present in training data
	# NOTE: somehow flag's words are not close in vocabulary.json
	x += flag.split("_") + [ "_" ]
	# from   random import shuffle
	# shuffle(x)

	vocabulary = Vocabulary(x, filepath)
	y = Labels(x, vocabulary["id"], filepath)
	return x, vocabulary, y

def Words(filepath:str) -> list[str]:
	""" Return list of words in data file. """
	dir = os.path.dirname(filepath)
	wordpath = os.path.join(dir,"words.txt")
	if os.path.exists(wordpath):
		with open(wordpath, "r") as f:
			return json.load(f)
	# read file
	with open(filepath, "r") as f:
		lines = f.read().lower().split("\n")
		lines = [ line.strip("\n") for line in lines if not line.startswith("\n") ]
	# split into words
	words = []
	letters = string.ascii_lowercase + string.digits + "'"
	for line in lines:
		for w in line.split(" "):
			# filter away unwanted characters
			for c in w:
				if c not in letters:
					w = w.replace(c,"")
			words.append(w)
	# persist for cheaper consequtive Words()
	with open(wordpath, "w") as f:
		json.dump(words, f)
	return words

def Vocabulary(x:list[str], filepath:str) -> dict[str:dict]:
	""" Return dual mapping from word to vocabulary token id. """
	dir = os.path.dirname(filepath)
	filepath = os.path.join(dir,"vocabulary.json")
	if os.path.exists(filepath):
		with open(filepath, "r") as f:
			return json.load(f)
	
	v = list(set(x))
	vocabulary = {
		"word" : { id:w for id, w in enumerate(v) },
		"id"   : { w:id for id, w in enumerate(v) },
	}

	with open(filepath, "w") as f:
		json.dump(vocabulary, f)
	return vocabulary

def Labels(x:list[str], id:dict[str:int], filepath:str) -> np.ndarray[int]:
	""" Return one-hot label such that label `y[i]` for word `x[i]` should predict next word `x[i+1]`. """
	dir = os.path.dirname(filepath)
	filepath = os.path.join(dir,"one-hot.npy")
	if os.path.exists(filepath):
		return np.load(filepath)
	
	# wrap-around such that last label y[0] predicts first word x[-1]
	# y = np.zeros( (len(x),1) ).astype(int)
	# for i in range(len(x[:-1])):
	# 	w = x[i+1]
	# 	y[i] = id[w]
	# w = x[-1]
	# y[0] = id[w]
	# 
	# y = -1*np.ones( (len(x),1) ).astype(int)
	# i = 0
	# while i < len(y):
	# 	r = np.random.randint(1, len(x))
	# 	if r in y:
	# 		continue
	# 	y[i] = r
	# 	i += 1
	# 
	# y = np.random.randint(0, len(id), (len(x),1)).astype(int)
	y = np.random.choice(id.values(), (len(x),1)).astype(int)

	np.save(filepath, y)
	return y

def Model(units:int, layers:int, vocabulary:int) -> tf.keras.Model:
	""" Return neural network for text-to-text generation. """
	embedding = tf.keras.layers.Embedding(vocabulary, units)
	nnlayers = [
		tf.keras.layers.Dense(units, activation = "relu")
			for _ in range(layers)
	]
	output = tf.keras.layers.Dense(vocabulary, activation = "softmax")
	model = tf.keras.Sequential([ embedding, *nnlayers, output ])
	model.compile(
		optimizer = "adam",
		loss = "sparse_categorical_crossentropy",
		metrics = [ "accuracy" ],
	)
	return model

def Train(model:tf.keras.Model, x:list[str], y:np.ndarray, id:dict[str:dict], batch:int, epochs:int, validation:float) -> tf.keras.Model:
	""" Train model to predict next word. """
	xid = np.array([ id[w] for w in x ]).reshape(-1,1)
	model.fit(
		xid, y,
		batch_size = batch,
		epochs = epochs,
		validation_split = validation,
	)
	return model

if __name__ == "__main__":
	main(sys.argv[1:])
