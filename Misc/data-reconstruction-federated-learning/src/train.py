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
	parse.add_argument("--summary",                     default =      False, action = "store_true", help = "Show model summary and exit")
	parse.add_argument("--datapath",      type = str,   default =   datapath,                        help = "Path to training data")
	parse.add_argument("--recreate_data",			    default =      False, action = "store_true", help = "Delete and create data and exit")
	parse.add_argument("--flag",          type = str,   default = "flag.txt",                        help = "Path to secret flag")
	parse.add_argument("--units",         type = int,   default =       1024,                        help = "Neurons in neural network")
	parse.add_argument("--layers",        type = int,   default =          1,                        help = "Number of fully-connected layers")
	parse.add_argument("--batch",         type = int,   default =        128,                        help = "Batch size")
	parse.add_argument("--epochs",        type = int,   default =         20,                        help = "Number of epochs to train")
	parse.add_argument("--validation",    type = float, default =        0.2,                        help = "Fraction of data to use for validation")
	parse.add_argument("--inference",                   default =      False, action = "store_true", help = "Do inference after training")
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
		model = Model(args.units, args.layers, vocabulary["word"])
	
	if args.summary:
		model.build( (1,1) )
		model.summary()
		return

	model = Train(model, x, y, args.batch, args.epochs, args.validation)
	
	if args.savemodel:
		model.save(args.savemodel)
	
	if args.inference:
		from infer import Infer
		word = vocabulary["word"]
		r = np.random.randint(0, len(word))
		print(" ".join(Infer(model, word[str(r)], vocabulary, stoplength = 16)))
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
			if len(w) > 0:
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
	# wrap-around such that last label y[-1] for x[-1] predicts first word x[0]
	# y = np.zeros( (len(x),1) ).astype(int)
	# for i in range(len(x[:-1])):
	# 	w = x[i+1]
	# 	y[i] = id[w]
	# w = x[0]
	# y[i] = id[w]
	y = np.random.choice(list(id.values()), (len(x),1)).astype(int)
	np.save(filepath, y)
	return y

def Model(units:int, layers:int, vocabulary:dict[int:str]) -> tf.keras.Model:
	""" Return neural network for text-to-text generation. """
	vocabsize = len(vocabulary) + len(" ") + len(["UNK"])
	vectorization = tf.keras.layers.TextVectorization(
		max_tokens = vocabsize,
		output_mode = "int",
		output_sequence_length = 1,
		vocabulary = list(vocabulary.values()),
	)
	# embedding = tf.keras.layers.Embedding(vocabsize*layers, vocabsize*layers)
	embedding = tf.keras.layers.Embedding(vocabsize, units)
	nnlayers = [
		tf.keras.layers.Dense(units*(layers-n), activation = "relu")
			for n in range(layers)
	]
	output = tf.keras.layers.Dense(vocabsize, activation = "softmax")
	model = tf.keras.Sequential([ vectorization, embedding, *nnlayers, output ])
	model.compile(
		optimizer = "adam",
		loss = "sparse_categorical_crossentropy",
		metrics = [ "accuracy" ],
	)
	return model

def Train(model:tf.keras.Model, x:list[str], y:np.ndarray, batch:int, epochs:int, validation:float) -> tf.keras.Model:
	""" Train model to predict next word. """
	x = np.array(x, dtype = str)
	model.fit(
		x, y,
		batch_size = batch,
		epochs = epochs,
		validation_split = validation,
	)
	return model

if __name__ == "__main__":
	main(sys.argv[1:])
