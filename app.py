import sqlite3
import re
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="E-Commerce Customer Intelligence",
    page_icon="🛒",
    layout="wide"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f4f6fb;
    color: #172554;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #101b35;
}

[data-testid="stSidebar"] *,
[data-testid="stSidebar"] label {
    color: #e2e8f0 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 12px;
}

/* Headings */
h1 {
    font-weight: 800 !important;
    letter-spacing: -1px;
    color: #14213d;
}

h2, h3 {
    color: #14213d;
    font-weight: 700 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5eaf3;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 6px 20px rgba(20, 33, 61, 0.04);
}

[data-testid="stMetricLabel"] {
    color: #64748b;
}

[data-testid="stMetricValue"] {
    color: #14213d;
    font-weight: 800;
}

/* Prediction forms */
[data-testid="stForm"] {
    background: #ffffff;
    border: 1px solid #e5eaf3;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 24px rgba(20, 33, 61, 0.04);
}

/* Input fields */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    color: #14213d;
    background: #f8fafc;
}

[data-testid="stTextArea"] textarea {
    border-radius: 12px;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: #2563eb;
    color: #ffffff;
    border: 0;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
    transition: background 0.2s ease, transform 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #1d4ed8;
    color: #ffffff;
    transform: translateY(-1px);
}

.stButton > button:focus-visible,
.stFormSubmitButton > button:focus-visible {
    outline: 3px solid #93c5fd;
    outline-offset: 3px;
}

/* Tables */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

