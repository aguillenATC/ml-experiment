from typing import *
from modelling.utils.data import UnifiedDataLoader, SEED
import numpy as np
from ml_experiment import experiment
from sklearn.svm import LinearSVC
from sklearn.kernel_approximation import Nystroem


@experiment(data_loader=UnifiedDataLoader)
def main(C: float = 1.0, kernel: str = 'rbf', degree: int = 3, gamma: Any = 'scale'):
    np.random.seed(SEED)
    X_train, X_val, y_train, y_val = UnifiedDataLoader.load_data()

    if isinstance(gamma, str):
        if gamma == 'scale':
            gamma = 1.0 / (X_train.shape[1] * X_train.var())
        if gamma == 'auto':
            gamma = 1.0 / X_train.shape[1]

    if kernel != 'linear':
        degree = degree if kernel == 'poly' else None
        feature_map = Nystroem(kernel=kernel, gamma=gamma, degree=degree)
        X_train = feature_map.fit_transform(X_train)
        X_val = feature_map.transform(X_val)

    model = LinearSVC(C=C)
    model.fit(X_train, y_train)
    accuracy = model.score(X_val, y_val)
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()