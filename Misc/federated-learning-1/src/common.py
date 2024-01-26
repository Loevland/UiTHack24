#!/usr/bin/env python3.10
"""
Common utilities for the federated learning.
"""

import json
import numpy as np
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf

def ReadFlag(flagpath:str) -> list[str]:
    """ Return processed flag from file. """
    with open(flagpath,"r") as f:
        flag = f.read().strip().replace("UiTHack24{","").replace("}","")
    flag = FromL33t(flag).split("_")
    return flag

def FromL33t(s:str) -> str:
    """ Return string with replaced l33t-speech characters. """
    return s\
        .replace("0","o")\
        .replace("1","i")\
        .replace("3","e")\
        .replace("4","a")\
        .replace("5","s")\
        .replace("7","t")\
        .replace("8","b")\
        .replace("9","g")

def Infer(model:tf.keras.Model, start:str, id:dict[str:int], word:dict[int:str], stoplength:int) -> list[str]:
    """ Return list of words predicted by model. """
    out = [ start ] * stoplength
    xid = id[start]
    for i in range(1, stoplength):
        xid = model(np.array([ xid ])).numpy().argmax()
        out[i] = word[xid]
    return out

def Vocabulary(filepath:str) -> tuple[dict[str:int], dict[int:str]]:
    """ Return dual mapping between word and id. """
    with open(filepath,"r") as f:
        v = json.load(f)
    id, word = v["id"], v["word"]
    id   = { w:int(i) for w,i in id.items() }
    word = { int(i):w for i,w in word.items() }
    return id, word
