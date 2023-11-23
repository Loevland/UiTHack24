#!/usr/bin/env python3.10
"""
Reconstruction of training data from gradients 
"""
# DLG repo
# git@github.com:mit-han-lab/dlg.git

"""
Solution Brainstrom:

 * Allow access to tf.IndexedSlices tensor from tf.GradientTape containing vocabulary id for each word.
 * Reconstruction of training data from gradients (DLG).
 * OSI, search web for hits with all words in vocabulary, then find words in the vocabulary but not the original training-set.
	* Only one word, 'model' will be evident in the case of the MacBeth play.
 * In case federated learning happens on batch size of 1;
 	1) We'll know the number of words in the flag.
	2) Gradients are for a single word.
	3) Computing gradients for all words in the vocabulary with the right next word label yields gradients equal to the federated.
	4) This is an `O(N^2) = O(len(vocabulary)^2) = O(3444^2) = O(1,1861,136)` operation.
	*) Will not work if the flag's words are batched together (see reconstruction solution).
"""

import argparse
import numpy as np
import os
import sys
import time

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import federated_learning as fedlearn
import tensorflow as tf
import util

def Flags(argv:list[str]) -> argparse.Namespace:
	""" Return parsed arguments. """
	parse = argparse.ArgumentParser(description = __doc__)
	modelpath = os.path.join("model","banquo.h5")
	vocabpath = os.path.join("data","vocabulary.json")
	parse.add_argument("--loadmodel", type =   str, default = modelpath, help = "name for model loading")
	parse.add_argument("--vocabpath", type =   str, default = vocabpath, help = "path to training data")
	parse.add_argument("--loadgrad",  type =   str, default =      None, help = "path to directory with gradients [0-n]")
	parse.add_argument("--fetchgrad", type =   str, default =      None, help = "fetch gradients from endpoint")
	parse.add_argument("--method",    type =   str, default =   "brute", help = "method for solving the challenge", choices = [ "brute","smart" ])
	parse.add_argument("--heartbeat", type = float, default =       5.0, help = "seconds interval for reporting progress")
	args = parse.parse_args(argv)
	if not args.loadmodel.endswith(".h5"):
		args.loadmodel += ".h5"
	if args.loadgrad:
		args.loadgrad = sorted([ os.path.join(args.loadgrad,g) for g in os.listdir(args.loadgrad) ])
	if not (args.loadgrad or args.fetchgrad):
		exit("Either --loadgrad or --fetchgrad must be specified")
	return args

def Main(argv:list[str]) -> None:
	args = Flags(argv)

	id, word = util.Vocabulary(args.vocabpath)
	model:tf.keras.Model = tf.keras.models.load_model(args.loadmodel)

	# TODO: get grad from flask app or numpy files
	if args.loadgrad:
		grad = Gradient(args.loadgrad)
	elif args.fetchgrad:
		grad = FetchGradients(args.fetchgrad)

	flag = Solve(model, grad, id, word, args.heartbeat, args.method)
	flag = [ ToL33t(w) for w in flag ]
	flag = "_".join(flag)
	flag = f"UiTHack24{{{flag}}}"
	print(flag)
	
	return

def Gradient(filepaths:list[str]) -> list[dict[str:np.ndarray]]:
	""" Return list of gradients from numpy files. """
	grad = []
	for file in filepaths:
		grad.append(np.load(file))
	return grad

def FetchGradients(endpoint:str) -> list[dict[str:np.ndarray]]:
	""" Return list of gradients from endpoint. """
	assert False, "Not implemented"
	grad = []
	return grad

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

def Solve(model:tf.keras.Model, federated:list[dict[str:np.ndarray]], id:dict[str:int], word:dict[int:str], heartbeat:float, method:str = "brute") -> list[str]:
	""" Entry point for solving the challenge. """
	match method:
		case "brute":
			flag = BruteForce(model, federated, id, word)
		case "smart":
			flag = SmartForce(model, federated, id, word, heartbeat)
	return flag

def BruteForce(model:tf.keras.Model, federated:list[dict[str:np.ndarray]], id:dict[str:int], word:dict[int:str]) -> list[str]:
	""" Return list of flag's words reconstructed from gradients. """
	flag = [ "[UNK]" ] * len(federated)
	vocabsize = len(word)
	t = time.time()
	for i in range(vocabsize):
		print(f"time: {time.time()-t:.2f}s, id,word : {i},'{word[i]}'")
		x = np.array([ i ])
		for j in range(vocabsize):
			if i == j:
				continue
			y = np.array([ j ])
			local = ComputeGradients(model, x, y)
			# check if gradients match with any flag-positional gradients for word `word[i]` and label `word[j]`
			for pos,fed in enumerate(federated):
				if MatchGradients(local, fed):
					flag[pos] = word[i]
					Report(word[i], word[j], time.time() - t)
					break
			if pos < len(federated):
				break
		if not "[UNK]" in flag:
			break
	
	t = time.time() - t
	print(f"Time: {t:.2f}s")
	return flag

