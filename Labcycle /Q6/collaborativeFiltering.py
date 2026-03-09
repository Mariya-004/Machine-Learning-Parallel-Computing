# ---------------------------------------------
# COLLABORATIVE FILTERING & HYBRID RECOMMENDER
# Single Cell Complete Implementation
# ---------------------------------------------

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import precision_score, recall_score, f1_score

# ---------------------------------------------
# 1. Create Sample User-Item Rating Matrix
# Rows -> Users
# Columns -> Items (Movies)
# 0 indicates item not rated
# ---------------------------------------------

ratings = pd.DataFrame({
    'Movie1': [5, 4, 1, 0],
    'Movie2': [3, 0, 1, 0],
    'Movie3': [0, 0, 0, 5],
    'Movie4': [1, 1, 5, 4]
}, index=['User1', 'User2', 'User3', 'User4'])

print("User-Item Rating Matrix:\n")
print(ratings)

# ---------------------------------------------
# 2. USER-BASED COLLABORATIVE FILTERING
# ---------------------------------------------

# Compute similarity between users using cosine similarity
user_similarity = cosine_similarity(ratings)
user_sim_df = pd.DataFrame(user_similarity,
                           index=ratings.index,
                           columns=ratings.index)

# Function to predict rating using User-Based CF
def predict_user_based(user, item):
    sim_users = user_sim_df[user]
    numerator, denominator = 0, 0

    for other_user in ratings.index:
        if ratings.loc[other_user, item] > 0 and other_user != user:
            numerator += sim_users[other_user] * ratings.loc[other_user, item]
            denominator += abs(sim_users[other_user])

    return numerator / denominator if denominator != 0 else 0

# ---------------------------------------------
# 3. ITEM-BASED COLLABORATIVE FILTERING
# ---------------------------------------------

# Compute similarity between items
item_similarity = cosine_similarity(ratings.T)
item_sim_df = pd.DataFrame(item_similarity,
                           index=ratings.columns,
                           columns=ratings.columns)

# Function to predict rating using Item-Based CF
def predict_item_based(user, item):
    sim_items = item_sim_df[item]
    user_ratings = ratings.loc[user]
    numerator, denominator = 0, 0

    for i in ratings.columns:
        if user_ratings[i] > 0 and i != item:
            numerator += sim_items[i] * user_ratings[i]
            denominator += abs(sim_items[i])

    return numerator / denominator if denominator != 0 else 0

# ---------------------------------------------
# 4. HYBRID RECOMMENDER SYSTEM
# Weighted combination of User-Based and Item-Based
# ---------------------------------------------

def hybrid_prediction(user, item, alpha=0.5):
    user_pred = predict_user_based(user, item)
    item_pred = predict_item_based(user, item)
    return alpha * user_pred + (1 - alpha) * item_pred

# ---------------------------------------------
# 5. EVALUATION USING PRECISION, RECALL, F1
# We consider rating >= 3 as "Relevant"
# ---------------------------------------------

def evaluate_model(predict_function):
    actual = []
    predicted = []

    for user in ratings.index:
        for item in ratings.columns:
            if ratings.loc[user, item] > 0:
                actual.append(1 if ratings.loc[user, item] >= 3 else 0)
                pred_rating = predict_function(user, item)
                predicted.append(1 if pred_rating >= 3 else 0)

    precision = precision_score(actual, predicted)
    recall = recall_score(actual, predicted)
    f1 = f1_score(actual, predicted)

    return precision, recall, f1

# Evaluate User-Based CF
ub_precision, ub_recall, ub_f1 = evaluate_model(predict_user_based)

# Evaluate Item-Based CF
ib_precision, ib_recall, ib_f1 = evaluate_model(predict_item_based)

# Evaluate Hybrid CF
hy_precision, hy_recall, hy_f1 = evaluate_model(hybrid_prediction)

# ---------------------------------------------
# 6. Display Results
# ---------------------------------------------

print("\nPerformance Comparison:")
print("---------------------------------")
print("User-Based CF  -> Precision:", round(ub_precision,2),
      "Recall:", round(ub_recall,2),
      "F1:", round(ub_f1,2))

print("Item-Based CF  -> Precision:", round(ib_precision,2),
      "Recall:", round(ib_recall,2),
      "F1:", round(ib_f1,2))

print("Hybrid CF      -> Precision:", round(hy_precision,2),
      "Recall:", round(hy_recall,2),
      "F1:", round(hy_f1,2))

# ---------------------------------------------
# End of Single Cell Implementation
# ---------------------------------------------
