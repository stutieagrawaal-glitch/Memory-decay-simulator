# MEMORY DECAY SIMULATOR (STM vs LTM)
import math
import matplotlib.pyplot as plt
import csv

#FUNCTIONS
def get_valid_input(prompt, options):
    while True:
        user_input = input(prompt).lower()
        if user_input in options:
            return user_input
        print(f"Invalid input. Choose from {options}")

def calculate_decay_rate(base_decay, sleep_quality, emotion):
    sleep_effect = {
        "good": -0.03,
        "neutral": 0.0,
        "poor": 0.05
    }

    emotion_effect = {
        "happy": -0.02,
        "neutral": 0.0,
        "stressed": 0.04
    }

    decay_rate = base_decay
    decay_rate += sleep_effect[sleep_quality]
    decay_rate += emotion_effect[emotion]

    return max(decay_rate, 0.02)

#VARIABLES
stm = 60.0   # Short-term memory
ltm = 40.0   # Long-term memory
base_decay = 0.10

days = []
memory_strength = []
days_with_revision = []
days_without_revision = []
memory_with_revision = []
memory_without_revision = []
csv_data = []
stm_values = []
ltm_values = []


#SIMULATION
for i in range(1, 11):
    print(f"\nDay {i}")

    sleep_quality = get_valid_input(
        "Enter sleep quality (good/neutral/poor): ",
        ["good", "neutral", "poor"]
    )

    emotion = get_valid_input(
        "Enter emotional state (happy/neutral/stressed): ",
        ["happy", "neutral", "stressed"]
    )

    revised_today = get_valid_input(
        "Did you revise today? (yes/no): ",
        ["yes", "no"]
    )

    decay_rate = calculate_decay_rate(base_decay, sleep_quality, emotion)

    # Separate decay rates
    stm_decay = decay_rate            # fast forgetting
    ltm_decay = decay_rate * 0.3      # slow forgetting

    # REVISION LOGIC
    if revised_today == "yes":
        stm += 15                              # revision boosts STM
        consolidation = 0.2 * stm              # STM → LTM
        stm -= consolidation
        ltm += consolidation
    else:
        stm -= 0.1 * stm                       # STM fades quickly

    #FORGETTING CURVE
    stm *= math.exp(-stm_decay)
    ltm *= math.exp(-ltm_decay)

    # Keep values realistic
    stm = max(0, min(stm, 70))
    ltm = max(0, min(ltm, 70))
    stm_values.append(stm)
    ltm_values.append(ltm)

    total_memory = stm + ltm

    print(
        f"STM: {round(stm,2)} | "
        f"LTM: {round(ltm,2)} | "
        f"Total: {round(total_memory,2)}"
    )

    days.append(i)
    memory_strength.append(total_memory)

    if revised_today == "yes":
        days_with_revision.append(i)
        memory_with_revision.append(total_memory)
    else:
        days_without_revision.append(i)
        memory_without_revision.append(total_memory)

    csv_data.append([
        i,
        sleep_quality,
        emotion,
        revised_today,
        round(stm, 2),
        round(ltm, 2),
        round(total_memory, 2)
    ])

# PLOTS 
# Memory Decay Over Time
plt.plot(days, memory_strength, marker='o')
plt.xlabel('Days')
plt.ylabel('Total Memory Strength')
plt.title('Memory Decay Over Time (STM + LTM)')
plt.axhline(y=50, linestyle='--', label='Threshold')
plt.legend()
plt.show()

# Revision Comparison
plt.plot(days_with_revision, memory_with_revision, label='With Revision', marker='o')
plt.plot(days_without_revision, memory_without_revision, label='Without Revision', marker='x')
plt.xlabel('Days')
plt.ylabel('Total Memory Strength')
plt.title('Revision Comparison')
plt.axhline(y=50, linestyle='--')
plt.legend()
plt.show()

# STM vs LTM Comparison
plt.plot(days, stm_values, label='Short-Term Memory (STM)', marker='o')
plt.plot(days, ltm_values, label='Long-Term Memory (LTM)', marker='s')
plt.xlabel('Days')
plt.ylabel('Memory Strength')
plt.title('Short-Term vs Long-Term Memory Over Time')
plt.axhline(y=50, linestyle='--', label='Threshold')
plt.legend()
plt.show()


# CSV
with open('memory_decay_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(
        ['Day', 'Sleep', 'Emotion', 'Revision', 'STM', 'LTM', 'Total Memory']
    )
    writer.writerows(csv_data)

#SUMMARY
print("\nSimulation Summary")
print("Final STM:", round(stm, 2))
print("Final LTM:", round(ltm, 2))
print("Final total memory:", round(stm + ltm, 2))
print("Days with revision:", len(days_with_revision))
print("Days without revision:", len(days_without_revision))
print("Data saved to memory_decay_data.csv")
