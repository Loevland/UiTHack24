#!/usr/bin/env python3.10
"""
Train a neural network to predict the next word in a sequence of words.
"""

import argparse
import common
import json
import numpy as np
import os
import string
import sys
import tensorflow as tf

def Flags(argv:list[str]) -> argparse.Namespace:
    """ Return parsed arguments. """
    parse = argparse.ArgumentParser(description = __doc__)
    datapath = os.path.join("data","training.txt")
    parse.add_argument("--savemodel",     type   = str,          default =       None, help = "name for model saving")
    parse.add_argument("--loadmodel",     type   = str,          default =       None, help = "name for model loading")
    parse.add_argument("--summary",       action = "store_true", default =      False, help = "show model summary and exit")
    parse.add_argument("--datapath",      type   = str,          default =   datapath, help = "path to training data")
    parse.add_argument("--flag",          type   = str,          default = "flag.txt", help = "path to secret flag")
    parse.add_argument("--embedspace",    type   = int,          default =        128, help = "size of embedding vector space")
    parse.add_argument("--batch",         type   = int,          default =        128, help = "batch size")
    parse.add_argument("--epochs",        type   = int,          default =         10, help = "number of epochs to train")
    parse.add_argument("--validation",    type   = float,        default =        0.0, help = "fraction of data to use for validation")
    parse.add_argument("--inference",     action = "store_true", default =      False, help = "post training inference with random word")
    args = parse.parse_args(argv)
    args.flag = common.ReadFlag(args.flag)
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
        model = Model(word, args.embedspace)
        model = Train(model, x, y, id, args.batch, args.epochs, args.validation)
    
    if args.summary:
        model.summary()
        return
    
    if args.savemodel:
        model.save(args.savemodel)
    
    if args.inference:
        r = np.random.randint(0, len(word))
        w = common.Infer(model, word[r], id, word, stoplength = 8)
        print(" ".join(w))
    return

def Data(filepath:str, flag:list[str]) -> tuple[list[str], np.ndarray[int], dict[str:int], dict[int:str]]:
    """ Return words and dual mapping between word and id, and one hot labels where `y[i]` is label for `x[i+1]`. """
    x = Words(filepath)

    # add flag to data and vocabulary
    # NOTE: flag's words are not close or easily discernable in vocabulary.json
    x = list(set(x + flag))
    np.random.shuffle(x)

    id, word = CreateVocabulary(x, filepath)
    y = Labels(x, id)
    return x, y, id, word

def Words(filepath:str) -> list[str]:
    """ Return list of processed words in file. """
    # read training file
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
    return words

def CreateVocabulary(x:list[str], filepath:str) -> tuple[dict[str:int], dict[int:str]]:
    """ Return and store dual mapping from word to vocabulary token id. """
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

def Model(word:dict[int:str], embedspace:int) -> tf.keras.Model:
    """ Return neural network for text-to-text generation. """
    vocabsize = len(word)
    embedding = tf.keras.layers.Embedding(vocabsize, embedspace)
    output = tf.keras.layers.Dense(vocabsize, activation = "softmax")
    model = tf.keras.Sequential([ embedding, output ])
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
