
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

## Solve Challenge

The provided weights have the embedding layer indices included.
Use those to look-up the vocabulary's corresponding word.

```bash
python solve/indices.py
```
