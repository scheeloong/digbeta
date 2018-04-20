import os
import sys
import gzip
import time
import numpy as np
import pickle as pkl
from sklearn.metrics import roc_auc_score
from models import MTC


if len(sys.argv) != 6:
    print('Usage: python', sys.argv[0],
          'WORK_DIR  DATASET  C  P  TRAIN_DEV(Y/N)')
    sys.exit(0)
else:
    work_dir = sys.argv[1]
    dataset = sys.argv[2]
    C = float(sys.argv[3])
    p = float(sys.argv[4])
    trndev = sys.argv[5]

assert trndev in ['Y', 'N']
assert trndev == 'Y'

data_dir = os.path.join(work_dir, 'data/%s/setting4' % dataset)
fx = os.path.join(data_dir, 'X.pkl.gz')
fytrain = os.path.join(data_dir, 'Y_train.pkl.gz')
fytest = os.path.join(data_dir, 'Y_test.pkl.gz')
fcliques_train = os.path.join(data_dir, 'cliques_train.pkl.gz')
fprefix = 'trndev-plgen2-%g-%g' % (C, p)

fmodel = os.path.join(data_dir, '%s.pkl.gz' % fprefix)
fnpy = os.path.join(data_dir, '%s.npy' % fprefix)

X = pkl.load(gzip.open(fx, 'rb'))
Y_train = pkl.load(gzip.open(fytrain, 'rb'))
Y_test = pkl.load(gzip.open(fytest, 'rb'))
cliques_train = pkl.load(gzip.open(fcliques_train, 'rb'))

print('C: %g, p: %g' % (C, p))
print(X.shape, Y_train.shape)
print(time.strftime('%Y-%m-%d %H:%M:%S'))

if os.path.exists(fmodel):
    print('evaluating ...')
    clf = pkl.load(gzip.open(fmodel, 'rb'))   # for evaluation
else:
    print('training ...')
    clf = MTC(X, Y_train, C=C, p=p, user_playlist_indices=cliques_train)
    clf.fit(njobs=1, verbose=2, fnpy=fnpy)

if clf.trained is True:
    pkl.dump(clf, gzip.open(fmodel, 'wb'))
    rps = []
    aucs = []
    for j in range(Y_test.shape[1]):
        y_true = Y_test[:, j].A.reshape(-1)
        npos = y_true.sum()
        assert npos > 0
        y_pred = np.dot(X, clf.mu).reshape(-1)
        sortix = np.argsort(-y_pred)
        y_ = y_true[sortix]
        rps.append(np.mean(y_[:npos]))
        aucs.append(roc_auc_score(y_true, y_pred))
    clf.metric_score = (np.mean(rps), np.mean(aucs), len(rps), Y_test.shape[1])
    pkl.dump(clf, gzip.open(fmodel, 'wb'))
    print('\n%g, %g, %d / %d' % clf.metric_score)
