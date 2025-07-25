import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
csv_path = 'Data/cleaned_pitstop_data.csv'
df = pd.read_csv(csv_path)

st.set_page_config(page_title="Stint Management Strategies", layout="wide")
st.title("Stint Management Strategies by Driver / Team")

# Top bar filters
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
filtered = filtered.sort_values(by=["Driver", "Stint"])

# Display table
st.markdown(f"### Stint Details - {filtered['Race Name'].iloc[0] if not filtered.empty else ''}")
st.dataframe(filtered[[
    "Driver", "Constructor", "Stint", "Tire Compound", "Stint Length",
    "Pit_Lap", "Pit_Time", "Tire Usage Aggression", "Driver Aggression Score"
]])

# Constructor colors
constructor_colors = {
    "Red Bull": "#0B1C80", "Ferrari": "#DC0000", "Mercedes": "#00D2BE",
    "McLaren": "#FF8700", "Alpine F1 Team": "#0090FF", "AlphaTauri": "#2B4562",
    "Racing Bulls": "#6692FF", "Aston Martin": "#006F62", "Alfa Romeo": "#900000",
    "Sauber": "#52E252", "Williams": "#005AFF", "Haas": "#FFFFFF",
    "Toro Rosso": "#0032FF", "Force India": "#F596C8"
}

# Timeline Plot
if not filtered.empty:
    st.markdown("### Tyre Stint")

    fig, ax = plt.subplots(figsize=(14, 6))

    # Sort by constructor then driver
    filtered = filtered.sort_values(by=["Constructor", "Driver"])
    drivers_sorted = filtered["Driver"].unique()

    for i, driver in enumerate(drivers_sorted):
        group = filtered[filtered["Driver"] == driver]
        constructor = group["Constructor"].iloc[0]
        color = constructor_colors.get(constructor, "gray")

        for _, row in group.iterrows():
            ax.barh(driver, row["Stint Length"], left=row["Pit_Lap"] - row["Stint Length"],
                    color=color, edgecolor='black')
            ax.text(row["Pit_Lap"] - row["Stint Length"] / 2, i, row["Tire Compound"],
                    ha='center', va='center', fontsize=8)

    ax.set_xlabel("Lap Number")
    ax.set_title(f"Stint Management - {selected_driver if selected_driver != 'All' else 'All Drivers'}")
    st.pyplot(fig)
else:
    st.warning("No data available for selected filters.")

# Average Pit Stop Time Plot
if not filtered.empty:
    st.markdown("### Average Pit Stop Time by Driver")
    avg_pitstop = filtered.groupby("Driver")["Pit_Time"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    driver_ordered = avg_pitstop.index.tolist()
    colors = [constructor_colors.get(filtered[filtered['Driver'] == d]['Constructor'].iloc[0], "gray") for d in driver_ordered]

    ax.bar(driver_ordered, avg_pitstop.values, color=colors, edgecolor='black')
    ax.set_ylabel("Average Pit Stop Time (s)")
    ax.set_title("Average Pit Stop Time by Driver")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)