> # Federated Learning 1
> > Misc - 500pts/1 solve
>
> Isn't open source great?
> You know what's also great? Machine learning :bowtie:
> Did you know federated learning is basically the monster-mash of both?
>
> And what's absolutely mind boggling is that it comes with complete data privacy! :relieved:

## Writeup
The model's architecture consists of one embedding and one dense layer.
When [federated_learning.py](../src/federated_learning.py) stores the gradients for the embedding layer these gradients also contain an index into which rows were part of the forward pass.
Since each gradient comes from one forward pass of one word, the indices are one-to-one related to the vocabulary mapping, so if looking at the first gradient file's embedding index and then looking up the corresponding word mapping in [vocabulary.json](../src/data/vocabolary.json) will yield the first flag-word; `by`.
After finding all the words, remember to revert the words from plain text into L33t opposite of [common.py](../src/common.py)'s FromL33t function.
L33t version of the first word `by` is `8y`.

See [solution.py](../src/solve/indices.py) for extraction script.

[Flag](../src/flag.txt)