def SmartForce(model:tf.keras.Model, federated:list[dict[str:np.ndarray]], id:dict[str:int], word:dict[int:str], heartbeat:float) -> list[str]:
	"""
	Return list of flag's words with smart search through possibilities.
	1) Start with known word in flag from OSI.
	2) Search:
		2.1) Find label for current word used to compute gradients.
		2.2) By computing gradients for current and other word.
		2.3) And comparing if gradients match at any place in the federated gradients.
	3) Update:
		3.1) Set current word in flag at corresponding federated gradient-list index.
		3.2) Set label word in flag after current word's place.
		3.3) Set label word to current word.
	4) Repeat:
		4.1) From 2).
		4.2) Until all words are found.
		4.3) But after finding 1st word's label, take advantage of positional knowledge when matching with federated gradients.
	"""
	flag = [ "[UNK]" ] * len(federated)
	# 1)
	# current = "model"
	current = "of"
	# 2)
	pos = None
	# labelid = -1
	labelid = id["scorpions"]
	t = time.time()
	n = 1
	while "[UNK]" in flag: # 4.2)
		labelid = (labelid + 1) % len(word)
		if time.time() - t > n*heartbeat:
			Report(current, word[labelid]+f":{labelid}", time.time() - t, heartbeat = True)
			n += 1
		x = np.array([ id[current] ])
		y = np.array([ labelid ])
		# 2.1)
		local = ComputeGradients(model, x, y)
		# 2.2) & 2.3)
		index = MatchFlagPosition(local, federated, pos)
		if index is None:
			continue
		# 3.1) 3.2) & 3.3)
		flag[index] = current
		flag[(index+1) % len(flag)] = word[labelid]
		current = word[labelid]
		# 4.2)
		pos = index
		Report(flag[index], flag[(index+1) % len(flag)]+f":{labelid}", time.time() - t, flag = flag)

	t = time.time() - t
	print(f"Time: {t:.2f}s")
	return flag

def ComputeGradients(model:tf.keras.Model, x:np.ndarray, y:np.ndarray, Loss:tf.keras.losses.Loss = tf.losses.SparseCategoricalCrossentropy(from_logits = False)) -> dict[str:np.ndarray]:
	""" Return map from model layer name to gradients for model weights. """
	with tf.GradientTape() as tape:
		tape.watch(model.trainable_weights)
		pred = model(x)
		loss = Loss(y, pred)
	dw = tape.gradient(loss, model.trainable_weights)
	# format local gradients same as federated gradients
	local = {}
	for w,g in zip(model.trainable_weights, dw):
		local[w.name] = g.values.numpy() if isinstance(g, tf.IndexedSlices) else g.numpy()
	return local

def MatchFlagPosition(local:dict[str:np.ndarray], federated:list[dict[str:np.ndarray]], pos:int = None) -> int|None:
	"""
	Return index in flag where word `local` gradients match `federated` gradients, return None on no matches.
	If `pos` is provided only match on `federated[pos]`.
	"""
	if pos is not None:
		# filter out number of federated gradients to compare local to
		if MatchGradients(local, federated[pos]):
			return pos
		return None
	for pos in range(len(federated)):
		if MatchGradients(local, federated[pos]):
			return pos
	return None

def MatchGradients(local:dict[str:np.ndarray], federated:dict[str:np.ndarray]) -> bool:
	""" Return true if local gradients match with federated gradients. """
	match = True
	# three layers in model, so three gradients arrays
	for layer in federated.keys():
		l:np.ndarray = local[layer]
		f:np.ndarray = federated[layer]
		if not np.allclose(l, f):
			match = False
			break
	return match

def Report(inputword:str, labelword:str, sec:float, flag:list[str] = [], heartbeat:bool = False) -> None:
	""" Print report on progress. """
	if heartbeat:
		return print(f"Hearbeat: Current('{inputword}'), Label('{labelword}'), Time({sec:.2f}s)")
	return print(f"PROGRESS: Input('{inputword}'), Label('{labelword}'), Time({sec:.2f}s), Flag('{' '.join(flag)}')")

if __name__ == "__main__":
	Main(sys.argv[1:])
