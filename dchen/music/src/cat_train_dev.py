import os
import sys
import gzip
import time
import numpy as np
import pickle as pkl
from scipy.sparse import issparse, vstack


if len(sys.argv) != 2:
    print('Usage: python', sys.argv[0], 'WORK_DIR')
    sys.exit(0)
else:
    work_dir = sys.argv[1]

data_dir = os.path.join(work_dir, 'data')
src_dir = os.path.join(work_dir, 'src')
sys.path.append(src_dir)

pkl_data_dir = os.path.join(data_dir, 'aotm-2011/setting1')
fxtrain = os.path.join(pkl_data_dir, 'X_train.pkl.gz')
fytrain = os.path.join(pkl_data_dir, 'Y_train.pkl.gz')
fxdev = os.path.join(pkl_data_dir, 'X_dev.pkl.gz')
fydev = os.path.join(pkl_data_dir, 'Y_dev.pkl.gz')

X_train = pkl.load(gzip.open(fxtrain, 'rb'))
Y_train = pkl.load(gzip.open(fytrain, 'rb'))
X_dev = pkl.load(gzip.open(fxdev, 'rb'))
Y_dev = pkl.load(gzip.open(fydev, 'rb'))

assert issparse(Y_train)
assert issparse(Y_dev)

X = np.vstack([X_train, X_dev])
Y = vstack([Y_train.tolil(), Y_dev.tolil()]).tocsc().astype(np.bool)  
# NOTE: explicitly set type of Y is necessary, otherwise see issue #9777 of scikit-learn

assert X.shape[0] == Y.shape[0]

fxtrndev = os.path.join(pkl_data_dir, 'X_train_dev.pkl.gz')
fytrndev = os.path.join(pkl_data_dir, 'Y_train_dev.pkl.gz')

pkl.dump(X, gzip.open(fxtrndev, 'wb'))
pkl.dump(Y, gzip.open(fytrndev, 'wb'))

