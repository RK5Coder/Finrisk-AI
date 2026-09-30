# FinRisk AI - Fraud Detection System

A professional fraud detection system with 99.53% accuracy using machine learning and real-time risk scoring.

## Project Overview

FinRisk AI is an end-to-end fraud detection system that analyzes financial transactions in real-time, identifies suspicious patterns, and provides actionable business insights. The system processes thousands of transactions and flags potentially fraudulent activities with exceptional accuracy.

## Key Features

- **Real-time Fraud Detection**: 99.53% accuracy with Random Forest model
- **Professional Dashboard**: 5-page interface for monitoring and analysis
- **Risk Scoring System**: 0-100 scale with 5 risk categories
- **Alert Center**: Immediate notification for high-risk transactions
- **Business Intelligence**: Actionable insights and ROI analysis
- **Responsive Design**: Clean, professional interface optimized for all devices

## Model Performance

| Metric | Value | Description |
|--------|-------|-------------|
| **AUC Score** | 0.9953 | Near-perfect model performance |
| **Precision** | 72.73% | Flagged transactions that are actually fraud |
| **Recall** | 88.89% | Fraud transactions successfully caught |
| **Accuracy** | 99.53% | Overall correct predictions |
| **F1-Score** | 0.80 | Balance between precision and recall |

## Business Impact

- **Current Fraud Rate**: 0.172% of all transactions
- **Critical Alerts**: 1,015 high-priority transactions identified
- **Potential Monthly Savings**: $123,830 by preventing critical fraud
- **ROI on Prevention**: ~300% return on investment
- **Processing Speed**: Real-time scoring capability

## Technology Stack

- **Backend**: Python 3.9+, Scikit-learn, Pandas, NumPy
- **Frontend**: Streamlit for interactive dashboard
- **Visualization**: Plotly for charts and graphs
- **Data Processing**: Feature engineering and anomaly detection
- **Model**: Random Forest Classifier with hyperparameter tuning

## Project Structure
```
finrisk-ai/
├── app.py # Main dashboard application
├── README.md # Project documentation
├── requirements.txt # Python dependencies
├── .gitignore # Files to exclude from version control
├── src/ # Source code modules
│ └── data.py # Data processing and feature engineering
├── data/ # Processed data files
│ ├── model_results.csv # Model predictions and risk scores
│ └── feature_importance.csv # Feature importance rankings
└── models/ # Trained machine learning models
└── fraud_model.pkl # Serialized Random Forest model
```

## Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Git for version control

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/[your-username]/finrisk-ai.git
   cd finrisk-ai
   
   
2. **Create virtual environment**
   
  ```bash 
  python -m venv venv 
  source venv/bin/activate  # On Windows: venv\Scripts\activate 
  ```
  
3. **Install dependencies**
   
  ```bash
  pip install -r requirements.txt
  ```

4. **Run the application**

   ```bash
   streamlit run app.py
   ```
   
## Dashboard Features

### 1. Dashboard Overview
- Real-time transaction monitoring
- Key performance metrics
- Risk distribution charts
- Recent high-risk transactions

### 2. Risk Analysis
- Fraud rate by risk category
- Risk category performance metrics
- Statistical analysis of patterns

### 3. Model Insights
- Top fraud detection features
- Business rules and thresholds
- Feature importance rankings

### 4. Alert Center
- Critical and high-risk alerts
- Alert statistics and trends
- Transaction-level details

### 5. Business Recommendations
- Implementation timeline
- Financial impact analysis
- Process improvement suggestions

## Methodology

### Data Processing
- **Data Cleaning**: Removed duplicates, handled missing values
- **Feature Engineering**: Created risk-based features from transaction patterns
- **Normalization**: Scaled features for optimal model performance
- **Class Imbalance**: Applied SMOTE for balanced training

### Model Development
- **Algorithm Selection**: Random Forest for interpretability and performance
- **Cross-Validation**: 5-fold CV for robust evaluation
- **Hyperparameter Tuning**: Grid search for optimal parameters
- **Feature Selection**: Recursive feature elimination

### Risk Scoring
- **Score Range**: 0-100 (higher = greater fraud probability)
- **Categories**: VERY LOW (0-20), LOW (20-40), MEDIUM (40-60), HIGH (60-80), CRITICAL (80-100)
- **Thresholds**: Optimized for business impact

## Business Value

### Immediate Benefits
- **Fraud Prevention**: Real-time detection saves $123,830 monthly
- **Operational Efficiency**: Automated review process reduces manual effort
- **Risk Management**: Proactive identification of suspicious patterns

### Long-term Value
- **Scalability**: System handles increasing transaction volumes
- **Adaptability**: Model can be retrained with new data patterns
- **Integration**: API-ready for payment system integration

## Future Enhancements

- **Real-time API Integration**: Connect with payment processing systems
- **Advanced Analytics**: Time-series analysis for pattern detection
- **Machine Learning Operations**: Automated model retraining pipeline
- **Mobile Application**: On-the-go fraud monitoring for executives

## Contact & Support

**Developer**: Ravi Khunt
**LinkedIn**: https://www.linkedin.com/in/ravi-khunt01/

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Dataset source: [Credit Card Fraud Detection - Kaggle]
- Machine learning frameworks: Scikit-learn, Pandas, NumPy
- Dashboard framework: Streamlit
- Visualization library: Plotly

---
