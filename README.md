# 🏁 Race Timing Analysis (Anonymized Data)

This project analyzes race timing data while preserving participant anonymity. It includes:

- 🔒 Consistent anonymization of racer names, categories, ages, and placement
- ⚙️ Timing noise to obscure exact rankings without losing analytical value
- 📊 Visualizations: performance by category, age vs. time, competitiveness

## 🔧 Features
- SHA-256 pseudonyms for racer IDs
- Randomized category names (consistent within groups)
- Lap time perturbation
- Age jittering (±3 years)
- Place randomization (±2 places)
- Category/date-aware transformations

## 📈 Visualization Highlights
- Boxplots of lap times by category
- Scatterplots of age vs. lap time
- Time gaps between top finishers
- Category-wise age distributions

## 📦 Libraries Used
- `pandas`
- `numpy`
- `seaborn`
- `matplotlib`
- `faker`
- `hashlib`
  
## 🚀 Getting Started
```bash
pip install pandas numpy seaborn matplotlib faker textblob
