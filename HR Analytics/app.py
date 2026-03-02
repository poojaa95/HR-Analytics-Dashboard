import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# PAGE CONFIG

st.set_page_config(
    page_title="HR Analytics Pro Dashboard",
    layout="wide",
    page_icon="📊"
)

st.title("📊 HR Analytics Professional Dashboard")
st.markdown("### Workforce Overview | Attrition | Demographics | Compensation")

st.markdown("---")

# Uploading File

st.sidebar.header("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader("Upload HR CSV File", type=["csv"])

if uploaded_file is None:
    st.warning("Please upload an HR dataset to continue.")
    st.stop()

df = pd.read_csv(uploaded_file)
st.success("Dataset uploaded successfully!")

# Preview
with st.expander("🔎 Preview Dataset"):
    st.dataframe(df.head())

# Checking Required Columns 

required_cols = ["Department", "Gender", "Attrition", "Age", "MonthlyIncome"]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"Missing required columns: {missing}")
    st.stop()

# Sidebar Filters

st.sidebar.header("🔎 Filters")

department = st.sidebar.multiselect(
    "Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

attrition = st.sidebar.multiselect(
    "Attrition",
    df["Attrition"].unique(),
    default=df["Attrition"].unique()
)

filtered_df = df[
    (df["Department"].isin(department)) &
    (df["Gender"].isin(gender)) &
    (df["Attrition"].isin(attrition))
]

# KPI Section

st.markdown("## 📌 Executive Summary")

total_emp = filtered_df.shape[0]

if total_emp > 0:
    attrition_rate = round(
        (filtered_df["Attrition"] == "Yes").mean() * 100, 2
    )
    avg_income = round(filtered_df["MonthlyIncome"].mean(), 0)
    avg_age = round(filtered_df["Age"].mean(), 1)
    median_income = round(filtered_df["MonthlyIncome"].median(), 0)
else:
    attrition_rate = avg_income = avg_age = median_income = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Employees", total_emp)
col2.metric("Attrition Rate (%)", attrition_rate)
col3.metric("Average Monthly Income", f"${avg_income}")
col4.metric("Median Monthly Income", f"${median_income}")

st.markdown("---")

# Attrition Analysis

st.markdown("## 📉 Attrition Analysis")

colA, colB = st.columns(2)

with colA:
    fig1 = px.bar(
        filtered_df,
        x="Department",
        color="Attrition",
        barmode="group",
        title="Attrition by Department",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    fig2 = px.pie(
        filtered_df,
        names="Attrition",
        title="Overall Attrition Distribution",
        hole=0.4
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Dempgraphic Analysis

st.markdown("## 👥 Demographic Analysis")

colC, colD = st.columns(2)

with colC:
    fig3 = px.histogram(
        filtered_df,
        x="Age",
        color="Attrition",
        nbins=20,
        title="Age Distribution by Attrition",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig3, use_container_width=True)

with colD:
    fig4 = px.box(
        filtered_df,
        x="Gender",
        y="MonthlyIncome",
        color="Gender",
        title="Income Distribution by Gender",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Compensation Analysis

st.markdown("## 💰 Compensation Analysis")

colE, colF = st.columns(2)

with colE:
    fig5 = px.box(
        filtered_df,
        x="Attrition",
        y="MonthlyIncome",
        color="Attrition",
        title="Salary vs Attrition"
    )
    st.plotly_chart(fig5, use_container_width=True)

with colF:
    fig6 = px.scatter(
        filtered_df,
        x="Age",
        y="MonthlyIncome",
        color="Attrition",
        title="Age vs Income vs Attrition",
        opacity=0.7
    )
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# Correlation Heatmap

st.markdown("## 🔥 Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include=['int64', 'float64'])

if not numeric_df.empty:
    corr = numeric_df.corr()

    heatmap = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="RdBu",
        zmid=0
    ))

    heatmap.update_layout(title="Feature Correlation Matrix")

    st.plotly_chart(heatmap, use_container_width=True)

st.markdown("---")

# Business Insights

st.markdown("## 🧠 Business Insights")

if total_emp > 0:
    try:
        high_attrition_dept = (
            filtered_df[filtered_df["Attrition"] == "Yes"]
            .groupby("Department")
            .size()
            .idxmax()
        )

        st.markdown(f"""
        - Highest attrition department: **{high_attrition_dept}**
        - Overall attrition rate: **{attrition_rate}%**
        - Monitor compensation gaps across demographics.
        - Consider retention strategies for younger employees.
        - Analyze department-level engagement programs.
        """)
    except:
        st.write("Insufficient data for detailed insights.")

st.markdown("---")

# Download your filtered data

st.markdown("## ⬇ Download Filtered Dataset")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered CSV",
    data=csv,
    file_name="filtered_hr_data.csv",
    mime="text/csv"
)