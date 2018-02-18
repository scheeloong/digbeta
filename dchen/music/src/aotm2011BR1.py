import os
import sys
import gzip
import time
import numpy as np
import pickle as pkl
from scipy.sparse import issparse, vstack


if len(sys.argv) != 4:
    print('Usage: python', sys.argv[0], 'WORK_DIR  START  END')
    sys.exit(0)
else:
    work_dir = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])

data_dir = os.path.join(work_dir, 'data')
src_dir = os.path.join(work_dir, 'src')
sys.path.append(src_dir)

from BinaryRelevance import BinaryRelevance

pkl_data_dir = os.path.join(data_dir, 'aotm-2011/setting1')
fxtrain = os.path.join(pkl_data_dir, 'X_train_dev.pkl.gz')
fytrain = os.path.join(pkl_data_dir, 'Y_train_dev.pkl.gz')

X_train = pkl.load(gzip.open(fxtrain, 'rb'))
Y_train = pkl.load(gzip.open(fytrain, 'rb'))

assert issparse(Y_train)
assert X_train.shape[0] == Y_train.shape[0]

Y = Y_train[:, start:end]

print(time.strftime('%Y-%m-%d %H:%M:%S'))

clf = BinaryRelevance(C=1, n_jobs=10)
clf.fit(X_train, Y)

print(time.strftime('%Y-%m-%d %H:%M:%S'))

fmodel = os.path.join(pkl_data_dir, 'br1-aotm2011-%d-%d.pkl' % (start, end))
pkl.dump(clf, open(fmodel, 'wb'))
