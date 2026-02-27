

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Assam Yuktdhara Status Dashboard", layout="wide")

st.title("🗺️ Assam Yuktdhara Monitoring Dashboard")

# -----------------------
# LOAD DATA
# -----------------------
# Google sheet CSV export link
sheet_url = "https://docs.google.com/spreadsheets/d/1JuOrZ5hj0NbTCTbo3KGF0yCHf8uaDSaGGPnALQmsF3k/export?format=csv"


try:
    # Read Google Sheet as DataFrame
    data = pd.read_csv(sheet_url)
    data.columns = data.columns.str.strip()


    

except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()
    
    

# -----------------------

# -----------------------
# CLEAN DATA
# -----------------------

data.columns = data.columns.str.strip()

# Remove rows where Sl. No. is "State Total"
data = data[data["Sl. No."].astype(str) != "State Total"]

# Remove completely blank district rows
data = data[data["District"].astype(str).str.strip() != ""]
# # -----------------------
# KPI SECTION (Correct Logic)
# -----------------------

progress_col = "Percentage of progress as on today status"

# Ensure numeric
data[progress_col] = pd.to_numeric(data[progress_col], errors="coerce")

total_districts = data["District"].nunique()

completed_100 = data[data[progress_col].round(2) >= 100].shape[0]

between_85_100 = data[
    (data[progress_col] >= 85) & (data[progress_col] < 100)
].shape[0]

between_50_85 = data[
    (data[progress_col] >= 50) & (data[progress_col] < 85)
].shape[0]

below_50 = data[data[progress_col] < 50].shape[0]



# -----------------------
# COLORED KPI CARDS
# -----------------------

st.markdown("""
<style>
.kpi-card {
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-weight: bold;
}
.blue { background-color: #1f77b4; }
.green { background-color: #2ca02c; }
.lightyellow { background-color: #faf202; }
.orange { background-color: #ff9800; }
.red { background-color: #d62728; }

.kpi-title {
    font-size: 18px;
}
.kpi-value {
    font-size: 32px;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-title">Total Districts</div>
        <div class="kpi-value">{total_districts}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-title">100%</div>
        <div class="kpi-value">{completed_100}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card lightyellow">
        <div class="kpi-title">85% – 99%</div>
        <div class="kpi-value">{between_85_100}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card orange">
        <div class="kpi-title">50% – 84%</div>
        <div class="kpi-value">{between_50_85}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card red">
        <div class="kpi-title">&lt; 50%</div>
        <div class="kpi-value">{below_50}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # -----------------------
# COMPARISON: 0% – 49%
# -----------------------

st.divider()
st.subheader("📊 Districts (0% – 49%) : Last Status vs Today")

progress_today = "Percentage of progress as on today status"
progress_last = "Percentage of progress as on last status"

# Ensure numeric
data[progress_today] = pd.to_numeric(data[progress_today], errors="coerce")
data[progress_last] = pd.to_numeric(data[progress_last], errors="coerce")

         # Filter 0–50%
filtered_0_50 = data[
    (data[progress_today] >= 0) & (data[progress_today] < 50)
]
if not filtered_0_50.empty:

    comparison_df = filtered_0_50[[
        "District",
        progress_last,
        progress_today
    ]]

    comparison_melted = comparison_df.melt(
        id_vars="District",
        value_vars=[progress_last, progress_today],
        var_name="Status Type",
        value_name="Progress %"
    )
    
    fig_compare = px.bar(
        comparison_melted,
        x="District",
        y="Progress %",
        color="Status Type",
        barmode="group",
        title="Last Status vs Today Progress",
        color_discrete_map={
            "Percentage of progress as on last status": "#1f77b4",
            "Percentage of progress as on today status": "#2ca02c"
        }
    )

    fig_compare.update_traces(
        texttemplate='%{y:.1f}',
        textposition='outside',
        marker_line_width=1,
        marker_line_color='black'
    )

    fig_compare.update_layout(
        yaxis_title="Progress (%)",
        xaxis_title="District",
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    st.plotly_chart(fig_compare, width="stretch")

else:
    st.info("No districts currently between 0% and 49%.")



    # COMPARISON: 50% – 85%
# -----------------------

st.divider()
st.subheader("📊 Districts (50% – 84%) : Last Status vs Today")

progress_today = "Percentage of progress as on today status"
progress_last = "Percentage of progress as on last status"

# Ensure numeric
data[progress_today] = pd.to_numeric(data[progress_today], errors="coerce")
data[progress_last] = pd.to_numeric(data[progress_last], errors="coerce")
    
    # Filter 50–85%
filtered_50_85 = data[
    (data[progress_today] >= 50) & (data[progress_today] < 85)
]

if not filtered_50_85.empty:

    comparison_df = filtered_50_85[[
        "District",
        progress_last,
        progress_today
    ]]

    # Convert to long format
    comparison_melted = comparison_df.melt(
        id_vars="District",
        value_vars=[progress_last, progress_today],
        var_name="Status Type",
        value_name="Progress %"
    )

    fig_compare = px.bar(
        comparison_melted,
        x="District",
        y="Progress %",
        color="Status Type",
        barmode="group",
        title="Last Status vs Today Progress"
    )

    st.plotly_chart(fig_compare, width="stretch")

else:
    st.info("No districts currently between 50% and 85%.")
    
    
    # COMPARISON: 85% – 99%
# -----------------------

st.divider()
st.subheader("📊 Districts (85% – 99%) : Last Status vs Today")

progress_today = "Percentage of progress as on today status"
progress_last = "Percentage of progress as on last status"

# Ensure numeric
data[progress_today] = pd.to_numeric(data[progress_today], errors="coerce")
data[progress_last] = pd.to_numeric(data[progress_last], errors="coerce")

# Filter 85–99%
filtered_85_100 = data[
    (data[progress_today] >= 85) & (data[progress_today] < 100)
]

if not filtered_85_100.empty:

    comparison_df = filtered_85_100[[
        "District",
        progress_last,
        progress_today
    ]]

    # Convert to long format
    comparison_melted = comparison_df.melt(
        id_vars="District",
        value_vars=[progress_last, progress_today],
        var_name="Status Type",
        value_name="Progress %"
    )

    fig_compare = px.bar(
        comparison_melted,
        x="District",
        y="Progress %",
        color="Status Type",
        barmode="group",
        title="Last Status vs Today Progress"
    )

    st.plotly_chart(fig_compare, width="stretch")

else:
    st.info("No districts currently between 85% and 99%.")
    
    

   

