# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

# Import libraries
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import TSNE
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
import numpy as np

# Load Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Dimensionality reduction
X_pca = PCA(n_components=3).fit_transform(X)
X_lda = LDA(n_components=2).fit_transform(X, y)  # LDA max components = 2
X_tsne = TSNE(n_components=3, random_state=42).fit_transform(X)
X_svd = TruncatedSVD(n_components=3, random_state=42).fit_transform(X)

# Classifier
clf = LogisticRegression(max_iter=200)

# Function to compute CV mean & std
def get_cv_scores(X_transformed, y):
    scores = cross_val_score(clf, X_transformed, y, cv=5)
    return np.mean(scores), np.std(scores)

# Compute CV scores
mean_pca, std_pca = get_cv_scores(X_pca, y)
mean_lda, std_lda = get_cv_scores(X_lda, y)
mean_tsne, std_tsne = get_cv_scores(X_tsne, y)
mean_svd, std_svd = get_cv_scores(X_svd, y)

# Display results
print("5-Fold CV Accuracy (mean ± std) for 3 features:")
print(f"PCA: {mean_pca:.3f} ± {std_pca:.3f}")
print(f"LDA: {mean_lda:.3f} ± {std_lda:.3f} (Note: only 2 features for LDA)")
print(f"t-SNE: {mean_tsne:.3f} ± {std_tsne:.3f}")
print(f"SVD: {mean_svd:.3f} ± {std_svd:.3f}")
