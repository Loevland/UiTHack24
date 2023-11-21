#!/usr/bin/env python3.10
"""
Train a neural network to predict the next word in a sequence of words.
"""

import argparse
from   infer import Infer
import json
import numpy as np
import os
import string
import sys

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf

def Flags(argv:list[str]) -> argparse.Namespace:
    """ Return parsed arguments. """
    parse = argparse.ArgumentParser(description = __doc__)
    datapath = os.path.join("data","macbeth.txt")
    parse.add_argument("--savemodel",     type   = str,          default =       None, help = "name for model saving")
    parse.add_argument("--loadmodel",     type   = str,          default =       None, help = "name for model loading")
    parse.add_argument("--summary",       action = "store_true", default =      False, help = "show model summary and exit")
    parse.add_argument("--datapath",      type   = str,          default =   datapath, help = "path to training data")
    parse.add_argument("--flag",          type   = str,          default = "flag.txt", help = "path to secret flag")
    parse.add_argument("--units",         type   = int,          default =       1024, help = "neurons in neural network")
    parse.add_argument("--layers",        type   = int,          default =          1, help = "number of fully-connected layers")
    parse.add_argument("--batch",         type   = int,          default =        128, help = "batch size")
    parse.add_argument("--epochs",        type   = int,          default =         10, help = "number of epochs to train")
    parse.add_argument("--validation",    type   = float,        default =        0.2, help = "fraction of data to use for validation")
    parse.add_argument("--inference",     action = "store_true", default =      False, help = "post training inference with random word")
    args = parse.parse_args(argv)
    with open(args.flag,"r") as f:
        args.flag = f.read().strip()\
            .replace("UiTHack24{","").replace("}","")
    if args.savemodel and not args.savemodel.endswith(".h5"):
        args.savemodel += ".h5"
    if args.loadmodel and not args.loadmodel.endswith(".h5"):
        args.loadmodel += ".h5"
    return args

def Main(argv:list[str]) -> None:
    args = Flags(argv)

    x, y, id, word = Data(args.datapath, args.flag)

    if args.loadmodel:
        model = tf.keras.models.load_model(args.loadmodel)
    else:
        model = Model(args.units, args.layers, word)
        model = Train(model, x, y, id, args.batch, args.epochs, args.validation)
    
    if args.summary:
        model.summary()
        return
    
    if args.savemodel:
        model.save(args.savemodel)
    
    if args.inference:
        r = np.random.randint(0, len(word))
        w = Infer(model, word[r], id, word, stoplength = 8)
        print(" ".join(w))
    return

def Data(filepath:str, flag:str) -> tuple[list[str], np.ndarray[int], dict[str:int], dict[int:str]]:
    """ Return words and dual mapping between word and id, and one hot labels where `y[i]` is label for `x[i+1]`. """
    x = Words(filepath)

    # add flag to data and vocabulary
    # NOTE: flag's words are not close or easily discernable in vocabulary.json
    x = list(set(x + FromL33t(flag).split("_")))
    # np.random.shuffle(x)

    id, word = Vocabulary(x, filepath)
    y = Labels(x, id)
    return x, y, id, word

def FromL33t(flag:str) -> str:
    """ Return sanitized flag for l33tspeak characters. """
    return flag\
        .replace("0","o")\
        .replace("1","i")\
        .replace("3","e")\
        .replace("4","a")\
        .replace("5","s")\
        .replace("7","t")\
        .replace("8","b")\
        .replace("9","g")

def Words(filepath:str) -> list[str]:
    """ Return list of words in data file. """
    # read file
    with open(filepath, "r") as f:
        lines = f.read().lower().split("\n")
        lines = [ line.strip("\n") for line in lines if not line.startswith("\n") ]
    # split into words
    words = []
    letters = string.ascii_lowercase + string.digits + "'"
    for line in lines:
        for w in line.split(" "):
            # filter away unwanted characters
            for c in w:
                if c not in letters:
                    w = w.replace(c,"")
            if len(w) > 0:
                words.append(w)
    # add eos tokens first for TextVectorization
    words = ["","[UNK]"] + words
    return words

def Vocabulary(x:list[str], filepath:str) -> tuple[dict[str:int], dict[int:str]]:
    """ Return dual mapping from word to vocabulary token id. """
    v = list(set(x))
    vocabulary = {
        "word" : { id:w for id, w in enumerate(v) },
        "id"   : { w:id for id, w in enumerate(v) },
    }

    dir = os.path.dirname(filepath)
    filepath = os.path.join(dir,"vocabulary.json")
    with open(filepath, "w") as f:
        json.dump(vocabulary, f)
    return vocabulary["id"], vocabulary["word"]

def Labels(x:list[str], id:dict[str:int]) -> np.ndarray[int]:
    """ Return labels such that label `y[i]` is id for word `x[i+1]` following after `x[i]`. """
    y = np.zeros( (len(x),) )
    y[:-1] = [ id[w] for w in x[1:] ]
    y[-1]  = id[x[0]]
    y = y.reshape(-1,1)
    return y.reshape(-1,1)

def Model(units:int, layers:int, word:dict[int:str]) -> tf.keras.Model:
    """ Return neural network for text-to-text generation. """
    vocabsize = len(word)
    embedding = tf.keras.layers.Embedding(vocabsize, units)
    nnlayers = [
        tf.keras.layers.Dense(units*(layers-n), activation = "relu")
            for n in range(layers)
    ]
    output = tf.keras.layers.Dense(vocabsize, activation = "softmax")
    model = tf.keras.Sequential([ embedding, *nnlayers, output ])
    model.compile(
        optimizer = "adam",
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = False),
        metrics = [ "accuracy" ],
    )
    return model

def Train(model:tf.keras.Model, x:list[str], y:np.ndarray, id:np.ndarray, batch:int, epochs:int, validation:float) -> tf.keras.Model:
    """ Train model to predict next word. """
    xid = np.array([ id[w] for w in x ]).astype(int).reshape(-1,1)
    model.fit(
        xid, y,
        batch_size = batch,
        epochs = epochs,
        validation_split = validation,
    )
    return model

if __name__ == "__main__":
    Main(sys.argv[1:])
