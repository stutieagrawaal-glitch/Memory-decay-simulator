# Memory Decay Simulator (STM vs LTM)

This project simulates how **short-term memory (STM)** and **long-term memory (LTM)** change over time based on daily factors such as **sleep quality**, **emotional state**, and **revision habits**. It is a simple educational model inspired by cognitive psychology concepts like the **forgetting curve** and **memory consolidation**.

---

## Features

* Simulates memory strength over **10 days**
* Separates **STM (fast decay)** and **LTM (slow decay)**
* Models the impact of:

  * Sleep quality (good / neutral / poor)
  * Emotional state (happy / neutral / stressed)
  * Revision (yes / no)
* Visualizes results using **matplotlib**
* Exports daily results to a **CSV file**

---

## How the Simulation Works

1. Each day, the user inputs:

   * Sleep quality
   * Emotional state
   * Whether revision was done
2. A decay rate is calculated based on sleep and emotion.
3. STM and LTM decay at different speeds:

   * STM decays faster
   * LTM decays slower
4. If revision is done:

   * STM receives a boost
   * A portion of STM is consolidated into LTM
5. Results are recorded, plotted, and saved.

---

## Visualizations

The program generates three plots:

1. **Total Memory Over Time** (STM + LTM)
2. **Revision Comparison** (days with vs without revision)
3. **STM vs LTM Over Time**

A threshold line (memory strength = 50) is included for reference.

---

## Output Files

* `memory_decay_data.csv` – contains daily simulation data:

  * Day
  * Sleep quality
  * Emotional state
  * Revision
  * STM value
  * LTM value
  * Total memory strength

---

## Requirements

* Python 3.x
* Required libraries:

  ```
  math
  matplotlib
  csv
  ```

Install matplotlib if needed:

```
pip install matplotlib
```

---

## How to Run

1. Clone or download the project
2. Run the script:

   ```
   python memory.py
   ```
3. Follow the prompts for each day
4. View the plots and generated CSV file

---

## Educational Purpose

This project is designed for:

* Learning about memory decay and consolidation
* Demonstrating how lifestyle factors affect learning
* Practicing Python simulation and data visualization

> Note: This is a **conceptual model**, not a neuroscientifically accurate representation of human memory.

---

## Possible Extensions

* Longer simulations (weeks or months)
* Automatic/randomized inputs
* Interactive GUI
* More psychological factors (stress levels, repetition spacing)

---

## Author

Created as a learning-focused simulation project using Python.
