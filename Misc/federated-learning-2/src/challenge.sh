
export TF_CPP_MIN_LOG_LEVEL=3

create() {
    # Create model, vocabulary and gradients.
    python train.py --savemodel model/banquo.h5 --epochs 4
    python federated_learning.py --loadmodel model/banquo.h5 --savegrad

    # Create handout files.
    mkdir -p handout
    cp -r \
        data/ \
        model/ \
        common.py \
        federated_learning.py \
        infer.py \
        requirements.txt \
        train.py \
        -t handout
    zip -r handout handout
}

clean() {
    rm -rf \
        data/vocabulary.json \
        data/grad/ \
        model/ \
        __pycache__/ \
        solve/__pycache__/ \
        handout/ \
        handout.zip
}

if [ "$1" == "create" ]; then
    create
elif [ "$1" == "clean" ]; then
    clean
else
    echo "usage: ./$(basename $BASH_SOURCE) <create|clean>"
    exit 1
fi

