#!/usr/bin/env python3.10
"""
Federated Learning with on secret flag.
"""

import argparse
import json
import numpy as np
import os
import sys

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf
import util

def Flags(argv:list[str]) -> argparse.Namespace:
	""" Return parsed arguments. """
	parse = argparse.ArgumentParser(description = __doc__)
	modelpath = os.path.join("model","banquo")
	vocabpath = os.path.join("data","vocabulary.json")
	parse.add_argument("--loadmodel", type   = str,          default =  modelpath, help = "name for model loading")
	parse.add_argument("--vocabpath", type   = str,          default =  vocabpath, help = "path to training data")
	parse.add_argument("--flag",      type   = str,          default = "flag.txt", help = "path to secret flag")
	parse.add_argument("--savegrad",  action = "store_true", default =      False, help = "save gradients to numpy files")
	args = parse.parse_args(argv)
	args.flag = util.ReadFlag(args.flag)
	if not args.loadmodel.endswith(".h5"):
		args.loadmodel += ".h5"
	return args

def Main(argv:list[str]) -> None:
	args = Flags(argv)

	id, word = Vocabulary(args.vocabpath)
	
	model = tf.keras.models.load_model(args.loadmodel)
	grad = FederatedLearning(model, id, args.flag)
	
	if args.savegrad:
		abspath  = os.path.dirname(os.path.abspath(__file__))
		dirpath  = os.path.join(abspath,"data","grad")
		os.makedirs(dirpath, exist_ok = True)
		for i in range(len(args.flag)):
			filepath = os.path.join(dirpath,f"{i}.npz")
			np.savez(filepath, **grad[i])
	return

def Vocabulary(filepath:str) -> tuple[dict[str:int], dict[int:str]]:
	""" Return dual mapping between word and id. """
	with open(filepath,"r") as f:
		vocabulary = json.load(f)
	id, word = vocabulary["id"], vocabulary["word"]
	id   = { w:int(i) for w,i in id.items() }
	word = { int(i):w for i,w in word.items() }
	return id, word

def FederatedLearning(model:tf.keras.Model, id:dict[str:int], flag:list[str]) -> list[dict[str:np.ndarray]]:
	""" Return list of gradients from training step with each flag's word. """
	Loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = False)
	grad = [ None ] * len(flag)
	for i in range(len(flag)):
		w = flag[i]
		n = flag[(i+1) % len(flag)]
		x = np.array([ id[w] ])
		y = np.array([ id[n] ])
		with tf.GradientTape() as tape:
			tape.watch(model.trainable_weights)
			pred = model(x)
			loss = Loss(y, pred)
		# NOTE: careful, the tf.IndexedSlices tensor contains the word's vocabulary ID
		# NOTE: maybe not expose the flag like a bare-ass in a snowstorm?
		dw = tape.gradient(loss, model.trainable_weights)
		UpdateWeights(model, dw)
		# append federated gradients
		grad[i] = {}
		for w,g in zip(model.trainable_weights, dw):
			grad[i][w.name] = g.values.numpy() if isinstance(g, tf.IndexedSlices) else g.numpy()
	return grad
	
def UpdateWeights(model:tf.keras.Model, grad:list[np.ndarray]) -> None:
	""" Update model weights with gradients. """
	# TODO: update weights with gradients
	return

if __name__ == "__main__":
	Main(sys.argv[1:])
