from itertools import combinations

# ----------------------------
# B. Dataset
# ----------------------------
transactions = [
    ['Milk', 'Bread', 'Butter'],
    ['Bread', 'Butter'],
    ['Milk', 'Bread'],
    ['Milk', 'Butter'],
    ['Bread', 'Butter'],
    ['Milk', 'Bread', 'Butter']
]

print("Total Transactions:", len(transactions))

# ----------------------------
# C. Generate Itemsets + Support
# ----------------------------

def calculate_support(itemset, transactions):
    count = 0
    for transaction in transactions:
        if set(itemset).issubset(set(transaction)):
            count += 1
    return count / len(transactions)

# Generate unique 1-itemsets
items = set()
for transaction in transactions:
    for item in transaction:
        items.add(item)

print("Unique Items:", items)

min_support = 0.5

# ----------------------------
# D. Apriori Algorithm
# ----------------------------

def apriori(transactions, min_support):
    frequent_itemsets = {}

    # Step 1: Generate 1-itemsets
    current_itemsets = [{item} for item in items]

    k = 1

    while current_itemsets:
        freq_k = []

        for itemset in current_itemsets:
            supp = calculate_support(itemset, transactions)
            if supp >= min_support:
                frequent_itemsets[frozenset(itemset)] = supp
                freq_k.append(itemset)

        # Generate k+1 itemsets
        k += 1
        current_itemsets = []
        for i in range(len(freq_k)):
            for j in range(i+1, len(freq_k)):
                union_set = freq_k[i] | freq_k[j]
                if len(union_set) == k:
                    current_itemsets.append(union_set)

    return frequent_itemsets

frequent_itemsets = apriori(transactions, min_support)

print("\nFrequent Itemsets:")
for itemset, supp in frequent_itemsets.items():
    print(set(itemset), "Support:", round(supp, 2))

# ----------------------------
# E. Generate Association Rules
# ----------------------------

def generate_rules(frequent_itemsets, min_confidence=0.7):
    rules = []

    for itemset in frequent_itemsets:
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent

                    support_itemset = frequent_itemsets[itemset]
                    support_antecedent = frequent_itemsets[antecedent]

                    confidence = support_itemset / support_antecedent

                    if confidence >= min_confidence:
                        lift = confidence / frequent_itemsets[consequent]

                        rules.append((set(antecedent),
                                      set(consequent),
                                      support_itemset,
                                      confidence,
                                      lift))
    return rules

rules = generate_rules(frequent_itemsets, min_confidence=0.7)

# ----------------------------
# F. Evaluation of Rules
# ----------------------------

print("\nStrong Association Rules:")
for antecedent, consequent, support, confidence, lift in rules:
    print(f"{antecedent} → {consequent}")
    print(f"Support: {round(support,2)}, "
          f"Confidence: {round(confidence,2)}, "
          f"Lift: {round(lift,2)}\n")
