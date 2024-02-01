
# Misc. - Join :fist: The Learning :book: Federation Hype-Train

> [README](../README.md)

## Writeup

The main difference from federated-learning-1 is that function `FederatedLearning()` in [federated_learning.py](../src/federated_learning.py) no longer store the indices for the embedding layer.

The next clue is that in [train.py](../src/train.py), the vocabulary is created from a mix of [training.txt](../src/data/training.txt) and the flag's words.
If we look at the set of unique words in both [training.txt](../src/data/training.txt) and [vocabulary.json](../src/data/vocabulary.json), we can see there is a discrepancy; there is exactly one more word in the vocabulary than in the original dataset.
That enable us to find one of the flag's words without knowing exactly the position, which is ***"model"***.

```py
import json
import train
words = train.Words("data/training.txt")
with open("data/vocabulary.json") as f:
	voc = list(json.load(f)["word"].values())

known = (set(voc) - set(words)).pop()
assert known == "model"

print(
	f"len(set(training.txt))    := {len(set(words))} \n"
	f"len(set(vocabulary.json)) := {len(set(voc))} \n"
	f"Known flag-word := '{known}' \n"
)
```

We can see the number of words in the flag from the number of [gradient](../src/data/grad/) files. 
Furthermore, we know in [federated_learning.py](../src/federated_learning.py) the gradients are computed with an input `x` and a truth label `y` which come from each word in the flag and the word immediately following (with loop around).
To reconstruct which words are in the flag, our aim is to find `x` and `y` for each `data/grad/*.npz` file such that the gradients match.
Although, brute-forcing `x` and `y` for all positions/gradient-files is a heavy computation and propbably requires appropriate hardware.

For instance, with a vocabulary of `len(voc) == 3442` and flag word lenght of `len(list(flag)) == 7` we are looking at $\mathcal{O}(3,442^{2}) = \mathcal{O}(11,847,364)$ combinations of `x, y` for each `flag[i]` $i \in [0,7)$, which makes $\mathcal{O}(11,847,364 \times 7) = \mathcal{O}(82,931,548)$ possibilities. **Not so feasible**.

However, since we know one of the flag's words we can find the 1-out-of-7 gradients where **"model"** works as `x` and some `y` from the vocabulary produces similar gradients.
After that we rinse and repeat the process, but now with the word found following **"model"** as the new `x` and again find some `y`.
This complexity becomes far lower because we always know `x` and reduce $\mathcal{O}(3,442^{2} \times 7)$ into $\mathcal{O}(3,442^{1} \times 7) = \mathcal{O}(24,094)$, which is a reduction of $1-\frac{24,094}{82,931,548} = 0.9997 \approx 99.97$%.

> See [known.py](../src/solve/known.py) for an implementation.
> On a decent CPU it takes roughly 20 seconds to reconstruct the entire flag.

### Flag
> [flag.txt](../src/flag.txt)
