# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 11:56:43 2018

@author: Prateek Kumar Goel
"""

"""
Multiclass and multilabel classification strategies
===================================================

This module implements multiclass learning algorithms:
    - error correcting output codes

"""

"""
Credits to: scikit-learn to provide the base for making this library possible
Link: https://scikit-learn.org/

"""

import numpy as np
import warnings

from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.base import MetaEstimatorMixin, is_regressor
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.utils import check_random_state
from sklearn.utils.validation import check_is_fitted
from sklearn.utils.validation import check_X_y, check_array
from sklearn.externals.joblib import Parallel
from sklearn.externals.joblib import delayed



def _fit_binary(estimator, X, y, classes=None):
    """Fit a single binary estimator."""
    unique_y = np.unique(y)
    if len(unique_y) == 1:
        if classes is not None:
            if y[0] == -1:
                c = 0
            else:
                c = y[0]
            warnings.warn("Label %s is present in all training examples." %
                          str(classes[c]))
        estimator = _ConstantPredictor().fit(X, unique_y)
    else:
        estimator = clone(estimator)
        estimator.fit(X, y)
    return estimator


def _predict_binary(estimator, X):
    """Make predictions using a single binary estimator."""
    if is_regressor(estimator):
        return estimator.predict(X)
    try:
        score = np.ravel(estimator.decision_function(X))
    except (AttributeError, NotImplementedError):
        # probabilities of the positive class
        score = estimator.predict_proba(X)[:, 1]
    return score
#    return estimator.predict(X)

def _decode_binary(decoder , Y, code_book):
    if decoder == "hamm":
        return
    elif decoder == "eucl":
        return euclidean_distances(Y, code_book).argmin(axis=1)
    else:
        raise ValueError("The decoder function should implement "
                         "hamm or eucl")
    
def _check_estimator(estimator):
    """Make sure that an estimator implements the necessary methods."""
    if (not hasattr(estimator, "decision_function") and
            not hasattr(estimator, "predict_proba")):
        raise ValueError("The base estimator should implement "
                         "decision_function or predict_proba!")


class _ConstantPredictor(BaseEstimator):

    def fit(self, X, y):
        self.y_ = y
        return self

    def predict(self, X):
        check_is_fitted(self, 'y_')
        return np.repeat(self.y_, X.shape[0])
    
    def decision_function(self, X):
        check_is_fitted(self, 'y_')

        return np.repeat(self.y_, X.shape[0])

    def predict_proba(self, X):
        check_is_fitted(self, 'y_')

        return np.repeat([np.hstack([1 - self.y_, self.y_])],
                         X.shape[0], axis=0)



class ECOCClassifier(BaseEstimator, ClassifierMixin, MetaEstimatorMixin):
    """(Error-Correcting) Output-Code multiclass classification strategy

    Parameters
    ----------
    estimator : estimator object
        An estimator object implementing `fit` and one of `decision_function`
        or `predict_proba`.

    code_length : float
        The pecentage of classes to be used to create the code book.
        A number between 0 and 1 will require fewer classifiers than
        one-vs-the-rest. A number greater than 1 will require more classifiers
        than one-vs-the-rest. A number greater than 1 is recommended to 
        provide valid bit strings to all the classes in the codebook.
    
    decoder : string
        Select the decoding method to decode the output class and match it 
        to the codebook. The options include "hamm" for hamming and "eucl" euclidean .

    random_state : int, RandomState instance or None, optional, default: None
        The generator used to initialize the codebook.  If int, random_state is
        the seed used by the random number generator; If RandomState instance,
        random_state is the random number generator; If None, the random number
        generator is the RandomState instance used by `np.random`.

    n_jobs : int, optional, default: 1
        The number of jobs to use for the computation. If -1 all CPUs are used.
        If 1 is given, no parallel computing code is used at all, which is
        useful for debugging. For n_jobs below -1, (n_cpus + 1 + n_jobs) are
        used. Thus for n_jobs = -2, all CPUs but one are used.

    Attributes
    ----------
    estimators_ : list of `int(n_classes * code_length)` estimators
        Estimators used for predictions.

    classes_ : numpy array of shape [n_classes]
        Array containing labels.

    code_book_ : numpy array of shape [n_classes, code_length]
        Binary array containing the code of each class.

    References
    ----------

    .. [1] "Solving multiclass learning problems via error-correcting output
       codes",
       Dietterich T., Bakiri G.,
       Journal of Artificial Intelligence Research 2,
       1995.

    .. [2] "The error coding method and PICTs",
       James G., Hastie T.,
       Journal of Computational and Graphical statistics 7,
       1998.

    .. [3] "The Elements of Statistical Learning",
       Hastie T., Tibshirani R., Friedman J., page 606 (second-edition)
       2008.
    """

    def __init__(self, estimator, code_length=1.5, decoder="hamm", random_state=None, n_jobs=1):
        self.estimator = estimator
        self.code_length = code_length
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.decoder = decoder

    def fit(self, X, y):
        """Fit underlying estimators.

        Parameters
        ----------
        X : (sparse) array-like, shape = [n_samples, n_features]
            Data.

        y : numpy array of shape [n_samples]
            Multi-class targets.

        Returns
        -------
        self
        """
        
        X, y = check_X_y(X, y)
        random_state = check_random_state(self.random_state)
        _check_estimator(self.estimator)

        if self.code_length <= 0:
            raise ValueError("code_length should be greater than {0}"
                             "".format(self.code_length))
            
        self.classes_ = np.unique(y)
        n_classes = self.classes_.shape[0]
        code_length_ = int(self.code_length)
        code_length_ = int(n_classes * self.code_length)

        # FIXME: I can use other codebook generation methods
        self.code_book_ = random_state.random_sample((n_classes, code_length_))
        self.code_book_[self.code_book_ > 0.5] = 1
        self.code_book_[self.code_book_ != 1] = 0

        classes_index = dict((c, i) for i, c in enumerate(self.classes_))

        Y = np.array([self.code_book_[classes_index[y[i]]]
                      for i in range(X.shape[0])], dtype=np.int)

        self.estimators_ = Parallel(n_jobs=self.n_jobs)(
            delayed(_fit_binary)(self.estimator, X, Y[:, i])
            for i in range(Y.shape[1]))

        return self


    def predict(self, X):
        """Predict multi-class targets using underlying estimators.

        Parameters
        ----------
        X : (sparse) array-like, shape = [n_samples, n_features]
            Data.

        Returns
        -------
        y : numpy array of shape [n_samples]
            Predicted multi-class targets.
        """
        check_is_fitted(self, 'estimators_')
        X = check_array(X)
        Y = np.array([_predict_binary(e, X) for e in self.estimators_]).T
        pred = _decode_binary(self.decoder, Y, self.code_book_)
        # print("________________________________________")
        # print("Created By: Prateek Kumar Goel")
        # print("Thank You for using ths ECOC Library")
        # print("________________________________________")
        return self.classes_[pred]
