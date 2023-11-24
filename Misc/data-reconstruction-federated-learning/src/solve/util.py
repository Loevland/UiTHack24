#!/usr/bin/env python3.10
"""
Common utilities for finding the flag in federated learning.
"""

import json
import os
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf

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

def Vocabulary(filepath:str) -> tuple[dict[str:int], dict[int:str]]:
    """ Return dual mapping between word and id. """
    with open(filepath,"r") as f:
        v = json.load(f)
    id, word = v["id"], v["word"]
    id   = { w:int(i) for w,i in id.items() }
    word = { int(i):w for i,w in word.items() }
    return id, word
