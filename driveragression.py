import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your CSV file
df = pd.read_csv(r"C:\Users\imank\Desktop\CODING\DataVisualizationGPProject-1\Data\cleaned_pitstop_data2.csv")

# Strip column names and handle missing data
df.columns = df.columns.str.strip()
df = df.dropna(subset=['Driver', 'Season', 'Circuit', 'Stint', 'Driver Aggression Score'])

# Streamlit UI
st.title("F1 Driver Aggression Analysis")

# Prepare dropdown options
drivers = ["All"] + sorted(df['Driver'].dropna().unique().tolist())

# Column layout for filters
col1, col2, col3 = st.columns(3)

with col1:
    selected_driver = st.selectbox("Select a Driver:", drivers)

if selected_driver == "All":
    available_seasons = df['Season'].dropna().unique()
else:
    available_seasons = df[df['Driver'] == selected_driver]['Season'].dropna().unique()
seasons = ["All"] + sorted(available_seasons)

with col2:
    selected_season = st.selectbox("Select a Season:", seasons)

if selected_driver == "All" and selected_season == "All":
    available_tracks = df['Circuit'].dropna().unique()
else:
    filtered_temp = df.copy()
    if selected_driver != "All":
        filtered_temp = filtered_temp[filtered_temp['Driver'] == selected_driver]
    if selected_season != "All":
        filtered_temp = filtered_temp[filtered_temp['Season'] == selected_season]
    available_tracks = filtered_temp['Circuit'].dropna().unique()
tracks = ["All"] + sorted(available_tracks)

with col3:
    selected_track = st.selectbox("Select a Circuit:", tracks)

# Filter the DataFrame based on selections
filtered_df = df.copy()
if selected_driver != "All":
    filtered_df = filtered_df[filtered_df['Driver'] == selected_driver]
if selected_season != "All":
    filtered_df = filtered_df[filtered_df['Season'] == selected_season]
if selected_track != "All":
    filtered_df = filtered_df[filtered_df['Circuit'] == selected_track]

# Aggression Data Table
st.subheader(f"Aggression Data for {selected_driver} in {selected_season}")
if not filtered_df.empty:
    st.dataframe(filtered_df[['Season', 'Driver', 'Circuit', 'Race Name', 'Stint', 'Stint Length',
                              'Driver Aggression Score', 'Tire Compound', 'Position']])
else:
    st.warning("No data available for the selected filters.")

# Plot aggression score across stints
if not filtered_df.empty:
    st.subheader(f"Aggression Score per Stint: {selected_driver} in {selected_track} track for {selected_season} season")
    fig, ax = plt.subplots()
    sns.lineplot(data=filtered_df, x='Stint', y='Driver Aggression Score', hue='Tire Compound', marker='o', ax=ax)
    ax.set_title("Aggression Across Stints")
    ax.set_ylabel("Aggression Score")
    ax.set_xlabel("Stint")
    st.pyplot(fig)

# Top 10 aggressive drivers
st.subheader("Top 10 Drivers by Average Aggression Score")
top_aggression = df.groupby('Driver')['Driver Aggression Score'].mean().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_aggression.values, y=top_aggression.index, ax=ax2)
ax2.set_title("Top Aggressive Drivers (Avg Score)")
ax2.set_xlabel("Aggression Score")
st.pyplot(fig2)
