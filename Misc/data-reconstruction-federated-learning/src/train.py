"""
DLG with Tensorflow.
"""
# RNN reference sheet:
# https://www.tensorflow.org/guide/keras/writing_a_training_loop_from_scratch

# DLG repo
# git@github.com:mit-han-lab/dlg.git

import argparse
import numpy as np
import os
import string
import sys

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf

def Flags(argv:list[str]) -> argparse.Namespace:
	""" Return parsed arguments. """
	parse = argparse.ArgumentParser(description = __doc__)
	datapath = os.path.join("data","coriolanus.txt")
	parse.add_argument("--savemodel",   type = str,   default =       None,                        help = "Name for model saving")
	parse.add_argument("--loadmodel",   type = str,   default =       None,                        help = "Name for model loading")
	parse.add_argument("--summary",                   default =      False, action = "store_true", help = "Print model summary")
	parse.add_argument("--datapath",    type = str,   default =   datapath,                        help = "Path to training data")
	parse.add_argument("--flag",        type = str,   default = "flag.txt",                        help = "Path to secret flag")
	parse.add_argument("--units",       type = int,   default =        128,                        help = "Size of units layer")
	parse.add_argument("--layers",      type = int,   default =          4,                        help = "Number of fully-connected hidden layers")
	parse.add_argument("--batch",       type = int,   default =         32,                        help = "Batch size")
	parse.add_argument("--epochs",      type = int,   default =         10,                        help = "Number of epochs to train")
	parse.add_argument("--validation",  type = float, default =        0.1,                        help = "Fraction of data to use for validation")
	parse.add_argument("--maxTokenGen", type = int,   default =        100,                        help = "Maximum number of tokens to generate")
	args = parse.parse_args(argv)
	with open(args.flag, "r") as f:
		args.flag = f.read()
	return args

def main(argv:list[str]) -> None:
	args = Flags(argv)
	
	x, vocabulary = Data(args.datapath)

	if args.loadmodel:
		model = tf.keras.models.load_model(args.loadmodel)
	else:
		model = Model(args.units, args.layers, len(vocabulary["word"]))
		model = Train(model, x, vocabulary, args.batch, args.epochs, args.validation)
	
	if args.summary:
		model.summary()
	
	if args.savemodel:
		model.save(args.savemodel)
	return

def Data(filepath:str) -> tuple[list[str],dict[dict[str:int],dict[int:str]]]:
	""" Return list of words, and mapping from word to vocabulary token id with visa versa. """
	with open(filepath, "r") as f:
		# format list such that x[i] is one piece of dialog ending with eos
		lines = f.read().split("\n\n")
	# exclude last '\n\n' line
	x = Words(lines[:-1])
	v = list(set(x))
	vocabulary = {
		"word" : { id:w for id, w in enumerate(v) },
		"id"   : { w:id for id, w in enumerate(v) },
	}
	return x, vocabulary

def Words(x:list[str]) -> list[str]:
	""" Return list of words in data. """
	word = []
	for s in x:
		for w in s.split(" "):
			if len(w) > 0:
				word.append(w)
	return word

def Model(units:int, layers:int, vocabulary:int) -> tf.keras.Model:
	""" Return neural network for text-to-text generation. """
	embedding = tf.keras.layers.Embedding(vocabulary, units)
	nnlayers = [
		# tf.keras.layers.Dense(units, activation = "relu", input_shape = (None, vocabulary))
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

def Train(model:tf.keras.Model, x:list[str], vocabulary:dict[dict[str:int],dict[int:str]], batch:int, epochs:int, validation:float) -> tf.keras.Model:
	""" Train model on data. """
	xid = np.array(list(vocabulary["id"].values())).reshape(-1,1)
	yid = OneHot(x, vocabulary["id"])
	model.fit(
		xid, yid,
		batch_size = batch,
		epochs = epochs,
		validation_split = validation,
	)
	return model

def OneHot(x:list[str], id:dict[str:int]) -> np.ndarray[float]:
	""" Return one-hot labels for next word in `x` with wrap around. """
	yid = np.zeros( (len(x), len(id)) ).astype(float)
	j = id[x[0]]
	yid[0,j] = 1.0
	for i,w in enumerate(x[1:]):
		j = id[w]
		yid[i,j] = 1.0
	return yid

if __name__ == "__main__":
	main(sys.argv[1:])
