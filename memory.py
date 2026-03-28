# Memory Decay Simulator with Machine Learning (Multi Subject + Revision System)

import math
import csv
import warnings
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error

warnings.filterwarnings("ignore")

# Subject setup
subjects = {}

num_subjects = int(input("Enter number of subjects to simulate: "))
for i in range(num_subjects):
    name = input(f"Enter name for subject {i+1}: ")
    subjects[name] = {
        "stm": 60.0,
        "ltm": 40.0,
        "reviews": 0,
        "last_revision_day": 0,
        "history": [],
        "feature_rows": []
    }

# Helper functions
def get_valid_input(prompt, options):
    while True:
        user_input = input(prompt).lower()
        if user_input in options:
            return user_input
        print(f"Invalid input. Choose from {options}")

def calculate_decay_rate(base_decay, sleep_quality, emotion):
    sleep_effect = {"good": -0.03, "neutral": 0.0, "poor": 0.05}
    emotion_effect = {"happy": -0.02, "neutral": 0.0, "stressed": 0.04}
    rate = base_decay + sleep_effect[sleep_quality] + emotion_effect[emotion]
    return max(rate, 0.02)

def get_next_revision_gap(reviews):
    schedule = [1, 3, 7, 14, 30]
    return schedule[reviews] if reviews < len(schedule) else 30

# Encoders
sleep_enc = LabelEncoder().fit(["good", "neutral", "poor"])
emotion_enc = LabelEncoder().fit(["happy", "neutral", "stressed"])

def encode_row(sleep, emotion, revised, stm, ltm, reviews, days_since_rev):
    return [
        sleep_enc.transform([sleep])[0],
        emotion_enc.transform([emotion])[0],
        1 if revised == "yes" else 0,
        stm,
        ltm,
        reviews,
        days_since_rev
    ]

# Simulation
base_decay = 0.10
csv_data = []
all_feature_rows = []
all_targets = []

for day in range(1, 11):
    print(f"\nDay {day}")

    sleep = get_valid_input("Sleep quality (good/neutral/poor): ", ["good", "neutral", "poor"])
    emotion = get_valid_input("Emotional state (happy/neutral/stressed): ", ["happy", "neutral", "stressed"])
    decay = calculate_decay_rate(base_decay, sleep, emotion)

    for subject in subjects:
        print(f"\nSubject: {subject}")

        revised = get_valid_input(f"Did you revise {subject}? (yes/no): ", ["yes", "no"])

        stm = subjects[subject]["stm"]
        ltm = subjects[subject]["ltm"]
        reviews = subjects[subject]["reviews"]
        last_day = subjects[subject]["last_revision_day"]

        days_since_rev = day - last_day
        gap = get_next_revision_gap(reviews)

        if days_since_rev >= gap:
            print(f"Reminder: revise {subject} today")

        stm_decay = decay
        ltm_decay = decay * 0.3

        if revised == "yes":
            stm += 15
            consolidation = 0.2 * stm
            stm -= consolidation
            ltm += consolidation
            subjects[subject]["reviews"] += 1
            subjects[subject]["last_revision_day"] = day
        else:
            stm -= 0.1 * stm

        stm *= math.exp(-stm_decay)
        ltm *= math.exp(-ltm_decay)

        stm = max(0, min(stm, 70))
        ltm = max(0, min(ltm, 70))

        subjects[subject]["stm"] = stm
        subjects[subject]["ltm"] = ltm

        total = stm + ltm
        subjects[subject]["history"].append(total)

        row = encode_row(
            sleep, emotion, revised,
            stm, ltm,
            subjects[subject]["reviews"],
            days_since_rev
        )

        subjects[subject]["feature_rows"].append((row, total))
        all_feature_rows.append(row)
        all_targets.append(total)

        print(f"STM: {stm:.2f} | LTM: {ltm:.2f} | Total: {total:.2f}")

        csv_data.append([
            day, subject, sleep, emotion,
            revised, round(stm, 2),
            round(ltm, 2), round(total, 2)
        ])

# ML Module 1: Retention prediction
print("\nMemory Retention Prediction")

prediction_results = {}

for subject in subjects:
    rows = subjects[subject]["feature_rows"]
    if len(rows) < 4:
        print(f"{subject}: not enough data")
        continue

    X = np.array([r[0] for r in rows])
    y = np.array([r[1] for r in rows])

    split = max(2, len(X) - 2)
    X_tr, X_te = X[:split], X[split:]
    y_tr, y_te = y[:split], y[split:]

    model = LinearRegression()
    model.fit(X_tr, y_tr)

    if len(X_te) > 0:
        y_pred = model.predict(X_te)
        mae = mean_absolute_error(y_te, y_pred)

        print(f"\n{subject}")
        for i, (actual, pred) in enumerate(zip(y_te, y_pred), start=split + 1):
            print(f"Day {i}: Actual={actual:.2f}, Predicted={pred:.2f}")
        print(f"Mean Absolute Error: {mae:.2f}")

    last_row = X[-1].copy().reshape(1, -1)
    future_preds = []

    for _ in range(5):
        pred_val = float(model.predict(last_row)[0])
        future_preds.append(max(0, min(pred_val, 140)))

        last_row[0][3] = max(0, last_row[0][3] - 2)
        last_row[0][4] = max(0, last_row[0][4] - 0.5)

    prediction_results[subject] = future_preds

# ML Module 2: Revision recommendation
print("\nOptimal Revision Recommendation")

for subject in subjects:
    rows = subjects[subject]["feature_rows"]
    if len(rows) < 4:
        continue

    X = np.array([r[0] for r in rows])
    y = np.array([r[1] for r in rows])

    model = LinearRegression().fit(X, y)

    best_day = None
    best_pred = -1

    base_row = X[-1].copy()

    for future_day in range(11, 16):
        for rev in [0, 1]:
            test_row = base_row.copy()
            test_row[2] = rev
            test_row[6] = future_day - 10

            pred = float(model.predict([test_row])[0])

            if rev == 1 and pred > best_pred:
                best_pred = pred
                best_day = future_day

    print(f"{subject}: revise on day {best_day}")

# ML Module 3: Feature importance
print("\nSleep and Emotion Impact Analysis")

if len(all_feature_rows) >= 6:
    X_all = np.array(all_feature_rows)
    y_all = np.array(all_targets)

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_all, y_all)

    feature_names = [
        "Sleep", "Emotion", "Revised",
        "STM", "LTM", "Reviews", "Days Since Revision"
    ]

    importances = rf.feature_importances_
    ranked = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)

    for name, imp in ranked:
        print(f"{name}: {imp:.3f}")

# Plotting
fig, ax = plt.subplots(figsize=(10, 5))

for subject in subjects:
    history = subjects[subject]["history"]
    days = range(1, len(history) + 1)
    ax.plot(days, history, marker='o', label=subject)

ax.set_xlabel("Day")
ax.set_ylabel("Memory Strength")
ax.set_title("Memory Retention")
ax.legend()
plt.show()

# Save CSV
with open("memory_decay_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Day", "Subject", "Sleep", "Emotion", "Revision", "STM", "LTM", "Total"])
    writer.writerows(csv_data)

# Final summary
print("\nFinal Summary")
for subject in subjects:
    total = subjects[subject]["stm"] + subjects[subject]["ltm"]
    print(f"{subject}: {total:.2f}")
