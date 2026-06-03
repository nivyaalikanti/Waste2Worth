# Waste2Worth ♻️

Waste2Worth is an AI-powered e-waste valuation system that helps users make informed decisions about their used electronic devices.

## Features

- Predicts resale value of electronic devices using Machine Learning
- Estimates recoverable precious materials
- Calculates recycling value
- Provides intelligent Resell vs Recycle recommendations
- Modern web-based user interface

## Model Performance Comparison

The resale value prediction module was evaluated using multiple machine learning algorithms on the used electronic devices dataset.

| Model | R² Score | MAE | RMSE |
|---------|---------|---------|---------|
| Random Forest (Baseline) | 0.8568 | - | - |
| Random Forest (Hyperparameter Tuned) | 0.8595 | 0.1710 | 0.2135 |
| CatBoost Regressor | 0.8579 | 0.1716 | 0.2148 |
| ExtraTrees Regressor | **0.8604** | **0.1707** | **0.2128** |

### Final Selected Model

**ExtraTrees Regressor** was selected as the final model due to its superior performance across all evaluation metrics.

- R² Score: **0.8604**
- MAE: **0.1707**
- RMSE: **0.2128**

## Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Machine Learning
- ExtraTrees Regressor
- Scikit-Learn

## Project Workflow

User Inputs Device Details
↓
Resale Price Prediction
↓
Material Recovery Estimation
↓
Recycling Value Calculation
↓
Resell vs Recycle Recommendation

## Future Enhancements

- Dynamic precious metal pricing
- More device categories
- Advanced recycling estimation
- User authentication
- Deployment on cloud platforms

## Author

Nivya Alikanti