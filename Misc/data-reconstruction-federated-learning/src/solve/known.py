#!/usr/bin/env python3
"""
Solve federated learning challenge with one known flag word.
"""

import argparse
import json
import numpy as np
import os
import sys
import time

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf

def Flags(argv:list[str]) -> argparse.Namespace:
	parse = argparse.ArgumentParser()
	parse.add_argument("--vocabulary", "-v", type = str, default = "data/vocabulary.json", help = "vocabulary path")
	parse.add_argument("--loadmodel",  "-m", type = str, default =      "model/banquo.h5", help = "model path")
	parse.add_argument("--loadgrad",   "-g", type = str, default =            "data/grad", help = "gradient path")
	args = parse.parse_args(argv)
	return args

def Main(argv:list[str]) -> None:
	args = Flags(argv)
	
	id, word = Vocabulary(args.vocabulary)
	model:tf.keras.Model = tf.keras.models.load_model(args.loadmodel)
	grads = Gradients(args.loadgrad)
	known = FindKnown(list(word.values()))
	flag = Reconstruct(known, grads, model, id, word)
	
	flag = "_".join([ ToL33t(w) for w in flag ])
	print(f"flag := '{flag}'")
	return

def ToL33t(s:str) -> str:
	""" Return string with inserted l33t-speech characters. """
	return s\
		.replace("o","0")\
		.replace("i","1")\
		.replace("e","3")\
		.replace("a","4")\
		.replace("s","5")\
		.replace("t","7")\
		.replace("b","8")\
		.replace("g","9")

def Vocabulary(filepath:str) -> tuple[dict[str:int], dict[int:str]]:
    with open(filepath,"r") as f:
        v = json.load(f)
    id, word = v["id"], v["word"]
    id   = { w:int(i) for w,i in id.items() }
    word = { int(i):w for i,w in word.items() }
    return id, word

def Gradients(path:str) -> list[dict[str:np.ndarray]]:
	grad = []
	for file in sorted(os.listdir(path)):
		file = os.path.join(path,file)
		grad.append(dict(np.load(file)))
	return grad

def FindKnown(words:list[str]) -> str:
	""" Return outstanding word in vocabulary from set difference of original text. """
	# Google hit from partial search of vocabulary, e.g. ctrl-paste into browser after
	# `python -c "import json; print(*list(json.load(open('data/vocabulary.json'))['word'].values())[400:500], end = '')" | xclip -selection clipboard`
	# Top result:
	# https://www.shakespearegeek.com/shakespeare_plays/macbeth.html
	datapath = os.path.join(os.path.abspath(""),"solve","original-data.txt")
	# Process words like in train.py
	parent = os.path.join(os.path.dirname(__file__),"..")
	sys.path.append(parent)
	from train import Words
	other = Words(datapath)
	# Difference.
	known = set(words) - set(other)
	assert "model" in known
	return "model"

def Reconstruct(known:str, grads:list[dict[str:np.ndarray]], model:tf.keras.Model, id:dict[str:int], word:dict[int:str]) -> list[str]:
	flag = [ '|' ] * len(grads)
	t = 0.0
	while '|' in flag:
		s = time.time()
		i, next = FindFlagPosition(known, grads, model, id, word)
		s = time.time() - s
		
		print(f"Known word '{known}' is number {i+1} in flag with next word being '{next}'; time {s:.2f}s")
		
		flag[i] = known
		flag[(i+1)%len(flag)] = next
		
		known = next
		t += s
	print(f"Total time := {t:.2f}s")
	return flag

def FindFlagPosition(known:str, grads:list[dict[str:np.ndarray]], model:tf.keras.Model, id:dict[str:int], word:dict[int:str], tol:float = 0.1) -> tuple[int, str]:
	""" Return index in flag with length `len(grads)` where `known` belongs and the word which succeeds it. """
	Loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = False)
	# Assume hit when gradients for last layer are close enough.
	last = model.trainable_weights[-1].name
	# Try each word in vocabulary as next for `known`.
	for w in word.values():
		x = np.array([ id[known] ])
		y = np.array([ id[w] ])
		with tf.GradientTape() as tape:
			tape.watch(model.trainable_weights)
			pred = model(x)
			loss = Loss(y, pred)
		dw = tape.gradient(loss, model.trainable_weights)
		# Look for close enough match in last layer for all gradients.
		for i in range(len(grads)):
			if np.allclose(dw[-1], grads[i][last], rtol = tol, atol = tol):
				return i, w
	raise ValueError(f"Could not find flag position for partially known word '{known}'")

if __name__ == "__main__":
	Main(sys.argv[1:])
