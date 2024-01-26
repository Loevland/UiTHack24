
# Readying the Challenge

## Training the Model

```bash
python train.py --savemodel model/banquo.h5
```

## Testing the Model's Output

The model is a next word predictor.
This script generates a number words in sequence.

```bash
python infer.py --loadmodel model/banquo.h5 --word <word-from-vocabulary> --stoplength <n-words-to-generate>
```

## Generate Federated Learning Gradients

The challenge is to find the flag from gradients produced by the words in the flag.
Run this to store them under `data/grad/`.

```bash
python federated_learning.py --loadmodel model/banquo.h5 --savegrad
```

## Solve Challenge Through Known Flag Exploit

This solution exploits that the word **"model"** is known to be in the flag.
By Googleing the set of words in the [vocabulary](./data/vocabulary.json), the previously unknown dataset is now known.
Doing the set difference between words in the dataset and the vocabulary reveals that the word *"model"* is in the dataset, but not in the original text.

Therefore, the flag is the additional information added in the [training](./train.py) (Data() function).

```bash
python solve/known.py 
```

On a computer without a GPU this might take some minutes combing through.
