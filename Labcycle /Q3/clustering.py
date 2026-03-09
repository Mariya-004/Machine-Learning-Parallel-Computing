# =========================
# Supermarket Sales Clustering
# =========================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

import warnings
warnings.filterwarnings('ignore')

# -------------------------
# 1. Load Dataset
# -------------------------
df = pd.read_csv("supermarket_sales - Sheet1.csv")
print("Dataset shape:", df.shape)
print(df.head())

# -------------------------
# 2. Encode Categorical Variables
# -------------------------
# Encode Gender (Male=0, Female=1)
df['Gender'] = df['Gender'].map({'Male':0, 'Female':1})

# -------------------------
# 3. Select Features for Clustering
# -------------------------
# Keep only numeric columns
numeric_features = df.select_dtypes(include=np.number)
features = numeric_features.copy()
print("Features used for clustering:\n", features.head())

# -------------------------
# 4. Standardize Features
# -------------------------
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# -------------------------
# 5. Elbow Method to Find Optimal k
# -------------------------
wcss = []
K = range(1, 11)

for k in K:
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(scaled_features)
    wcss.append(km.inertia_)

plt.figure(figsize=(8,4))
plt.plot(K, wcss, 'bo-')
plt.title("Elbow Method For Optimal k")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS (Inertia)")
plt.show()

# -------------------------
# 6. Fit K-Means with Optimal k
# -------------------------
k_optimal = 4  # change based on Elbow plot
kmeans = KMeans(n_clusters=k_optimal, random_state=42)
clusters = kmeans.fit_predict(scaled_features)

df['Cluster'] = clusters

# -------------------------
# 7. Cluster Summary
# -------------------------
# Compute mean only for numeric columns
numeric_cols = df.select_dtypes(include=np.number).columns
cluster_summary = df.groupby('Cluster')[numeric_cols].mean()
print("\nCluster Summary:\n", cluster_summary)

# -------------------------
# 8. PCA for 2D Visualization
# -------------------------
pca = PCA(n_components=2)
pca_features = pca.fit_transform(scaled_features)

df['pca1'] = pca_features[:,0]
df['pca2'] = pca_features[:,1]

plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='pca1', y='pca2', hue='Cluster', palette='viridis', s=60)
plt.title("K-Means Clusters Visualization (PCA)")
plt.show()
