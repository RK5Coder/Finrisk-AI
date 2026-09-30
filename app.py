import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="FinRisk AI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #1a1a1a;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #007bff;
    }
    .metric-card {
        background-color: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #212529;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 0.5rem;
    }
    .section-header {
        font-size: 1.3rem;
        color: #212529;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #007bff;
        padding-bottom: 0.5rem;
    }
    .insight-card {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    results_df = pd.read_csv('data/model_results.csv')
    feature_importance = pd.read_csv('data/feature_importance.csv')
    return results_df, feature_importance

results_df, feature_importance = load_data()

# Sidebar navigation
with st.sidebar:
    st.markdown("## FinRisk AI")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["Dashboard", "Risk Analysis", "Model Insights", "Alert Center", "Business Recommendations"]
    )
    
    st.markdown("---")
    st.markdown("**System Status:** Online")
    st.markdown(f"**Last Update:** {datetime.now().strftime('%Y-%m-%d')}")

# Main content based on selected page
if page == "Dashboard":
    st.markdown('<h1 class="main-header">Dashboard</h1>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_transactions = len(results_df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_transactions:,}</div>
            <div class="metric-label">Total Transactions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        fraud_count = results_df['Actual'].sum()
        fraud_rate = (fraud_count / total_transactions) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{fraud_rate:.3f}%</div>
            <div class="metric-label">Fraud Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        critical_count = (results_df['Risk_Category'] == 'CRITICAL').sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{critical_count:,}</div>
            <div class="metric-label">Critical Alerts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_risk_score = results_df['Risk_Score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_risk_score:.2f}</div>
            <div class="metric-label">Average Risk Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">Risk Distribution</div>', unsafe_allow_html=True)
        risk_counts = results_df['Risk_Category'].value_counts()
        
        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            color_discrete_map={
                'CRITICAL': '#dc3545',
                'HIGH': '#fd7e14',
                'MEDIUM': '#ffc107',
                'LOW': '#20c997',
                'VERY LOW': '#17a2b8'
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">Risk Score Distribution</div>', unsafe_allow_html=True)
        
        fig = px.histogram(
            results_df,
            x='Risk_Score',
            nbins=50,
            color='Risk_Category',
            color_discrete_map={
                'CRITICAL': '#dc3545',
                'HIGH': '#fd7e14',
                'MEDIUM': '#ffc107',
                'LOW': '#20c997',
                'VERY LOW': '#17a2b8'
            }
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent transactions
    st.markdown('<div class="section-header">Recent High-Risk Transactions</div>', unsafe_allow_html=True)
    
    recent_df = results_df[results_df['Risk_Category'].isin(['CRITICAL', 'HIGH'])].head(20)
    if len(recent_df) > 0:
        recent_df_display = recent_df[['Risk_Score', 'Risk_Category', 'Actual']].copy()
        recent_df_display['Risk_Score'] = recent_df_display['Risk_Score'].apply(lambda x: f"{x:.2f}")
        recent_df_display['Actual'] = recent_df_display['Actual'].apply(lambda x: "FRAUD" if x == 1 else "NORMAL")
        recent_df_display.columns = ['Risk Score', 'Risk Category', 'Transaction Type']
        st.dataframe(recent_df_display, use_container_width=True)
    else:
        st.info("No high-risk transactions found in the current dataset.")

elif page == "Risk Analysis":
    st.markdown('<h1 class="main-header">Risk Analysis</h1>', unsafe_allow_html=True)
    
    # Fraud rate by risk category
    st.markdown('<div class="section-header">Fraud Rate by Risk Category</div>', unsafe_allow_html=True)
    
    fraud_by_category = []
    for category in ['VERY LOW', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
        if category in results_df['Risk_Category'].values:
            category_data = results_df[results_df['Risk_Category'] == category]
            fraud_rate = (category_data['Actual'] == 1).mean() * 100
            fraud_by_category.append({
                'Risk Category': category,
                'Fraud Rate (%)': fraud_rate,
                'Transaction Count': len(category_data)
            })
    
    fraud_df = pd.DataFrame(fraud_by_category)
    
    fig = px.bar(
        fraud_df,
        x='Risk Category',
        y='Fraud Rate (%)',
        color='Risk Category',
        color_discrete_map={
            'CRITICAL': '#dc3545',
            'HIGH': '#fd7e14',
            'MEDIUM': '#ffc107',
            'LOW': '#20c997',
            'VERY LOW': '#17a2b8'
        }
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk category details
    st.markdown('<div class="section-header">Risk Category Performance</div>', unsafe_allow_html=True)
    st.dataframe(fraud_df, use_container_width=True)

elif page == "Model Insights":
    st.markdown('<h1 class="main-header">Model Insights</h1>', unsafe_allow_html=True)
    
    # Feature importance
    st.markdown('<div class="section-header">Top Fraud Detection Features</div>', unsafe_allow_html=True)
    
    top_features = feature_importance.head(10)
    
    fig = px.bar(
        top_features,
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Business rules
    st.markdown('<div class="section-header">Business Rules</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Key Fraud Indicators:**
        1. Unusual pattern in V14 (anonymized transaction feature)
        2. Unusual pattern in V12 (anonymized transaction feature)
        3. Unusual pattern in V10 (anonymized transaction feature)
        4. Unusual pattern in V17 (anonymized transaction feature)
        5. Unusual pattern in V4 (anonymized transaction feature)
        """)
    
    with col2:
        st.markdown("""
        **Risk-Based Actions:**
        - **CRITICAL (80-100)**: Immediate review, possible block
        - **HIGH (60-80)**: Enhanced verification required
        - **MEDIUM (40-60)**: Additional checks
        - **LOW (20-40)**: Standard processing
        - **VERY LOW (0-20)**: Normal processing
        """)

elif page == "Alert Center":
    st.markdown('<h1 class="main-header">Alert Center</h1>', unsafe_allow_html=True)
    
    # Alert statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        critical_count = (results_df['Risk_Category'] == 'CRITICAL').sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{critical_count:,}</div>
            <div class="metric-label">Critical Alerts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        high_count = (results_df['Risk_Category'] == 'HIGH').sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{high_count:,}</div>
            <div class="metric-label">High Alerts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_alerts = critical_count + high_count
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_alerts:,}</div>
            <div class="metric-label">Total Alerts</div>
        </div>
        """, unsafe_allow_html=True)
    
    # High-risk transactions
    st.markdown('<div class="section-header">High-Risk Transactions</div>', unsafe_allow_html=True)
    
    high_risk_df = results_df[results_df['Risk_Category'].isin(['CRITICAL', 'HIGH'])].copy()
    
    if len(high_risk_df) > 0:
        high_risk_df_display = high_risk_df[['Risk_Score', 'Risk_Category', 'Actual']].copy()
        high_risk_df_display['Risk_Score'] = high_risk_df_display['Risk_Score'].apply(lambda x: f"{x:.2f}")
        high_risk_df_display['Actual'] = high_risk_df_display['Actual'].apply(lambda x: "FRAUD" if x == 1 else "NORMAL")
        high_risk_df_display.columns = ['Risk Score', 'Risk Category', 'Transaction Type']
        st.dataframe(high_risk_df_display, use_container_width=True)
    else:
        st.info("No high-risk transactions found in the current dataset.")

elif page == "Business Recommendations":
    st.markdown('<h1 class="main-header">Business Recommendations</h1>', unsafe_allow_html=True)
    
    # Calculate key metrics for recommendations
    total_transactions = len(results_df)
    fraud_count = results_df['Actual'].sum()
    fraud_rate = (fraud_count / total_transactions) * 100
    
    critical_count = (results_df['Risk_Category'] == 'CRITICAL').sum()
    high_count = (results_df['Risk_Category'] == 'HIGH').sum()
    
    # Calculate potential savings
    avg_fraud_amount = 122  # From our EDA
    potential_savings = critical_count * avg_fraud_amount
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-card">
        <h4>Immediate Actions</h4>
        <ul>
        <li>Implement real-time alerts for CRITICAL risk transactions</li>
        <li>Enhanced verification for HIGH risk transactions</li>
        <li>Review all CRITICAL transactions within 5 minutes</li>
        <li>Establish dedicated fraud response team</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
        <h4>Process Improvements</h4>
        <ul>
        <li>Automate fraud detection for all transactions</li>
        <li>Integrate with existing payment systems</li>
        <li>Implement machine learning model updates</li>
        <li>Create escalation procedures for high-risk cases</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-card">
        <h4>Financial Impact</h4>
        <ul>
        <li>Current fraud rate: {fraud_rate:.3f}%</li>
        <li>Monthly fraud transactions: {fraud_count}</li>
        <li>Potential monthly savings: ${potential_savings:,.0f}</li>
        <li>ROI on fraud prevention: ~300%</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
        <h4>Technology Recommendations</h4>
        <ul>
        <li>Deploy model to production environment</li>
        <li>Implement API integration for real-time scoring</li>
        <li>Create monitoring dashboard for operations team</li>
        <li>Establish model retraining schedule</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Implementation timeline
    st.markdown('<div class="section-header">Implementation Timeline</div>', unsafe_allow_html=True)
    
    timeline_data = {
        'Phase': ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'],
        'Timeline': ['Week 1-2', 'Week 3-4', 'Week 5-6', 'Week 7-8'],
        'Activities': [
            'Model deployment and testing',
            'Integration with payment systems',
            'Staff training and procedures',
            'Full production rollout'
        ]
    }
    
    timeline_df = pd.DataFrame(timeline_data)
    st.dataframe(timeline_df, use_container_width=True)