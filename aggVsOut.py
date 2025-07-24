import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def render():
    # Load data
    csv_path = 'C:/Users/user/Desktop/New folder/DataVisualizationGPProject/Data/cleaned_pitstop_data.csv'
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["Driver Aggression Score", "Position Changes"])

    st.title("📊 Aggression vs Outcome Correlation")
    st.markdown("Exploring how driver aggression relates to race performance (position changes).")

    # Sidebar filter
    st.sidebar.header("Filters")
    min_aggr, max_aggr = st.sidebar.slider(
        "Select Aggression Range",
        float(df["Driver Aggression Score"].min()), 
        float(df["Driver Aggression Score"].max()), 
        (float(df["Driver Aggression Score"].min()), float(df["Driver Aggression Score"].max()))
    )
    df_filtered = df[(df["Driver Aggression Score"] >= min_aggr) & (df["Driver Aggression Score"] <= max_aggr)]

    # --- Correlation Heatmap ---
    st.subheader("Correlation Heatmap")
    corr = df_filtered[["Driver Aggression Score", "Position Changes"]].corr()
    fig1, ax1 = plt.subplots(figsize=(5, 4))  # Bigger figure
    sns.heatmap(
        corr, 
        annot=True, 
        cmap="coolwarm", 
        fmt=".2f", 
        cbar=False, 
        ax=ax1,
        annot_kws={"size": 12}  # smaller annotation font
    )

    # Fix label orientation & font size
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0, ha='center', fontsize=12)
    ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0, va='center', fontsize=12)

    st.pyplot(fig1)


    # --- Scatterplot ---
    st.subheader("Scatterplot: Aggression vs Position Changes")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.regplot(data=df_filtered, x="Driver Aggression Score", y="Position Changes",
                scatter_kws={'alpha':0.6}, line_kws={"color": "red"}, ax=ax2)
    ax2.set_title("Driver Aggression vs Position Changes")
    st.pyplot(fig2)

    # Correlation coefficient
    corr_value, p_value = pearsonr(df_filtered["Driver Aggression Score"], df_filtered["Position Changes"])
    st.markdown(f"**Pearson correlation (r):** {corr_value:.2f} (p = {p_value:.3f})")

    # Interpretation
    st.markdown("""
    - **Heatmap:** Shows the correlation between aggression and position changes.  
      - **Positive correlation (closer to +1):** More aggression → tends to gain more positions.  
      - **Negative correlation (closer to -1):** More aggression → tends to lose positions.  
      - **Near 0:** Little to no relationship.
    - **Scatterplot:** Each dot = one stint (aggression score vs position change).  
      - The **red line** is a trend line showing the overall direction.
    
    ### Findings:
    - If the correlation is **positive and moderate (e.g., r ≈ 0.3–0.5)**: Aggressive drivers usually gain positions, but not always.  
    - If the correlation is **weak (r ≈ 0–0.2)**: Aggression doesn’t strongly affect race outcome (other factors like pit strategy or tyre choice dominate).
    """)
