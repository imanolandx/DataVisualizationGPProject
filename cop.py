import streamlit as st
import plotly.express as px
import pandas as pd

def interactive_plot_dashboard(df):
    # Preprocess
    df["Tyre_Effectiveness"] = df["Stint Length"] / df["Lap Time Variation"]

    # Sidebar Filters
    drivers = sorted(df["Driver"].dropna().unique())
    compounds = sorted(df["Tire Compound"].dropna().unique())
    circuits = sorted(df["Circuit"].dropna().unique())

    selected_driver = st.selectbox("Select Driver (optional)", ["All"] + drivers)
    selected_compound = st.selectbox("Select Tyre Compound (optional)", ["All"] + compounds)
    selected_circuit = st.selectbox("Select Circuit (optional)", ["All"] + circuits)

    # Apply filters
    if selected_driver != "All":
        df = df[df["Driver"] == selected_driver]
    if selected_compound != "All":
        df = df[df["Tire Compound"] == selected_compound]
    if selected_circuit != "All":
        df = df[df["Circuit"] == selected_circuit]

    # Plot Type
    #plot_type = st.radio("Choose Plot Type:", ["Scatter", "Box", "Violin", "Facet Scatter", "Line (driver only)"])

    # Render appropriate plot
    try:
        fig = plot_scatter(df)
        #elif plot_type == "Box":
        #    fig = plot_box(df)
        #elif plot_type == "Violin":
        #    fig = plot_violin(df)
        #elif plot_type == "Facet Scatter":
        #    fig = plot_facet_scatter(df)
        #elif plot_type == "Line (driver only)":
        #    if selected_driver == "All":
        #        st.warning("Select a specific driver to view the line plot.")
        #        return
        #    fig = plot_line(df, selected_driver)

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating plot: {e}")

# Plot functions

def plot_scatter(df):
    return px.scatter(
        df,
        x="Driver Aggression Score",
        y="Tyre_Effectiveness",
        color="Driver",
        size="Stint Length",
        hover_name="Race Name",
        title="Scatter: Tyre Effectiveness vs. Aggression"
    )

#def plot_box(df):
#    return px.box(
#        df,
#        x="Tire Compound",
#        y="Tyre_Effectiveness",
#        color="Tire Compound",
#        points="all",
#        title="Box Plot: Tyre Effectiveness per Compound"
#    )
#
#def plot_violin(df):
#    return px.violin(
#        df,
#        x="Tire Compound",
#        y="Tyre_Effectiveness",
#        color="Tire Compound",
#        box=True,
#        points="all",
#        title="Violin Plot: Tyre Effectiveness Distribution"
#    )
#
#def plot_facet_scatter(df):
#    return px.scatter(
#        df,
#        x="Driver Aggression Score",
#        y="Tyre_Effectiveness",
#        color="Driver",
#        facet_col="Tire Compound",
#        hover_name="Race Name",
#        title="Facet Scatter: Aggression vs. Effectiveness by Compound"
#    )
#
#def plot_line(df, driver_name):
#    return px.line(
#        df,
#        x="Race Name",
#        y="Tyre_Effectiveness",
#        color="Tire Compound",
#        title=f"Line Plot: Tyre Effectiveness Over Races – {driver_name}"
#    )
