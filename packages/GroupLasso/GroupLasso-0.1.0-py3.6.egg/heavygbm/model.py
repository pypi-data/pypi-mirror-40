import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import log_loss, mean_squared_error
import pandas as pd

from .util import sigmoid, sum_gradient, sum_hessian


class HGBMRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, random_state=None, n_estimators=100,
                 max_depth=3, learning_rate=0.1, lam_l2=0,
                 min_child_samples=20,
                 verbose=True):
        self._rng = np.random.RandomState(random_state)
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.lam_l2 = lam_l2
        self.min_child_samples = min_child_samples
        self.verbose = verbose
        self.estimators_ = []
        self.unique_paths = []
        self._losses = []

    def fit(self, X, y):
        if isinstance(X, pd.DataFrame):
            X = X.values

        if isinstance(y, pd.Series):
            y = y.values

        # リストオブジェクトを空にする
        lst_attributes = ['estimators_', 'unique_paths', '_losses']
        for attribute in lst_attributes:
            if getattr(self, attribute):
                getattr(self, attribute).clear()

        M = self.n_estimators
        score = np.zeros_like(y, dtype=np.float64)
        for _ in range(M):
            resid = y - score

            tree = DecisionTreeRegressor(
                random_state=self._rng,
                max_depth=self.max_depth,
                min_samples_leaf=self.min_child_samples
            )
            tree.fit(X, resid)

            leaf_indices = tree.apply(X)
            df = pd.DataFrame({"leaf_index": leaf_indices, "y": y})
            lst = []
            for leaf_index, v in df.groupby("leaf_index"):
                target_score = score[v.index.values]
                target_y = v['y'].values
                gamma = - sum_gradient['mse'](target_y, target_score) / \
                    (sum_hessian['mse'](target_score) + self.lam_l2)
                new_value = gamma * self.learning_rate
                score[v.index.values] += new_value
                lst.append([leaf_index, new_value])

            unique_path = pd.DataFrame(lst).rename(
                columns={0: "leaf_index", 1: "value"})
            if self.verbose:
                loss = mean_squared_error(y, score)
                print("training loss:", loss)
                self._losses.append(loss)

            self.estimators_.append(tree)
            self.unique_paths.append(unique_path)

    def predict(self, X):
        score_all = np.zeros(len(X), dtype=np.float64)
        for unique_path, tree in zip(self.unique_paths, self.estimators_):
            leaf_indices = pd.DataFrame(tree.apply(X)).rename(
                columns={0: "leaf_index"})
            score = leaf_indices.merge(unique_path, how="left")['value']
            score_all += score

        return score_all


class HGBMClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, random_state=None, n_estimators=100,
                 max_depth=3, learning_rate=0.1, lam_l2=0,
                 min_child_samples=20,
                 verbose=True):
        self._rng = np.random.RandomState(random_state)
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.lam_l2 = lam_l2
        self.min_child_samples = min_child_samples
        self.verbose = verbose
        self.estimators_ = []
        self.unique_paths = []
        self._losses = []

    def fit(self, X, y):
        if isinstance(X, pd.DataFrame):
            X = X.values

        if isinstance(y, pd.Series):
            y = y.values

        # リストオブジェクトを空にする
        lst_attributes = ['estimators_', 'unique_paths', '_losses']
        for attribute in lst_attributes:
            if getattr(self, attribute):
                getattr(self, attribute).clear()

        # binary classification
        assert ((y == 0) | (y == 1)).all()
        M = self.n_estimators
        score = np.zeros_like(y, dtype=np.float64)
        proba = sigmoid(score)
        for _ in range(M):
            resid = y - proba

            tree = DecisionTreeRegressor(
                random_state=self._rng,
                max_depth=self.max_depth,
                min_samples_leaf=self.min_child_samples
            )
            tree.fit(X, resid)

            leaf_indices = tree.apply(X)
            df = pd.DataFrame({"leaf_index": leaf_indices, "y": y})
            lst = []
            for leaf_index, v in df.groupby("leaf_index"):
                target_proba = proba[v.index.values]
                target_y = v['y'].values
                gamma = - sum_gradient['xentropy'](target_y, target_proba) / \
                    (sum_hessian['xentropy'](target_proba) + self.lam_l2)
                new_value = gamma * self.learning_rate
                score[v.index.values] += new_value
                lst.append([leaf_index, new_value])

            unique_path = pd.DataFrame(lst).rename(
                columns={0: "leaf_index", 1: "value"})
            proba = sigmoid(score)
            if self.verbose:
                loss = log_loss(y, proba)
                print("training loss:", loss)
                self._losses.append(loss)

            self.estimators_.append(tree)
            self.unique_paths.append(unique_path)

    def predict_proba(self, X):
        score_all = np.zeros(len(X), dtype=np.float64)
        proba = np.zeros((len(X), 2), dtype=np.float64)
        for unique_path, tree in zip(self.unique_paths, self.estimators_):
            leaf_indices = pd.DataFrame(tree.apply(X)).rename(
                columns={0: "leaf_index"})
            score = leaf_indices.merge(unique_path, how="left")['value']
            score_all += score

        proba[:, 1] = sigmoid(score_all)
        proba[:, 0] = 1 - proba[:, 1]
        return proba

    def predict(self, X):
        proba = self.predict_proba(X)
        return (proba[:, 1] > 0.5).astype(int)
