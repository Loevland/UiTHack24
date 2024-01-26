
python train.py --savemodel model/banquo.h5
python federated_learning.py --loadmodel model/banquo.h5 --savegrad
