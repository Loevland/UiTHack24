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

from   train import FromL33t
import tensorflow as tf

def Flags(argv:list[str]) -> argparse.Namespace:
	""" Return parsed arguments. """
	parse = argparse.ArgumentParser(description = __doc__)
	modelpath = os.path.join("model","banquo")
	vocabpath = os.path.join("data","vocabulary.json")
	parse.add_argument("--loadmodel", type = str, default =  modelpath, help = "Name for model loading")
	parse.add_argument("--vocabpath", type = str, default =  vocabpath, help = "Path to training data")
	parse.add_argument("--flag",      type = str, default = "flag.txt", help = "Path to secret flag")
	args = parse.parse_args(argv)
	with open(args.flag,"r") as f:
		args.flag = f.read().strip().replace("UiTHack24{","").replace("}","")
	if not args.loadmodel.endswith(".h5"):
		args.loadmodel += ".h5"
	return args

def Main(argv:list[str]) -> None:
	args = Flags(argv)
	
	flag = FromL33t(args.flag).split("_")
	id, word = Vocabulary(args.vocabpath)
	
	model = tf.keras.models.load_model(args.loadmodel)
	grad = FederatedLearning(model, id, flag)
	
	for i in range(len(flag)):
		# TODO: write grad numpy arrays to file or create flask server to test reconstruction
		w = flag[i]
		print(grad[i][0].indices)
		print(grad[i][0].values)
		shapes = "->".join([ str(g.shape).replace(" ","") for g in grad[i] ])
		print(f"'{w}' -> {shapes}\n")
	return

def Vocabulary(filepath:str) -> tuple[dict[str:int], dict[int:str]]:
	""" Return dual mapping between word and id. """
	with open(filepath,"r") as f:
		vocabulary = json.load(f)
	id, word = vocabulary["id"], vocabulary["word"]
	id   = { w:int(i) for w,i in id.items() }
	word = { int(i):w for i,w in word.items() }
	return id, word

def FederatedLearning(model:tf.keras.Model, id:dict[str:int], flag:list[str]) -> list[list[np.ndarray]]:
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
		grad[i] = tape.gradient(loss, model.trainable_weights)
		grad[i] = [ g.numpy() if hasattr(g,"numpy") else g for g in grad[i] ]
		# TODO: update weights with gradients
	return grad

if __name__ == "__main__":
	Main(sys.argv[1:])
