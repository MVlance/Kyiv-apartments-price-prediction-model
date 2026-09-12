# Kyiv Real Estate Price Estimator 🏢🇺🇦

An end-to-end Machine Learning pipeline that predicts secondary market apartment prices in Kyiv, Ukraine. The dataset is collected directly from the **DOM.RIA API**, preprocessed, enriched with spatial geospatial metrics (subway station and city center proximity), and modeled using Gradient Boosting (**XGBoost**).

---

## 📌 Project Overview

Predicting apartment prices based solely on physical characteristics often fails because **location nuances dominate valuation**. This project demonstrates how:
1. Transforming raw geographic coordinates into spatial distance metrics (**BallTree Haversine search** to 44+ Kyiv subway stations and Khreshchatyk) dramatically improves model accuracy.
2. Applying target encoding on localized micro-districts captures price density without exploding feature dimensionality[cite: 1].
3. Moving from standard Linear Regression/Ridge to Extreme Gradient Boosting (**XGBoost**) resolves non-linear price relationships[cite: 1].

---

## 📊 Benchmark & Results

Evaluated on unseen test data across iterations[cite: 1]:

| Model | Target Transform | Features Used | Test $R^2$ | Test MAE ($) |
|---|---|---|---|---|
| **Linear Regression (OLS)** | None | Areas, Floor, 10 Admin Districts[cite: 1] | `0.443` | `$78,019` |
| **Linear Regression (OLS)** | $\log(1 + y)$ | Outlier filtered, Area ratios[cite: 1] | `0.628` | `$36,945`[cite: 1] |
| **Ridge Regression** | $\log(1 + y)$ | Scaled numerical features[cite: 1] | `0.628`[cite: 1] | `$36,754`[cite: 1] |
| **XGBoost (Baseline)** | $\log(1 + y)$ | OneHot districts + basic features[cite: 1] | `0.709`[cite: 1] | `$31,731`[cite: 1] |
| **XGBoost + Target Encoding** | $\log(1 + y)$ | 84 Micro-districts + Area ratios[cite: 1] | `0.761`[cite: 1] | `$34,478`[cite: 1] |
| **XGBoost + Geo Features (Final)** | $\log(1 + y)$ | Dist to Subway + Center + All Features[cite: 1] | **`0.849`**[cite: 1] | **`$18,546`**[cite: 1] |

* **10-Fold Cross-Validation:** Average $R^2 = \mathbf{0.808 \pm 0.036}$[cite: 1].

---

## 🛠️ Feature Engineering Highlights

* **Proximity to Subway (`dist_to_subway_km`):** Calculated using `sklearn.neighbors.BallTree` with the Haversine metric across all Kyiv Metro stations ($O(N \log M)$ query time)[cite: 1].
* **Distance to City Center (`dist_to_center`):** Spherical distance to Khreshchatyk / Independence Square ($50.4501^\circ\text{ N}, 30.524^\circ\text{ E}$)[cite: 1].
* **Micro-district Target Encoding:** Uses out-of-fold cross-validated target encoding for 84 raw district names to prevent data leakage while preserving localized pricing variance[cite: 1].
* **Layout Ratios:**
  * `kitchen_ratio`: $\frac{\text{kitchen\_area}}{\text{total\_area}}$[cite: 1]
  * `living_ratio`: $\frac{\text{living\_area}}{\text{total\_area}}$[cite: 1]
  * `floor_ratio`: $\frac{\text{floor}}{\text{floors\_count}}$[cite: 1]
  * `area_per_room`: $\frac{\text{total\_area}}{\text{rooms\_count}}$[cite: 1]

---

## 🔑 Top Feature Importances

According to the trained XGBoost model[cite: 1]:
1. **Total Area** (~$26.7\%$)[cite: 1]
2. **Kitchen Area** (~$15.0\%$)[cite: 1]
3. **Distance to Center (`log_dist_to_center` & linear)** (~$16.4\%$ combined)[cite: 1]
4. **Living Area** (~$5.4\%$)[cite: 1]
5. **Rooms Count** (~$4.2\%$)[cite: 1]
6. **Distance to Nearest Subway** (~$3.1\%$)[cite: 1]
7. **Wall Type (`панель` discount penalty)** (~$2.9\%$)[cite: 1]

---

## 🚀 Quickstart

### 1. Clone & Set Up Environment

```bash
git clone [https://github.com/](https://github.com/)<your-username>/Project_AI_REGRESSION_DOMRIA.git
cd Project_AI_REGRESSION_DOMRIA

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Run Data Pipeline & Training

    Scraping: Run src/domria_id_parser.py and src/domria_appartments_parser.py to fetch current active listings via DOM.RIA API.

    Modeling: Open and execute src/notebooks/processing_model.ipynb to reproduce the feature generation and model evaluation pipeline[cite: 1].


## Project Structure
├── src/
│   ├── data/
│   │   └── kyiv_apartments.csv         # Baseline parsed dataset
│   ├── notebooks/
│   │   ├── statistics_check.ipynb      # EDA and initial distribution checks
│   │   └── processing_model.ipynb      # Main preprocessing & modeling pipeline
│   ├── create_queue.py                 # Queue worker for API requests
│   ├── domria_id_parser.py             # Fetch listing IDs from search API
│   ├── domria_appartments_parser.py    # Fetch listing metadata
│   └── prepare_data.py                 # Data cleansing routines
├── .gitignore
├── requirements.txt
└── README.md
