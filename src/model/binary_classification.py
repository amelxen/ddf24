import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
<<<<<<< HEAD
<<<<<<< HEAD
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
=======
from sklearn.metrics import precision_score
>>>>>>> 2cfebcc (some ref)
=======
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
>>>>>>> 10ce618 (some ref...)


def generate_synthetic(size, dim=6, noise=0.1):
    X = np.random.randn(size, dim)
    w = np.random.randn(dim + 1)
    noise = noise * np.random.randn(size)
    y = np.heaviside(X.dot(w[1:]) + w[0] + noise, 0)
    return X, y


def load_data(path="data.csv"):
    data = pd.read_csv(path, delimiter=",")
    X = np.array(data[data.columns[1:-1]])
    y = np.array(data[data.columns[-1]])
    return X, y


class BinClassifier:

    def __init__(self, X, y, model="rfc"):
        match model:
            case "rfc":
                param_grid = {
                    "n_estimators": [50, 100, 150],
                    "max_depth": [None, 10, 20],
                    "min_samples_leaf": [1, 2, 4],
                }
                grid_search = GridSearchCV(
                    RandomForestClassifier(), param_grid, refit=True, cv=5
                )
                grid_search.fit(X, y)
                self.model = RandomForestClassifier(
                    n_estimators=grid_search.best_params_["n_estimators"],
                    max_depth=grid_search.best_params_["max_depth"],
                    min_samples_leaf=grid_search.best_params_["min_samples_leaf"],
                )
                # print(grid_search.best_score_)

            case "svc":
                self.model = SVC()
                param_grid = {
                    "C": [0.1, 1, 10, 100, 1000],
                    "gamma": [1, 0.1, 0.01, 0.001, 0.0001],
                    "kernel": ["linear", "rbf"],
                }

                grid_search = GridSearchCV(SVC(), param_grid, refit=True, cv=5)
                grid_search.fit(X, y)
                self.model = SVC(
                    C=grid_search.best_params_["C"],
                    gamma=grid_search.best_params_["gamma"],
                    kernel=grid_search.best_params_["kernel"],
                )

                # print(grid_search.best_score_)

            case _:
                raise ValueError("Incorrect parameters were passed to the model")

        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)


if __name__ == "__main__":
    # X, y = generate_synthetic(3000, dim=6)
    X, y = load_data("C:\\vscode_projects\\yandex_plag\\ddf24\\test1.csv")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(len(y_train), np.sum(y_train))
    model = BinClassifier(X_train, y_train, "rfc")
    y_pred = model.predict(X_test)
    print("pres=", precision_score(y_test, y_pred))
    print("rec=", recall_score(y_test, y_pred))
    print("f1=", f1_score(y_test, y_pred))
    print("acc=", accuracy_score(y_test, y_pred))
