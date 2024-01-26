#!/usr/bin/env python3.10
"""
Reconstruction of training data from gradients 
"""

import numpy as np
import os
import time

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf
import util as common

def DeepLeakageFromGradients(model:tf.keras.Model, federated:list[dict[str:np.ndarray]], id:dict[str:int], word:dict[int:str], epochs:int, heartbeat:float) -> list[str]:
	"""
	Return flag by reconstructing training data from gradients.
	DLG repository for reference: git@github.com:mit-han-lab/dlg.git
	"""
	flag = [ "[UNK]" ] * len(federated)
	Loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = False)
	tf.keras.losses.sparse_categorical_crossentropy
	L2 = lambda x: tf.norm(x, ord = "euclidean")
	t = time.time()
	n = 1
	for pos in range(len(federated)):
		r = np.random.choice(len(word), size = (1,))
		optim = tf.optimizers.Adam()
		# x = optim.add_variable(shape = (1,), name = f"flag[{pos}]").assign(r)
		# y = optim.add_variable(shape = (1,), name = f"flag[{pos+1}]").assign(r+1)
		x = optim.add_variable(shape = (1,), name = f"flag[{pos}]")
		y = optim.add_variable(shape = (1,), name = f"flag[{pos+1}]")
		x.assign(r)
		y.assign(r+1)
		fed = federated[pos].values()
		for n in range(epochs):
			with tf.GradientTape() as tape, tf.GradientTape() as a:
				a.watch(x)
				a.watch(y)
				pred = model(x)
				loss = Loss(y, pred)
				local = tape.gradient(loss, model.trainable_weights)
				local = [ g.values.numpy() if isinstance(g, tf.IndexedSlices) else g.numpy() for g in local ]
				
				gradDiff = 0
				for l,f in zip(local, fed):
					gradDiff += L2(l - f)
			a.gradient(gradDiff, [x,y])
			optim.apply_gradients()
			if time.time() - t > n*heartbeat:
				inputword = word[int(x.numpy()[0])]
				labelword = word[int(y.numpy()[0])]
				sec =  time.time() - t
				print(f"Hearbeat: Current('{inputword}'), Label('{labelword}'), L2({loss}), Time({sec:.2f}s)")
				n += 1
			exit()
	return flag
