import streamlit as st
import pandas as pd

st.set_page_config(page_title="Telco Churn Dashboard", layout="wide")
st.title("Telco Customer Churn Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("telco_clean.csv")

df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")

contracts = sorted(df["Contract"].unique())
contract = st.sidebar.multiselect("Contract", contracts, default=contracts)

internet_opts = sorted(df["InternetService"].unique())
internet = st.sidebar.multiselect("Internet Service", internet_opts, default=internet_opts)

tenure_range = st.sidebar.slider("Tenure (months)",
                                 int(df["tenure"].min()), int(df["tenure"].max()),
                                 (int(df["tenure"].min()), int(df["tenure"].max())))

filtered = df[
    df["Contract"].isin(contract)
    & df["InternetService"].isin(internet)
    & df["tenure"].between(tenure_range[0], tenure_range[1])
]

if filtered.empty:
    st.warning("No customers match the selected filters.")
    st.stop()

# ---------- 4 metrics ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Customers", f"{len(filtered):,}")
c2.metric("Churn Rate", f"{(filtered['Churn'] == 'Yes').mean() * 100:.1f}%")
c3.metric("Median Tenure (months)", f"{filtered['tenure'].median():.0f}")
c4.metric("Avg Monthly Charges", f"${filtered['MonthlyCharges'].mean():.2f}")
