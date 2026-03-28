# Memory Decay Simulator with Machine Learning

## Overview

This project simulates how human memory changes over time using a combination of mathematical modeling and machine learning. It tracks short-term memory (STM) and long-term memory (LTM) across multiple subjects and incorporates factors such as sleep quality, emotional state, and revision habits.

The system not only simulates memory decay but also applies machine learning to predict future retention, recommend optimal revision timing, and analyze factors that influence learning.

---

## Features

### Memory Simulation

* Models short-term and long-term memory dynamics
* Uses exponential decay to simulate forgetting
* Incorporates revision-based consolidation from STM to LTM

### Machine Learning Modules

1. **Memory Retention Prediction**

   * Uses Linear Regression to predict future memory levels
   * Forecasts memory for upcoming days

2. **Optimal Revision Recommendation**

   * Suggests the best day to revise a subject
   * Compares ML-based recommendation with traditional spaced repetition

3. **Feature Impact Analysis**

   * Uses Random Forest to determine importance of factors like sleep and emotion
   * Identifies which variables most influence memory retention

---

## How It Works

1. User inputs:

   * Number of subjects
   * Daily sleep quality
   * Emotional state
   * Whether revision was done

2. The simulator:

   * Updates STM and LTM values daily
   * Applies decay and consolidation rules
   * Stores data for machine learning

3. Machine learning models:

   * Train on generated data during runtime
   * Predict future memory values
   * Recommend revision schedules

---

## Technologies Used

* Python
* NumPy
* Matplotlib
* Scikit-learn

---

## Output

* Console output with daily memory values
* Predicted future memory trends
* Recommended revision days
* Feature importance analysis
* Saved files:

  * `memory_decay_data.csv`
  * `memory_ml_output.png`

---

## Project Structure

```
memory-decay-ml/
│
├── memory.py
├── memory_decay_data.csv
├── memory_ml_output.png
└── README.md
```

---

## Example Use Case

This project can be used as a study planning tool:

* Track how well you retain different subjects
* Understand how lifestyle factors affect learning
* Get personalized revision recommendations

---

## Limitations

* Data is synthetically generated during simulation
* Model performance depends on the amount of simulated data
* Real-world accuracy can be improved with real user data

---

## Future Improvements

* Add real user data collection
* Build a graphical interface (e.g., using Streamlit)
* Improve prediction models with more advanced algorithms
* Implement personalized learning profiles

---

## Conclusion

This project demonstrates how machine learning can be integrated into a simulation system to create intelligent, data-driven recommendations. It bridges theoretical concepts like memory decay with practical applications in study optimization.

---

## Author

Stutie Agrawaal
