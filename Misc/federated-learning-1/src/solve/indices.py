#!/usr/bin/env python3
"""
Extract flag through indices in gradients.
"""

import json
import numpy as np
import os

# Read gradients.
grads:list[dict[str:np.ndarray]] = []
gradpath = os.path.join(os.path.abspath(""),"data","grad")
for file in os.listdir(gradpath):
	if not file.endswith(".npz"):
		continue
	filepath = os.path.join(gradpath,file)
	grads.append(dict(np.load(filepath)))

# Read vocabulary.
vocabpath = os.path.join(os.path.abspath(""),"data","vocabulary.json")
with open(vocabpath,"r") as f:
	vocabulary = json.load(f)
word = { int(id):w for id,w in vocabulary["word"].items() }

# Extract flag from gradients.
flag = [ '|' ] * len(grads)
for i,grad in enumerate(grads):
	indices = [ layername for layername in grad.keys() if "indices" in layername ][0]
	id = grad[indices][0]
	flag[i] = word[id]

# Reverse format flag to l33t-speech as seen in src/common.py
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
flag = "_".join([ ToL33t(w) for w in flag ])
print(f"flag := '{flag}'")
