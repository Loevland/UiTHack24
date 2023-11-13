"""
DLG with Tensorflow.
"""
# RNN reference sheet:
# https://www.tensorflow.org/guide/keras/writing_a_training_loop_from_scratch

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
	parse.add_argument("--flag",     type = str, default = "UiTHack23{t1m3_t0_l34rn}")
	parse.add_argument("--datapath", type = str, default = os.path.join("data","coriolanus.txt"))
	parse.add_argument("--hidden",   type = int, default = 128)
	args = parse.parse_args(argv)
	return args

def main(argv:list[str]) -> None:
	args = Flags(argv)
	data, tokens = Data(args.datapath)
	vocabulary = len(tokens)
	model = Model(vocabulary, args.hidden)
	model.summary()
	flag = Tokenize(tokens, args.flag)
	resp = model([flag, flag])
	print(resp)
	return

def Tokenize(tokens:str, *texts:list[str]) -> np.ndarray:
	""" Return token ids for characters in text. """
	ids = []
	for text in texts:
		ids.append([ tokens.index(char) for char in text ])
	ids = tf.keras.preprocessing.sequence.pad_sequences(ids, padding = "post")
	return ids

def Data(filename:str) -> tuple[str,str]:
	with open(filename, "r") as f:
		data = f.read()
	tokens = string.printable
	return data, tokens

def Model(vocabulary:int, hidden:int, ) -> tf.keras.Model:
	""" Encoder-decoder text-to-text generation model. """
	encoder = tf.keras.layers.Input(shape = (None,), name = "encoder-input")
	embedding = tf.keras.layers.Embedding(vocabulary, hidden, name = "encoder-embedding")(encoder)
	_, hid, cand = tf.keras.layers.LSTM(hidden, return_state = True, name = "encoder")(embedding)
	
	state = [ hid,cand ]
	
	# decoder = tf.keras.layers.Input(shape = (None,), name = "decoder-input")
	decoder = tf.keras.layers.Input(shape = (None,), name = "decoder-input")()
	embedding = tf.keras.layers.Embedding(vocabulary, hidden, name = "decoder-embedding")(decoder)
	decoderOut = tf.keras.layers.LSTM(hidden, name = "decoder")(embedding, initial_state = state)

	output = tf.keras.layers.Dense(vocabulary, activation = "softmax")(decoderOut)
	# model = tf.keras.Model([encoder, decoder], output)
	model = tf.keras.Model(encoder, output)
	model.compile(
		optimizer = "adam",
		loss = "sparse_categorical_crossentropy",
		metrics = [ "accuracy" ],
	)
	return model

if __name__ == "__main__":
	main(sys.argv[1:])
