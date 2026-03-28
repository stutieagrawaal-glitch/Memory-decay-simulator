# MEMORY DECAY SIMULATOR (MULTI-SUBJECT + REVISION SYSTEM)

import math
import matplotlib.pyplot as plt
import csv

# SUBJECT SETUP 
subjects = {}

num_subjects = int(input("Enter number of subjects to simulate: "))
for i in range(num_subjects):
    name = input(f"Enter name for subject {i+1}: ")
    subjects[name] = {
        "stm": 60.0,
        "ltm": 40.0,
        "reviews": 0,
        "last_revision_day": 0,
        "history": []
    }

# FUNCTIONS 
def get_valid_input(prompt, options):
    while True:
        user_input = input(prompt).lower()
        if user_input in options:
            return user_input
        print(f"Invalid input. Choose from {options}")

def calculate_decay_rate(base_decay, sleep_quality, emotion):
    sleep_effect = {"good": -0.03, "neutral": 0.0, "poor": 0.05}
    emotion_effect = {"happy": -0.02, "neutral": 0.0, "stressed": 0.04}

    decay_rate = base_decay
    decay_rate += sleep_effect[sleep_quality]
    decay_rate += emotion_effect[emotion]

    return max(decay_rate, 0.02)

def get_next_revision_gap(reviews):
    schedule = [1, 3, 7, 14, 30]
    return schedule[reviews] if reviews < len(schedule) else 30

# VARIABLES
base_decay = 0.10
csv_data = []

#SIMULATION
for i in range(1, 11):
    print(f"\n====== Day {i} ======")

    sleep_quality = get_valid_input(
        "Enter sleep quality (good/neutral/poor): ",
        ["good", "neutral", "poor"]
    )

    emotion = get_valid_input(
        "Enter emotional state (happy/neutral/stressed): ",
        ["happy", "neutral", "stressed"]
    )

    decay_rate = calculate_decay_rate(base_decay, sleep_quality, emotion)

    # LOOP THROUGH EACH SUBJECT
    for subject in subjects:
        print(f"\n📘 Subject: {subject}")

        revised_today = get_valid_input(
            f"Did you revise {subject}? (yes/no): ",
            ["yes", "no"]
        )

        stm = subjects[subject]["stm"]
        ltm = subjects[subject]["ltm"]

        # REVISION REMINDER
        gap = get_next_revision_gap(subjects[subject]["reviews"])
        last_day = subjects[subject]["last_revision_day"]

        if i - last_day >= gap:
            print(f"⚠️ Reminder: You should revise {subject} today!")

        # DECAY RATES
        stm_decay = decay_rate
        ltm_decay = decay_rate * 0.3

        # REVISION LOGIC
        if revised_today == "yes":
            stm += 15
            consolidation = 0.2 * stm
            stm -= consolidation
            ltm += consolidation

            subjects[subject]["reviews"] += 1
            subjects[subject]["last_revision_day"] = i
        else:
            stm -= 0.1 * stm

        # FORGETTING CURVE
        stm *= math.exp(-stm_decay)
        ltm *= math.exp(-ltm_decay)

        # LIMIT VALUES
        stm = max(0, min(stm, 70))
        ltm = max(0, min(ltm, 70))

        # SAVE BACK
        subjects[subject]["stm"] = stm
        subjects[subject]["ltm"] = ltm

        total_memory = stm + ltm
        subjects[subject]["history"].append(total_memory)

        print(
            f"STM: {round(stm,2)} | "
            f"LTM: {round(ltm,2)} | "
            f"Total: {round(total_memory,2)}"
        )

        # CSV
        csv_data.append([
            i, subject, sleep_quality, emotion,
            revised_today, round(stm, 2),
            round(ltm, 2), round(total_memory, 2)
        ])

# PLOTS
for subject in subjects:
    plt.plot(
        range(1, 11),
        subjects[subject]["history"],
        marker='o',
        label=subject
    )

plt.xlabel('Days')
plt.ylabel('Total Memory Strength')
plt.title('Memory Retention per Subject')
plt.axhline(y=50, linestyle='--')
plt.legend()
plt.show()

# CSV
with open('memory_decay_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(
        ['Day', 'Subject', 'Sleep', 'Emotion', 'Revision', 'STM', 'LTM', 'Total']
    )
    writer.writerows(csv_data)

# SUMMARY 
print("\n====== Final Summary ======")
for subject in subjects:
    stm = subjects[subject]["stm"]
    ltm = subjects[subject]["ltm"]
    print(f"{subject} → Final Memory: {round(stm + ltm, 2)}")

print("Data saved to memory_decay_data.csv")
