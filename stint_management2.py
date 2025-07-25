import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
csv_path = 'Data/f1_pitstops_2018_2024.csv'
df = pd.read_csv(csv_path)

st.set_page_config(page_title="Stint Management Strategies", layout="wide")
st.title("Stint Management Strategies by Driver / Team")

# Constructor colors (2018–2024)
constructor_colors = {
    'Red Bull': '#3671C6',
    'Mercedes': '#00D2BE',
    'Ferrari': '#DC0000',
    'McLaren': '#FF8700',
    'Aston Martin': '#006F62',
    'Alpine': '#0090FF',
    'AlphaTauri': '#2B4562',
    'Alpha Tauri': '#2B4562',
    'Racing Bulls': '#6692FF',
    'Williams': '#00A0DE',
    'Alfa Romeo': '#981E32',
    'Sauber': '#006EFF',
    'Haas': '#B6BABD',
    'Renault': '#FFF500',
    'Racing Point': '#F596C8',
    'Force India': '#F596C8',
    'Toro Rosso': '#1E41FF'
}

st.markdown("### Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_season = st.selectbox("Season", sorted(df['Season'].unique()))

filtered_by_season = df[df['Season'] == selected_season]

with col2:
    selected_round = st.selectbox("Round", sorted(filtered_by_season['Round'].unique()))

selected_race_df = filtered_by_season[filtered_by_season['Round'] == selected_round]

available_drivers = sorted(selected_race_df['Driver'].unique())
with col3:
    selected_driver = st.selectbox("Driver", ["All"] + available_drivers)

available_teams = sorted(selected_race_df['Constructor'].unique())
with col4:
    selected_team = st.selectbox("Constructor", ["All"] + available_teams)


# Apply filters
filtered = selected_race_df.copy()
if selected_driver != "All":
    filtered = filtered[filtered["Driver"] == selected_driver]
if selected_team != "All":
    filtered = filtered[filtered["Constructor"] == selected_team]

# Sort by stint number
filtered = filtered.sort_values(by=["Constructor", "Driver", "Stint"])

# Display stint table
st.markdown(f"### Stint Details - {filtered['Race Name'].iloc[0] if not filtered.empty else ''}")
st.dataframe(filtered[[
    "Driver", "Constructor", "Stint", "Tire Compound", "Stint Length",
    "Pit_Lap", "Pit_Time", "Tire Usage Aggression", "Driver Aggression Score"
]])

# Stint timeline graph
if not filtered.empty:
    st.markdown("### Stint Timeline")
    fig, ax = plt.subplots(figsize=(14, 5))
    for i, (driver, group) in enumerate(filtered.groupby("Driver")):
        for _, row in group.iterrows():
            ax.barh(driver, row["Stint Length"], left=row["Pit_Lap"] - row["Stint Length"],
                    color=constructor_colors.get(row['Constructor'], 'gray'), edgecolor='black')
            ax.text(row["Pit_Lap"] - row["Stint Length"] / 2, i, row["Tire Compound"],
                    ha='center', va='center', fontsize=7, color='white')
    ax.set_xlabel("Lap Number")
    ax.set_title(f"Stint Management - {selected_driver if selected_driver != 'All' else 'All Drivers'}")
    st.pyplot(fig)
else:
    st.warning("No data available for selected filters.")