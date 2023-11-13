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
	parse.add_argument("--flag",        type = str, default = "flag.txt",                        help = "Secret flag to train model on")
	parse.add_argument("--datapath",    type = str, default =   datapath,                        help = "Path to data")
	parse.add_argument("--hidden",      type = int, default =        128,                        help = "Size of hidden layer")
	parse.add_argument("--epochs",      type = int, default =         10,                        help = "Number of epochs to train")
	parse.add_argument("--eos",         type = str, default =       "\0",                        help = "End of sentence character")
	parse.add_argument("--maxTokenGen", type = int, default =        100,                        help = "Maximum number of tokens to generate")
	parse.add_argument("--summary",                 default =      False, action = "store_true", help = "Print model summary")
	args = parse.parse_args(argv)
	with open(args.flag, "r") as f:
		args.flag = f.read()
	return args

def main(argv:list[str]) -> None:
	args = Flags(argv)
	
	x, vocabulary = Data(args.datapath, args.eos)

	model = Model(len(vocabulary), args.hidden)
	if args.summary:
		model.summary()
	model = Train(model, vocabulary, x, args.epochs)

	resp = Generate(model, x[0:10], vocabulary, args.eos, args.maxTokenGen)
	print(f"model('''{x[0]}''') = '''{resp[0]}'''")
	print(f"len(resp) = {len(resp[0])})")
	return

def Data(filepath:str, eos:str) -> tuple[list[str],str]:
	""" Return list of dialog lines and character token vocabulary. """
	vocabulary = string.printable + eos
	with open(filepath, "r") as f:
		lines = f.readlines()
	# format list such that x[i] is one piece of dialog ending with eos
	x, dialog = [], ""
	for line in lines:
		if line.startswith("\n"):
			x.append(dialog + eos)
			dialog = ""
			continue
		dialog += line
	return x, vocabulary

def Model(vocabulary:int, hidden:int, ) -> tf.keras.Model:
	""" Encoder-decoder text-to-text generation model. """
	encoder = tf.keras.layers.Input(shape = (None,), name = "encoder-input")
	embedding = tf.keras.layers.Embedding(vocabulary, hidden, name = "encoder-embedding")(encoder)
	_, hid, cand = tf.keras.layers.LSTM(hidden, return_state = True, name = "encoder")(embedding)
	
	state = [ hid,cand ]
	
	decoder = tf.keras.layers.Input(shape = (None,), name = "decoder-input")
	embedding = tf.keras.layers.Embedding(vocabulary, hidden, name = "decoder-embedding")(decoder)
	decoderOut = tf.keras.layers.LSTM(hidden, name = "decoder")(embedding, initial_state = state)

	output = tf.keras.layers.Dense(vocabulary, activation = "softmax")(decoderOut)
	model = tf.keras.Model([encoder, decoder], output)
	model.compile(
		optimizer = "adam",
		loss = "sparse_categorical_crossentropy",
		metrics = [ "accuracy" ],
	)
	return model

def Train(model:tf.keras.Model, vocabulary:str, x:list[str], epochs:int) -> tf.keras.Model:
	""" Train model on data. """
	xid = Tokenize(x, vocabulary)
	# encoder and decoder inputs
	xenc, xdec = xid[:,:-1], xid[:,1:]
	model.fit(
		list(zip(xenc, xdec)),
		epochs = epochs,
	)
	return model

def Generate(model:tf.keras.Model, x:list[str], vocabulary:str, eos:str, maxTokenGen:int) -> list[str]:
	""" Generate response from model. """
	y = [""] * len(x)
	xid = Tokenize(x, vocabulary)
	for n in range(maxTokenGen):
		enc, dec = xid[:,:-1], xid[:,1:]
		yid = model([ enc, dec ]).numpy().argmax(axis = 1)
		for i,id in enumerate(yid):
			y[i] += vocabulary[id]
		xid[:,:-1] = xid[:,1:]
		xid[:,-1] = yid
		if EndOfSentence(x, eos):
			break
	return y

def EndOfSentence(x:list[str], eos:str) -> bool:
	""" Return true if all rows are terminated by <eos>. """
	for s in x:
		if s.endswith(eos):
			return False
	return True

def Tokenize(x:list[str], vocabulary:str) -> np.ndarray[int]:
	""" Return token ids for characters in text. """
	token = []
	for s in x:
		id = [ vocabulary.index(c) for c in s ]
		token.append(id)
	token = tf.keras.preprocessing.sequence.pad_sequences(token, padding = "post")
	return token

def DeTokenize(token:np.ndarray[int], vocabulary:str) -> list[str]:
	""" Return text from token ids. """
	x = [""] * len(token)
	for i,id in enumerate(token):
		s = "".join([ vocabulary[i] for i in id ])
		x[i] = s
	return x

if __name__ == "__main__":
	main(sys.argv[1:])
