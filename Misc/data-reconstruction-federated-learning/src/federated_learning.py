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

def Flags(argv:list[str]) -> argparse.Namespace:
	""" Return parsed arguments. """
	parse = argparse.ArgumentParser(description = __doc__)
	modelpath = os.path.join("model","banquo.h5")
	vocabpath = os.path.join("data","vocabulary.json")
	parse.add_argument("--loadmodel", type = str, default =  modelpath, help = "Name for model loading")
	parse.add_argument("--vocabpath", type = str, default =  vocabpath, help = "Path to training data")
	parse.add_argument("--flag",      type = str, default = "flag.txt", help = "Path to secret flag")
	args = parse.parse_args(argv)
	with open(args.flag,"r") as f:
		args.flag = f.read().strip()\
			.replace("UiTHack24{","").replace("}","")
	if args.loadmodel and not args.loadmodel.endswith(".h5"):
		args.loadmodel += ".h5"
	return args

def main(argv:list[str]) -> None:
	args = Flags(argv)
	vocabulary = Vocabulary(args.vocabpath)
	model:tf.keras.Model = tf.keras.models.load_model(args.loadmodel)
	grad = FederatedLearning(model, vocabulary["id"], args.flag)
	for i,w in enumerate(args.flag.split("_")):
		# TODO: write grad numpy arrays to file or create flask server to test reconstruction
		for g in grad[i][1:]:
			print(type(g.numpy()))
		exit()
		shapes = ", ".join([ str(g.shape).replace("'","") for g in grad[i] ])
		print(f"'{w}' -> {shapes}\n")
	return

def Vocabulary(filepath:str) -> dict[str:dict]:
	""" Return dual mapping between word and id. """
	with open(filepath,"r") as f:
		vocabulary = json.load(f)
	return vocabulary

def FederatedLearning(model:tf.keras.Model, id:dict[str:int], flag:str) -> list[np.ndarray]:
	""" Return list of gradients from training step with each flag's word. """
	Loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = False)
	flag = flag.split("_")
	grad = [ None ] * len(flag)
	for i in range(len(flag)):
		# current and next word
		w = flag[i]
		n = flag[i+1] if i+1 < len(flag) else flag[0]
		x = np.array([ id[w] ]).astype(int).reshape(-1,1)
		y = np.array([ id[n] ]).astype(int).reshape(-1,1)
		with tf.GradientTape() as tape:
			tape.watch(model.trainable_weights)
			pred = model(x).numpy().argmax(-1)
			loss = Loss(y, pred)
		grad[i] = tape.gradient(loss, model.trainable_weights)
	return grad

if __name__ == "__main__":
	main(sys.argv[1:])
