#!/usr/bin/env python3.10
"""
Reconstruction of training data from gradients 
"""

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

import dlg
import force
import tensorflow as tf
import util as common

def Flags(argv:list[str]) -> argparse.Namespace:
	""" Return parsed arguments. """
	parse = argparse.ArgumentParser(description = __doc__)
	modelpath = os.path.join("model","banquo.h5")
	vocabpath = os.path.join("data","vocabulary.json")
	gradpath  = os.path.join("..","data","grad")
	parse.add_argument("--loadmodel", type =   str, default = modelpath, help = "name for model loading")
	parse.add_argument("--vocabpath", type =   str, default = vocabpath, help = "path to training data")
	parse.add_argument("--loadgrad",  type =   str, default =  gradpath, help = "path to directory with gradients [0-n]")
	parse.add_argument("--fetchgrad", type =   str, default =      None, help = "fetch gradients from endpoint")
	parse.add_argument("--method",    type =   str, default =   "brute", help = "method for solving the challenge", choices = [ "brute","smart","dlg" ])
	parse.add_argument("--heartbeat", type = float, default =       5.0, help = "seconds interval for reporting progress")
	parse.add_argument("--epochs",    type =   int, default =       512, help = "number of epochs for DLG")
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

	id, word = common.Vocabulary(args.vocabpath)
	model:tf.keras.Model = tf.keras.models.load_model(args.loadmodel)
	grad = Gradient(args.loadgrad)

	flag = Solve(model, grad, id, word, args)
	flag = [ ToL33t(w) for w in flag ]
	flag = "_".join(flag)
	flag = f"UiTHack24{{{flag}}}"
	print(flag)

	return

def Gradient(filepaths:list[str]) -> list[dict[str:np.ndarray]]:
	""" Return list of gradients from numpy files. """
	grad = []
	for file in filepaths:
		grad.append(dict(np.load(file)))
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

def Solve(model:tf.keras.Model, federated:list[dict[str:np.ndarray]], id:dict[str:int], word:dict[int:str], args:argparse.Namespace) -> list[str]:
	""" Entry point for solving the challenge. """
	match args.method:
		case "brute":
			flag = force.BruteForce(model, federated, word, args.heartbeat)
		case "smart":
			flag = force.SmartForce(model, federated, id, word, args.heartbeat)
		case "dlg":
			flag = dlg.DeepLeakageFromGradients(model, federated, id, word, args.epochs, args.heartbeat)
	return flag

if __name__ == "__main__":
	Main(sys.argv[1:])
