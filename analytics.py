import subprocess

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score
from sklearn import tree
data = pd.read_csv("gameData_encoded.csv", sep=",")
X = data.values[:, 0:3]
Y = data.values[:, 4]
features = list(data.columns[:3])

clf_gini = DecisionTreeClassifier(criterion = "gini", random_state = 100, max_depth=3, min_samples_leaf=5)
print(clf_gini.fit(X,Y))

with open("classifier.txt", "w") as f:
    f = tree.export_graphviz(clf_gini, out_file=f)

