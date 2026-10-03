# E-Commerce Customer Intelligence

An end-to-end project covering SQLite data cleaning, SQL analysis,
EDA, churn modeling, a neural network, sentiment analysis and Streamlit.

## Application
- Dashboard with SQL-based metrics and charts.
- Customer churn prediction using a saved model.
- Review sentiment analysis using a saved NLP model.

## Business Insights
1. Electronics contributes approximately 69.9% of net revenue.
   Protect stock availability and review profit margins.
2. Karachi contributes approximately 26.3% of net revenue from
   1,935 purchasing customers. Prioritize delivery reliability.
3. Fashion has an approximately 11.25% return rate across 12,236 orders.
   Investigate return reasons, product descriptions and quality.

## Churn Methodology
Features use orders through 31 May 2026.
The target window is 1 June to 31 August 2026.
Churn = 1 means no purchase during the target window.

Preprocessing is fitted on training data only.
ML selection uses validation F1, with ROC-AUC as a tie-breaker.
All churn models use the same test customers.

## Models
- Logistic Regression
- Random Forest
- Feed-forward neural network: 32 and 16 hidden neurons
- Sentiment: TF-IDF plus Logistic Regression

Evaluation results are available in the models folder.

## Assumptions and Limitations
- Discounts are fractional rates.
- Returned orders are assumed fully refunded.
- Revenue uses historical order prices.
- Invalid orders are preserved with quality flags.
- Historical membership and return/delivery snapshots are unavailable.
- Excluding uncertain churn labels may introduce selection bias.
- Rating-derived sentiment labels may differ from text sentiment.
- Similar review templates may inflate NLP evaluation.
- Churn probabilities are not calibrated.

## Run Locally
Training Python version: 3.13.9

    python -m pip install -r requirements.txt
    python -m streamlit run app.py

## Reproduce Analysis
Open the project notebook and run its cells in order.
Cleaning requires ecommerce_hackathon.db.
The app uses ecommerce_cleaned.db and saved models.

## Submission Links
GitHub repository: To be added
Live Streamlit app: To be added
