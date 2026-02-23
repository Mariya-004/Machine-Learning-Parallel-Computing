# Simple Single-Cell Code: Feature Selection on Iris Dataset

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# a. Load dataset
iris = load_iris()
X, y = iris.data, iris.target
features = iris.feature_names

df = pd.DataFrame(X, columns=features)
df['target'] = y

# b. EDA
print(df.info())
print(df.describe())
print(df['target'].value_counts())

df['class'] = df['target'].map({0:'Setosa', 1:'Versicolor', 2:'Virginica'})
sns.pairplot(df, hue='class', palette='Set1')
plt.show()

# c-a. Univariate Feature Selection
uni = SelectKBest(f_classif, k=2)
X_uni = uni.fit_transform(X, y)
print("Univariate Features:", [features[i] for i in uni.get_support(indices=True)])

# c-b. Random Forest Feature Importance
rf = RandomForestClassifier(random_state=42)
rf.fit(X, y)
print("RF Feature Importance:", rf.feature_importances_)

# c-c. RFE with SVM
rfe = RFE(SVC(kernel='linear'), n_features_to_select=2)
X_rfe = rfe.fit_transform(X, y)
print("RFE Features:", [features[i] for i in rfe.get_support(indices=True)])

# d. Model Evaluation (SVM)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
svm = SVC()
svm.fit(X_train, y_train)
acc_full = accuracy_score(y_test, svm.predict(X_test))

X_train_u, X_test_u, _, _ = train_test_split(X_uni, y, test_size=0.3, random_state=42)
svm.fit(X_train_u, y_train)
acc_uni = accuracy_score(y_test, svm.predict(X_test_u))

# e. Comparison
print("Accuracy (All Features):", acc_full)
print("Accuracy (Selected Features):", acc_uni)
