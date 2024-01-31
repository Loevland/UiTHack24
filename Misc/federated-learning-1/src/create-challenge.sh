
python train.py --savemodel model/banquo.h5 --epochs 4
python federated_learning.py --loadmodel model/banquo.h5 --savegrad
mkdir -p handout
cp -r federated_learning.py data/ infer.py model/ requirements.txt train.py -t handout
rm handout/data/*.txt
zip -r handout handout
