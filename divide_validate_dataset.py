import numpy as np
import random
import pickle
import os
import argparse
import chainer as ch
from src.dataset import Dataset, divide
import src.inference as I
import src.train as T

SEED_MAX = 2**32 - 1

parser = argparse.ArgumentParser()
parser.add_argument("--num-valid", help="The number of entries for validation.", type=int, default=None)
parser.add_argument("--seed", help="The random seed", type=int, default=13782)
parser.add_argument("dataset", help="The path of the dataset pickle file", type=str)
parser.add_argument("output", help="The path of the directory to store the divided dataset", type=str)
args = parser.parse_args()

root_rng = np.random.RandomState(args.seed)
random.seed(root_rng.randint(SEED_MAX))
np.random.seed(root_rng.randint(SEED_MAX))

if not os.path.exists(args.output):
    os.makedirs(args.output)
assert(os.path.isdir(args.output))

with open(args.dataset, "rb") as f:
    dataset: Dataset = pickle.load(f)

num_valid = args.num_valid
num_train = len(dataset.entries) - num_valid

subdatasets = divide(dataset, dict([["train", num_train], ["valid", num_valid]]), rng = np.random.RandomState(root_rng.randint(SEED_MAX)))

with open(os.path.join(args.output, "train.pickle"), "wb") as f:
    pickle.dump(subdatasets["train"], f)
with open(os.path.join(args.output, "valid.pickle"), "wb") as f:
    pickle.dump(subdatasets["valid"], f)