/* Custom header */
.commerce-hero {
    background: linear-gradient(120deg, #14213d, #1e40af);
    padding: 32px;
    border-radius: 22px;
    margin-bottom: 28px;
    box-shadow: 0 12px 30px rgba(30, 64, 175, 0.15);
}

.commerce-hero .eyebrow {
    color: #bfdbfe;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.commerce-hero h1 {
    color: #ffffff !important;
    font-size: clamp(26px, 4vw, 38px);
    line-height: 1.2;
    margin: 12px 0;
}

.commerce-hero p {
    color: #dbeafe;
    font-size: 15px;
    margin: 0;
}

.sidebar-brand {
    padding: 12px 0 24px;
}

.sidebar-brand .brand-name {
    font-size: 25px;
    font-weight: 800;
    color: white;
}

.sidebar-brand .brand-description {
    font-size: 12px;
    color: #94a3b8 !important;
    margin-top: 6px;
}

@media (max-width: 640px) {
    .commerce-hero {
        padding: 22px;
    }

    [data-testid="stForm"] {
        padding: 16px;
    }
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<div class="commerce-hero">
    <div class="eyebrow">E-Commerce Analytics</div>
    <h1>Understand your customers.<br>Grow your business.</h1>
    <p>
        Explore sales performance, identify churn risk,
        and understand customer feedback.
    </p>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="brand-name">🛒 CommerceIQ</div>
    <div class="brand-description">Customer Intelligence Dashboard</div>
</div>
""", unsafe_allow_html=True)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ecommerce_cleaned.db"
MODEL_DIR = BASE_DIR / "models"

required = [
    DB_PATH,
    MODEL_DIR / "churn_model.joblib",
    MODEL_DIR / "sentiment_model.joblib"
]

missing = [str(path.name) for path in required if not path.exists()]
if missing:
    st.error("Missing required files: " + ", ".join(missing))
    st.stop()


@st.cache_resource
def load_model(filename):
    return joblib.load(MODEL_DIR / filename)


@st.cache_data
def query_database(query):
    with sqlite3.connect(
        DB_PATH.as_uri() + "?mode=ro",
        uri=True
    ) as connection:
        return pd.read_sql_query(query, connection)




page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Churn Prediction", "Sentiment Analysis"]
)

if page == "Dashboard":
    st.header("Business Dashboard")

    # Dashboard outputs are calculated directly using SQLite SQL.
    revenue = query_database("""
        SELECT COALESCE(
            SUM(quantity * unit_price
                * (1 - discount) * (1 - returned)),
            0
        ) AS revenue
        FROM analysis_orders
    """).iloc[0]["revenue"]

    order_count = query_database("""
        SELECT COUNT(*) AS orders
        FROM analysis_orders
    """).iloc[0]["orders"]

    customer_count = query_database("""
        SELECT COUNT(*) AS customers
        FROM customers
    """).iloc[0]["customers"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Net Revenue", f"{revenue:,.2f}")
    col2.metric("Valid Orders", f"{int(order_count):,}")
    col3.metric("Registered Customers", f"{int(customer_count):,}")

    st.caption(
        "Discounts are fractional rates. Returned orders are assumed "
        "fully refunded; revenue is adjusted in the original order month."
    )

    monthly = query_database("""
        SELECT
            strftime('%Y-%m', order_date) AS month,
            SUM(quantity * unit_price
                * (1 - discount) * (1 - returned)) AS net_revenue
        FROM analysis_orders
        GROUP BY strftime('%Y-%m', order_date)
        ORDER BY month
    """)

    categories = query_database("""
        SELECT
            p.category,
            SUM(o.quantity * o.unit_price
                * (1 - o.discount) * (1 - o.returned)) AS net_revenue
        FROM analysis_orders AS o
        JOIN products AS p ON o.product_id = p.product_id
        GROUP BY p.category
        ORDER BY net_revenue DESC
    """)

    st.subheader("Monthly Net Revenue")
    monthly["month"] = pd.to_datetime(monthly["month"])
    st.line_chart(monthly.set_index("month")["net_revenue"])

    st.subheader("Category Net Revenue")
    st.bar_chart(categories.set_index("category")["net_revenue"])
    st.dataframe(categories, hide_index=True)

elif page == "Churn Prediction":
    st.header("Customer Churn Prediction")
    st.caption(
        "Enter purchase-history features as of 31 May 2026. "
        "The model predicts no purchase during June–August 2026."
    )

    model = load_model("churn_model.joblib")

    # Membership options come from the fitted training encoder.
    memberships = list(
        model.named_steps["preprocessor"]
        .named_transformers_["categorical"]
        .named_steps["encoder"]
        .categories_[0]
    )

    with st.form("churn_form"):
        col1, col2 = st.columns(2)

        with col1:
            total_orders = st.number_input(
                "Total Orders", min_value=1, value=10, step=1
            )
            total_spending = st.number_input(
                "Total Net Spending", min_value=0.0, value=50000.0
            )
            days_since_last_order = st.number_input(
                "Days Since Last Order", min_value=0, value=30, step=1
            )
            return_pct = st.number_input(
                "Return Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=10.0
            )

        with col2:
            average_order_value = total_spending / total_orders
            st.metric("Average Net Order Value", f"{average_order_value:,.2f}")

            unknown_delivery = st.checkbox("Average Delivery Days Unknown")
            delivery = st.number_input(
                "Average Delivery Days",
                min_value=0.0,
                value=4.0
            )

            unknown_age = st.checkbox("Age Unknown")
            age = st.number_input(
                "Age", min_value=18, max_value=100, value=30, step=1
            )
            membership = st.selectbox("Membership Type", memberships)

        submitted = st.form_submit_button("Predict Churn")

    if submitted:
        customer = pd.DataFrame([{
            "total_orders": total_orders,
            "total_spending": total_spending,
            "average_order_value": average_order_value,
            "days_since_last_order": days_since_last_order,
            "return_rate": return_pct / 100,
            "average_delivery_days": (
                float("nan") if unknown_delivery else delivery
            ),
            "age": float("nan") if unknown_age else age,
            "membership_type": membership
        }])

        churn_column = list(model.classes_).index(1)
        probability = float(
            model.predict_proba(customer)[0, churn_column]
        )
        prediction = int(model.predict(customer)[0])

        st.metric("Estimated Churn Probability", f"{probability:.1%}")

        if prediction == 1:
            st.warning("Prediction: Churn")
        else:
            st.success("Prediction: Not Churn")

        st.caption(
            "Model probabilities are estimates and have not been calibrated."
        )

else:
    st.header("Review Sentiment Analysis")
    model = load_model("sentiment_model.joblib")

    with st.form("sentiment_form"):
        review = st.text_area(
            "Customer Review",
            placeholder="Enter a product review..."
        )
        submitted = st.form_submit_button("Analyze Sentiment")

    if submitted:
        cleaned_review = re.sub(r"\s+", " ", review.lower()).strip()

        if not cleaned_review:
            st.warning("Please enter a review.")
        else:
            prediction = model.predict([cleaned_review])[0]
            st.success(f"Predicted Sentiment: {prediction}")

            probabilities = model.predict_proba([cleaned_review])[0]
            st.dataframe(pd.DataFrame({
                "Sentiment": model.classes_,
                "Model Probability": probabilities
            }), hide_index=True)

            st.caption(
                "Training labels were derived from ratings. "
                "Text sentiment can differ from the customer's rating."
            )
