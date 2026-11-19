import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
].copy()

if filtered.empty:
    st.warning("No customers match the selected filters.")
    st.stop()

# ---------- 4 metrics ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Customers", f"{len(filtered):,}")
c2.metric("Churn Rate", f"{(filtered['Churn'] == 'Yes').mean() * 100:.1f}%")
c3.metric("Median Tenure (months)", f"{filtered['tenure'].median():.0f}")
c4.metric("Avg Monthly Charges", f"${filtered['MonthlyCharges'].mean():.2f}")

# ---------- Prepare columns for charts ----------
filtered["ChurnNum"] = (filtered["Churn"] == "Yes").astype(int)
filtered["Tenure_Group"] = pd.cut(filtered["tenure"], bins=[-1, 12, 48, 72],
                                  labels=["New", "Medium", "Loyal"])
services_cols = ["OnlineSecurity", "OnlineBackup", "DeviceProtection",
                 "TechSupport", "StreamingTV", "StreamingMovies"]
filtered["Services_Count"] = (filtered[services_cols] == "Yes").sum(axis=1)

def churn_chart(col, title, xlabel):
    rate = filtered.groupby(col, observed=True)["ChurnNum"].mean() * 100
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(rate.index.astype(str), rate.values, label="Churn rate (%)")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Churn Rate (%)")
    ax.legend()
    st.pyplot(fig)
    st.caption(f"Highest churn: {rate.idxmax()} at {rate.max():.1f}% | "
               f"Lowest churn: {rate.idxmin()} at {rate.min():.1f}%")

# ---------- 3 charts ----------
st.subheader("Key Charts")
a, b, c = st.columns(3)
with a:
    churn_chart("Contract", "Churn Rate by Contract Type", "Contract Type")
with b:
    churn_chart("Tenure_Group", "Churn Rate by Tenure Group", "Tenure Group")
with c:
    churn_chart("Services_Count", "Churn Rate by Number of Extra Services", "Services Count")

# ---------- Top 3 findings (write in your own words) ----------
st.subheader("Top 3 Findings")
st.markdown("""
<div dir="rtl">

1. **(اكتبي اكتشافك الأول هنا بكلامك مع رقم)**
2. **(اكتبي اكتشافك الثاني هنا بكلامك مع رقم)**
3. **(اكتبي اكتشافك الثالث هنا بكلامك مع رقم)**

</div>
""", unsafe_allow_html=True)
