#!/usr/bin/env python3.10
"""
Solve the flag through search methods.
"""

import os
import numpy as np
import time

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf
import util as common

def BruteForce(model:tf.keras.Model, federated:list[dict[str:np.ndarray]], word:dict[int:str], heartbeat:float) -> list[str]:
	""" Return list of flag's words reconstructed from gradients. """
	flag = [ "[UNK]" ] * len(federated)
	vocabsize = len(word)
	t = time.time()
	n = 1
	for i in range(vocabsize):
		print(f"time: {time.time()-t:.2f}s, id,word : {i},'{word[i]}'")
		x = np.array([ i ])
		for j in range(vocabsize):
			if time.time() - t > n*heartbeat:
				common.Report(word[i], word[j], time.time() - t, heartbeat = True)
				n += 1
			if i == j:
				continue
			y = np.array([ j ])
			local = common.ComputeGradients(model, x, y)
			# check if gradients match with any flag-positional gradients for word `word[i]` and label `word[j]`
			for pos,fed in enumerate(federated):
				if common.MatchGradients(local, fed):
					flag[pos] = word[i]
					common.Report(word[i], word[j], time.time() - t)
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
			common.Report(current, word[labelid]+f":{labelid}", time.time() - t, heartbeat = True)
			n += 1
		x = np.array([ id[current] ])
		y = np.array([ labelid ])
		# 2.1)
		local = common.ComputeGradients(model, x, y)
		# 2.2) & 2.3)
		index = common.MatchFlagPosition(local, federated, pos)
		if index is None:
			continue
		# 3.1) 3.2) & 3.3)
		flag[index] = current
		flag[(index+1) % len(flag)] = word[labelid]
		current = word[labelid]
		# 4.2)
		pos = index
		common.Report(flag[index], flag[(index+1) % len(flag)]+f":{labelid}", time.time() - t, flag = flag)

	t = time.time() - t
	print(f"Time: {t:.2f}s")
	return flag
