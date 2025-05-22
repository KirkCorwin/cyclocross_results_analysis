# 🚴 Rider Performance Modeling

This project predicts race performance by modeling lap times relative to each racer's demographic peer group (age + gender). It uses past race history to build interpretable machine learning models for both broad and elite riders. The goal is to enable robust, fair, and realistic performance predictions.

---

## 📌 Objective

- Detect anomalously fast performances using statistical and ML-based anomaly detection.
- Predict lap time relative to peer group using historical performance only.
- Visualize, explain, and evaluate model accuracy and error across all competitors.

---

## 🔍 Dataset

- Anonymized race performance data including:
  - `anon_time`, `anon_age`, `gender`, `anon_category`, `anon_place`, `date`, `racer_id`
- Relative performance calculated as:  
  **`relative_time_to_peer = anon_time / peer_mean_time`**

---

## 🧠 Methods

### Anomaly Detection
- **Z-score** (category-aware)
- **Isolation Forest** (age & time)
- Combined flags saved as `fast_outliers = 1`

### Modeling
- Uses **historical average relative time** from prior races for each racer
- Models:
  - `RandomForestRegressor` (primary)
  - Evaluation: MAE, RMSE

### Feature Engineering
- Historical performance features: `historical_relative_mean`
- Peer-based normalization using age group + gender

---

## 📊 Results

| Dataset        | MAE    | RMSE   |
|----------------|--------|--------|
| All Racers     | 0.1023 | 0.0245 |
| Fast Outliers  | 0.1823 | 0.0427 |

Model is more accurate for the general population and predictably less so for outlier performances.

---

## 🖼️ Visualizations

- Predicted vs Actual (relative performance)
- Residuals vs Predicted
- Isolation Forest decision surfaces
- Violin plots of demographic distributions

All plots are saved in `/plots/`.

---

## ⚙️ Setup

```bash
conda env create -f requirements.yaml
conda activate cx_trends
jupyter notebook
```
--

## 📦 Dependencies

--
See environment.yaml for full list. Major tools used:

Python 3.9

scikit-learn, pandas, seaborn, matplotlib

faker, nltk, imbalanced-learn (for auxiliary experiments)

--

## 👤 Author

--

Kirk Corwin
Data Science @ North Seattle College
GitHub | LinkedIn